<template>
  <div class="detail">
    <button class="back-btn" @click="router.push({ name: 'community-list' })">← 목록으로</button>

    <p v-if="loadError" class="state-msg error">{{ loadError }}</p>

    <template v-else-if="post">
      <div class="title-row">
        <h1>{{ post.title }}</h1>
        <div class="actions">
          <button class="btn-ghost" @click="openEditModal">수정</button>
          <button class="btn-ghost danger" @click="openDeleteModal">삭제</button>
        </div>
      </div>
      <div class="detail-meta">
        <span>{{ post.category }}</span>
        <span>👁 {{ post.view_count }}</span>
      </div>
      <div class="detail-content">{{ post.content }}</div>

      <div class="comments">
        <h3>댓글</h3>
        <p v-if="commentError" class="state-msg error small">{{ commentError }}</p>
        <template v-else>
          <div v-if="comments.length === 0" class="state-msg small">첫 댓글을 남겨보세요.</div>
          <div class="comment" v-for="c in comments" :key="c.id">
            <span class="comment-text">{{ c.content }}</span>
            <div class="comment-actions">
              <button class="link-btn" @click="openCommentEditModal(c)">수정</button>
              <button class="link-btn danger" @click="openCommentDeleteModal(c)">삭제</button>
            </div>
          </div>
        </template>

        <div class="comment-form">
          <input v-model="newComment" type="text" placeholder="댓글 내용" @keyup.enter="addComment" />
          <input v-model="commentPassword" type="password" placeholder="비밀번호" />
          <button class="btn-solid" @click="addComment">등록</button>
        </div>
      </div>
    </template>

    <div v-else class="state-msg">불러오는 중…</div>

    <!-- 게시글/댓글 수정·삭제 공용 모달 -->
    <div v-if="modalMode" class="overlay" @click.self="closeModal">
      <div class="modal">
        <template v-if="modalMode === 'edit-post'">
          <h2>게시글 수정</h2>
          <div class="field">
            <label>제목</label>
            <input v-model="editTitle" type="text" placeholder="제목" />
          </div>
          <div class="field">
            <label>내용</label>
            <textarea v-model="editContent" placeholder="내용"></textarea>
          </div>
        </template>

        <template v-else-if="modalMode === 'delete-post'">
          <h2>게시글 삭제</h2>
          <p class="modal-desc">삭제하시려면 비밀번호를 입력해주세요.</p>
        </template>

        <template v-else-if="modalMode === 'edit-comment'">
          <h2>댓글 수정</h2>
          <div class="field">
            <label>내용</label>
            <textarea v-model="editCommentContent" placeholder="댓글 내용"></textarea>
          </div>
        </template>

        <template v-else>
          <h2>댓글 삭제</h2>
          <p class="modal-desc">삭제하시려면 비밀번호를 입력해주세요.</p>
        </template>

        <div class="field">
          <label>비밀번호</label>
          <input
            v-model="modalPassword"
            type="password"
            placeholder="비밀번호"
            @keyup.enter="handleModalEnter"
          />
        </div>
        <div class="error-msg" v-if="modalError">{{ modalError }}</div>

        <div class="modal-actions">
          <button class="btn-ghost" @click="closeModal">취소</button>
          <button
            v-if="modalMode === 'edit-post'"
            class="btn-solid"
            @click="submitEdit"
          >수정 완료</button>
          <button
            v-else-if="modalMode === 'delete-post'"
            class="btn-solid danger"
            @click="submitDelete"
          >삭제 확인</button>
          <button
            v-else-if="modalMode === 'edit-comment'"
            class="btn-solid"
            @click="submitCommentEdit"
          >수정 완료</button>
          <button v-else class="btn-solid danger" @click="submitCommentDelete">삭제 확인</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import client from "../api/client";

const route = useRoute();
const router = useRouter();
const postId = route.params.id;

const post = ref(null);
const comments = ref([]);
const loadError = ref("");
const commentError = ref("");

const newComment = ref("");
const commentPassword = ref("");

// 게시글/댓글 수정·삭제 공용 모달 상태
// modalMode: "edit-post" | "delete-post" | "edit-comment" | "delete-comment" | null
const modalMode = ref(null);
const modalPassword = ref("");
const modalError = ref("");
const editTitle = ref("");
const editContent = ref("");
const editCommentContent = ref("");
const activeCommentId = ref(null);

async function fetchPost() {
  try {
    const { data } = await client.get(`/posts/${postId}`);
    post.value = data;
    loadError.value = "";
  } catch (e) {
    loadError.value = "게시글을 불러오지 못했어요.";
  }
}

async function fetchComments() {
  try {
    const { data } = await client.get(`/posts/${postId}/comments`);
    comments.value = data;
    commentError.value = "";
  } catch (e) {
    commentError.value = "댓글을 불러오지 못했어요.";
  }
}

function openEditModal() {
  editTitle.value = post.value.title;
  editContent.value = post.value.content;
  modalPassword.value = "";
  modalError.value = "";
  modalMode.value = "edit-post";
}

function openDeleteModal() {
  modalPassword.value = "";
  modalError.value = "";
  modalMode.value = "delete-post";
}

function openCommentEditModal(c) {
  activeCommentId.value = c.id;
  editCommentContent.value = c.content;
  modalPassword.value = "";
  modalError.value = "";
  modalMode.value = "edit-comment";
}

function openCommentDeleteModal(c) {
  activeCommentId.value = c.id;
  modalPassword.value = "";
  modalError.value = "";
  modalMode.value = "delete-comment";
}

function closeModal() {
  modalMode.value = null;
  activeCommentId.value = null;
}

function handleModalEnter() {
  if (modalMode.value === "edit-post") submitEdit();
  else if (modalMode.value === "delete-post") submitDelete();
  else if (modalMode.value === "edit-comment") submitCommentEdit();
  else if (modalMode.value === "delete-comment") submitCommentDelete();
}

async function submitEdit() {
  try {
    const { data } = await client.put(`/posts/${postId}`, {
      title: editTitle.value,
      content: editContent.value,
      category: post.value.category,
      password: modalPassword.value,
    });
    post.value = data;
    closeModal();
  } catch (e) {
    modalError.value = e.response?.data?.detail || "수정에 실패했습니다.";
  }
}

async function submitDelete() {
  try {
    await client.delete(`/posts/${postId}`, { data: { password: modalPassword.value } });
    router.push("/community");
  } catch (e) {
    modalError.value = e.response?.data?.detail || "삭제에 실패했습니다.";
  }
}

async function submitCommentEdit() {
  try {
    // 주의: 백엔드에 PUT /api/comments/{id} 엔드포인트가 아직 명세에 없어요.
    // 게시글 수정과 동일한 패턴으로 팀원에게 추가를 요청해야 동작합니다.
    await client.put(`/comments/${activeCommentId.value}`, {
      content: editCommentContent.value,
      password: modalPassword.value,
    });
    closeModal();
    fetchComments();
  } catch (e) {
    modalError.value = e.response?.data?.detail || "댓글 수정에 실패했습니다.";
  }
}

async function submitCommentDelete() {
  try {
    await client.delete(`/comments/${activeCommentId.value}`, { data: { password: modalPassword.value } });
    closeModal();
    fetchComments();
  } catch (e) {
    modalError.value = e.response?.data?.detail || "댓글 삭제에 실패했습니다.";
  }
}

async function addComment() {
  if (!newComment.value.trim()) return;
  try {
    await client.post(`/posts/${postId}/comments`, {
      content: newComment.value,
      password: commentPassword.value,
    });
    newComment.value = "";
    commentPassword.value = "";
    fetchComments();
  } catch (e) {
    alert(e.response?.data?.detail || "댓글 등록에 실패했습니다.");
  }
}

onMounted(() => {
  fetchPost();
  fetchComments();
});
</script>

<style scoped>
.detail { max-width: 720px; margin: 0 auto; padding: 36px 20px 60px; }
.back-btn { border: none; background: transparent; color: #7c8a86; font-size: 13px; cursor: pointer; padding: 0; margin-bottom: 18px; }

.title-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
h1 { font-size: 24px; margin: 0; flex: 1; }
.actions { display: flex; gap: 8px; flex-shrink: 0; }

.detail-meta { display: flex; gap: 14px; color: #7c8a86; font-size: 12.5px; margin: 10px 0 18px; }
.detail-content {
  font-size: 14.5px; line-height: 1.75; white-space: pre-wrap;
  padding-bottom: 22px; border-bottom: 1px solid #e2e0d6; margin-bottom: 20px;
}

.state-msg { padding: 60px 0; text-align: center; color: #7c8a86; font-size: 14px; }
.state-msg.small { padding: 16px 0; }
.state-msg.error { color: #d9603f; }

.comments h3 { font-size: 14px; margin: 0 0 12px; }
.comment {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid #e2e0d6; font-size: 13.5px;
}
.comment-text { flex: 1; }
.comment-actions { display: flex; gap: 10px; flex-shrink: 0; }
.link-btn {
  border: none; background: transparent; color: #7c8a86; font-size: 12px;
  cursor: pointer; padding: 0;
}
.link-btn.danger { color: #d9603f; }
.link-btn:hover { text-decoration: underline; }

.comment-form { display: flex; gap: 8px; margin-top: 14px; }
.comment-form input[type="text"] {
  flex: 1; border: 1px solid #e2e0d6; border-radius: 8px; padding: 9px 11px; font-size: 13.5px;
}
.comment-form input[type="password"] {
  width: 100px; border: 1px solid #e2e0d6; border-radius: 8px; padding: 9px 11px; font-size: 13.5px;
}

.btn-ghost {
  border: 1px solid #e2e0d6; background: transparent; border-radius: 8px;
  padding: 7px 14px; font-size: 13px; cursor: pointer; color: #1c2b2a;
}
.btn-ghost.danger { color: #d9603f; border-color: #ecc3b8; }
.btn-solid {
  border: none; background: #2f7f70; color: #fff; border-radius: 8px;
  padding: 9px 18px; font-size: 13.5px; font-weight: 600; cursor: pointer;
}
.btn-solid.danger { background: #d9603f; }
.error-msg { color: #d9603f; font-size: 12.5px; margin: 4px 0 6px; }

/* 모달 */
.overlay {
  position: fixed; inset: 0; background: rgba(20, 25, 24, 0.45);
  display: flex; align-items: flex-start; justify-content: center;
  padding: 8vh 16px; overflow-y: auto; z-index: 100;
}
.modal {
  background: #fff; border-radius: 14px; max-width: 420px; width: 100%;
  padding: 26px 28px 28px;
}
.modal h2 { font-size: 20px; margin: 0 0 16px; }
.modal-desc { font-size: 13.5px; color: #7c8a86; margin: 0 0 16px; }
.field { margin-bottom: 14px; }
.field label { display: block; font-size: 12.5px; font-weight: 600; color: #7c8a86; margin-bottom: 5px; }
.field input, .field textarea {
  width: 100%; border: 1px solid #e2e0d6; border-radius: 8px; padding: 9px 11px;
  font-size: 14px; outline: none; box-sizing: border-box; font-family: inherit;
}
.field input:focus, .field textarea:focus { border-color: #2f7f70; }
.field textarea { min-height: 120px; resize: vertical; }
.modal-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 6px; }
</style>