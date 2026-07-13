<template>
  <main v-if="post">
    <h1>{{ post.title }}</h1>
    <p class="meta">조회수 {{ post.view_count }}</p>
    <div class="content">{{ post.content }}</div>

    <button @click="showDeleteForm = true">삭제</button>

    <div v-if="showDeleteForm">
      <input v-model="password" type="password" placeholder="비밀번호" />
      <button @click="deletePost">확인</button>
    </div>

    <section class="comments">
      <h2>댓글</h2>
      <ul>
        <li v-for="c in comments" :key="c.id">{{ c.content }}</li>
      </ul>
      <input v-model="newComment" placeholder="댓글 내용" />
      <input v-model="commentPassword" type="password" placeholder="비밀번호" />
      <button @click="addComment">등록</button>
    </section>
  </main>
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
const showDeleteForm = ref(false);
const password = ref("");
const newComment = ref("");
const commentPassword = ref("");

async function fetchPost() {
  const { data } = await client.get(`/posts/${postId}`);
  post.value = data;
}

async function fetchComments() {
  const { data } = await client.get(`/posts/${postId}/comments`);
  comments.value = data;
}

async function deletePost() {
  try {
    await client.delete(`/posts/${postId}`, { data: { password: password.value } });
    router.push("/community");
  } catch (e) {
    alert(e.response?.data?.detail || "삭제에 실패했습니다.");
  }
}

async function addComment() {
  await client.post(`/posts/${postId}/comments`, {
    content: newComment.value,
    password: commentPassword.value,
  });
  newComment.value = "";
  commentPassword.value = "";
  fetchComments();
}

onMounted(() => {
  fetchPost();
  fetchComments();
});
</script>
