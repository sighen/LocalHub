<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import client from '@/api/client'

const router = useRouter()

const categories = ['전체', '자유', '후기', '질문']

const category = ref('전체')
const keywordInput = ref('')
const keyword = ref('')
const posts = ref([])
const total = ref(0)
const page = ref(1)
const size = ref(10)
const loading = ref(false)
const errorMsg = ref('')

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / size.value)))

// 점 세개(⋯) 메뉴 상태
const openMenuId = ref(null)

// 목록에서 바로 삭제할 때 쓰는 비밀번호 모달
const deleteTarget = ref(null)
const deletePassword = ref('')
const deleteError = ref('')

async function fetchPosts() {
  loading.value = true
  errorMsg.value = ''
  try {
    const params = { page: page.value, size: size.value }
    if (category.value !== '전체') params.category = category.value
    if (keyword.value) params.keyword = keyword.value

    const { data } = await client.get('/posts', { params })
    posts.value = data.items
    total.value = data.total
  } catch (e) {
    errorMsg.value = '게시글을 불러오지 못했어요. 잠시 후 다시 시도해주세요.'
    posts.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function changeCategory(c) {
  category.value = c
  page.value = 1
}

function applySearch() {
  keyword.value = keywordInput.value.trim()
  page.value = 1
}

function goPage(n) {
  page.value = n
}

function openDetail(post) {
  router.push({ name: 'community-detail', params: { id: post.id } })
}

function toggleMenu(postId) {
  openMenuId.value = openMenuId.value === postId ? null : postId
}

function closeMenu() {
  openMenuId.value = null
}

function goEdit(post) {
  closeMenu()
  // 수정 폼은 상세 페이지의 수정 모달을 사용합니다.
  router.push({ name: 'community-detail', params: { id: post.id } })
}

function openDeleteFromMenu(post) {
  closeMenu()
  deleteTarget.value = post
  deletePassword.value = ''
  deleteError.value = ''
}

function closeDeleteModal() {
  deleteTarget.value = null
}

async function confirmDelete() {
  try {
    await client.delete(`/posts/${deleteTarget.value.id}`, { data: { password: deletePassword.value } })
    closeDeleteModal()
    fetchPosts()
  } catch (e) {
    deleteError.value = e.response?.data?.detail || '삭제에 실패했습니다.'
  }
}

function formatDate(iso) {
  const d = new Date(iso)
  return `${d.getMonth() + 1}.${d.getDate()}`
}

watch([category, keyword, page], fetchPosts)
onMounted(fetchPosts)
</script>

<template>
  <div class="board">
    <div class="board-header">
      <h1>여행자들의 이야기</h1>
      <div class="toolbar">
        <div class="tabs">
          <button
            v-for="c in categories"
            :key="c"
            :class="['tab', category === c ? 'active' : '']"
            @click="changeCategory(c)"
          >{{ c }}</button>
        </div>
        <div class="search-wrap">
          <input
            type="text"
            placeholder="제목·내용 검색"
            v-model="keywordInput"
            @keyup.enter="applySearch"
          />
        </div>
        <button class="write-btn" @click="router.push({ name: 'community-write' })">
          ✎ 글쓰기
        </button>
      </div>
    </div>

    <div class="list">
      <div v-if="loading" class="state-msg">불러오는 중…</div>
      <div v-else-if="errorMsg" class="state-msg error">{{ errorMsg }}</div>
      <div v-else-if="posts.length === 0" class="state-msg">아직 게시글이 없어요. 첫 글을 남겨보세요.</div>
      <div
        v-else
        class="row"
        v-for="p in posts"
        :key="p.id"
        @click="openDetail(p)"
      >
        <div :class="['badge', p.category]">{{ p.category }}</div>
        <div class="row-main">
          <p class="title">{{ p.title }}</p>
          <div class="meta">
            <span>👁 {{ p.view_count }}</span>
            <span>💬 {{ p.comment_count }}</span>
            <span>{{ formatDate(p.created_at) }}</span>
          </div>
        </div>

        <div class="row-menu">
          <button class="kebab-btn" @click.stop="toggleMenu(p.id)">⋯</button>
          <div v-if="openMenuId === p.id" class="menu-dropdown" @click.stop>
            <button @click="goEdit(p)">수정</button>
            <button class="danger" @click="openDeleteFromMenu(p)">삭제</button>
          </div>
        </div>
      </div>
    </div>

    <div class="pager" v-if="totalPages > 1">
      <button
        v-for="n in totalPages"
        :key="n"
        :class="page === n ? 'active' : ''"
        @click="goPage(n)"
      >{{ n }}</button>
    </div>

    <!-- 메뉴 바깥을 클릭하면 닫히도록 하는 투명 오버레이 -->
    <div v-if="openMenuId" class="click-catcher" @click="closeMenu"></div>

    <!-- 목록에서 바로 삭제하는 비밀번호 확인 모달 -->
    <div v-if="deleteTarget" class="overlay" @click.self="closeDeleteModal">
      <div class="modal">
        <h2>게시글 삭제</h2>
        <p class="modal-desc">'{{ deleteTarget.title }}' 글을 삭제하시려면 비밀번호를 입력해주세요.</p>
        <div class="field">
          <label>비밀번호</label>
          <input
            v-model="deletePassword"
            type="password"
            placeholder="비밀번호"
            @keyup.enter="confirmDelete"
          />
        </div>
        <div class="error-msg" v-if="deleteError">{{ deleteError }}</div>
        <div class="modal-actions">
          <button class="btn-ghost" @click="closeDeleteModal">취소</button>
          <button class="btn-solid danger" @click="confirmDelete">삭제 확인</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.board { max-width: 920px; margin: 0 auto; padding: 36px 20px 60px; }
.board-header { border-bottom: 1px solid #e2e0d6; padding-bottom: 20px; }
h1 { font-size: 28px; margin: 0 0 18px; }
.toolbar { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
.tabs { display: flex; gap: 4px; background: #ece9de; padding: 4px; border-radius: 10px; }
.tab { border: none; background: transparent; padding: 7px 14px; border-radius: 7px; font-size: 13.5px; font-weight: 600; color: #7c8a86; cursor: pointer; }
.tab.active { background: #fff; color: #1c2b2a; box-shadow: 0 1px 2px rgba(0,0,0,.08); }
.search-wrap { display: flex; align-items: center; background: #fff; border: 1px solid #e2e0d6; border-radius: 9px; padding: 0 10px; min-width: 220px; }
.search-wrap input { border: none; outline: none; padding: 9px 6px; font-size: 13.5px; width: 100%; background: transparent; }
.write-btn { margin-left: auto; border: none; background: #2f7f70; color: #fff; font-weight: 600; padding: 9px 16px; border-radius: 9px; font-size: 13.5px; cursor: pointer; }
.write-btn:hover { background: #235f54; }
.list { margin-top: 6px; }
.state-msg { padding: 60px 0; text-align: center; color: #7c8a86; font-size: 14px; }
.state-msg.error { color: #d9603f; }

.row { display: flex; align-items: flex-start; gap: 14px; padding: 18px 4px; border-bottom: 1px solid #e2e0d6; cursor: pointer; position: relative; }
.row:hover .title { color: #235f54; text-decoration: underline; }
.badge { flex: 0 0 46px; height: 46px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; color: #fff; background: #2f7f70; }
.badge.자유 { background: #c98a3a; }
.badge.질문 { background: #d9603f; }
.row-main { flex: 1; min-width: 0; }
.title { font-weight: 500; font-size: 16.5px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.meta { display: flex; gap: 12px; margin-top: 6px; font-size: 12.5px; color: #7c8a86; }

.row-menu { position: relative; flex-shrink: 0; }
.kebab-btn {
  border: none; background: transparent; font-size: 18px; line-height: 1; color: #7c8a86;
  cursor: pointer; padding: 4px 8px; border-radius: 6px;
}
.kebab-btn:hover { background: #ece9de; }
.menu-dropdown {
  position: absolute; right: 0; top: 32px; z-index: 20;
  background: #fff; border: 1px solid #e2e0d6; border-radius: 10px;
  box-shadow: 0 6px 18px rgba(0,0,0,.1); overflow: hidden; min-width: 96px;
}
.menu-dropdown button {
  display: block; width: 100%; text-align: left; border: none; background: transparent;
  padding: 9px 14px; font-size: 13px; cursor: pointer; color: #1c2b2a;
}
.menu-dropdown button:hover { background: #f5f6f2; }
.menu-dropdown button.danger { color: #d9603f; }
.click-catcher { position: fixed; inset: 0; z-index: 10; }

.pager { display: flex; justify-content: center; gap: 6px; margin-top: 28px; }
.pager button { border: 1px solid #e2e0d6; background: #fff; border-radius: 7px; width: 32px; height: 32px; font-size: 13px; cursor: pointer; }
.pager button.active { background: #2f7f70; color: #fff; border-color: #2f7f70; }

/* 삭제 모달 */
.overlay {
  position: fixed; inset: 0; background: rgba(20, 25, 24, 0.45);
  display: flex; align-items: flex-start; justify-content: center;
  padding: 8vh 16px; overflow-y: auto; z-index: 100;
}
.modal { background: #fff; border-radius: 14px; max-width: 420px; width: 100%; padding: 26px 28px 28px; }
.modal h2 { font-size: 20px; margin: 0 0 16px; }
.modal-desc { font-size: 13.5px; color: #7c8a86; margin: 0 0 16px; }
.field { margin-bottom: 14px; }
.field label { display: block; font-size: 12.5px; font-weight: 600; color: #7c8a86; margin-bottom: 5px; }
.field input { width: 100%; border: 1px solid #e2e0d6; border-radius: 8px; padding: 9px 11px; font-size: 14px; outline: none; box-sizing: border-box; }
.field input:focus { border-color: #2f7f70; }
.error-msg { color: #d9603f; font-size: 12.5px; margin: 4px 0 6px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 6px; }
.btn-ghost { border: 1px solid #e2e0d6; background: transparent; border-radius: 8px; padding: 9px 16px; font-size: 13.5px; cursor: pointer; color: #1c2b2a; }
.btn-solid { border: none; background: #2f7f70; color: #fff; border-radius: 8px; padding: 9px 18px; font-size: 13.5px; font-weight: 600; cursor: pointer; }
.btn-solid.danger { background: #d9603f; }
</style>