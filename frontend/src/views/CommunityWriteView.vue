<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import client from '@/api/client'

const router = useRouter()
const categories = ['자유', '후기', '질문']

const draft = ref({ title: '', content: '', category: '자유', password: '' })
const errorMsg = ref('')
const submitting = ref(false)

async function submitPost() {
  if (!draft.value.title || !draft.value.content || !draft.value.password) {
    errorMsg.value = '제목, 내용, 비밀번호는 필수예요.'
    return
  }
  errorMsg.value = ''
  submitting.value = true
  try {
    const { data } = await client.post('/posts', draft.value)
    router.push({ name: 'community-detail', params: { id: data.id } })
  } catch (e) {
    errorMsg.value = '게시글 등록에 실패했어요. 잠시 후 다시 시도해주세요.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="write">
    <h1>새 글 작성</h1>

    <div class="field">
      <label>카테고리</label>
      <select v-model="draft.category">
        <option v-for="c in categories" :key="c">{{ c }}</option>
      </select>
    </div>
    <div class="field">
      <label>제목</label>
      <input type="text" v-model="draft.title" placeholder="제목을 입력하세요" />
    </div>
    <div class="field">
      <label>내용</label>
      <textarea v-model="draft.content" placeholder="내용을 입력하세요"></textarea>
    </div>
    <div class="field">
      <label>비밀번호 (수정·삭제 시 필요)</label>
      <input type="password" v-model="draft.password" placeholder="4자리 이상" />
    </div>

    <div class="error-msg" v-if="errorMsg">{{ errorMsg }}</div>

    <div class="actions">
      <button class="btn-ghost" @click="router.push({ name: 'community-list' })">취소</button>
      <button class="btn-solid" :disabled="submitting" @click="submitPost">
        {{ submitting ? '등록 중…' : '등록' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.write { max-width: 560px; margin: 0 auto; padding: 36px 20px 60px; }
h1 { font-size: 24px; margin: 0 0 22px; }
.field { margin-bottom: 16px; }
.field label { display: block; font-size: 12.5px; font-weight: 600; color: #7c8a86; margin-bottom: 5px; }
.field input, .field textarea, .field select { width: 100%; border: 1px solid #e2e0d6; border-radius: 8px; padding: 9px 11px; font-size: 14px; outline: none; box-sizing: border-box; }
.field input:focus, .field textarea:focus, .field select:focus { border-color: #2f7f70; }
.field textarea { min-height: 160px; resize: vertical; }
.error-msg { color: #d9603f; font-size: 12.5px; margin: 4px 0 6px; }
.actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 10px; }
.btn-ghost { border: 1px solid #e2e0d6; background: transparent; border-radius: 8px; padding: 9px 16px; font-size: 13.5px; cursor: pointer; }
.btn-solid { border: none; background: #2f7f70; color: #fff; border-radius: 8px; padding: 9px 18px; font-size: 13.5px; font-weight: 600; cursor: pointer; }
.btn-solid:disabled { opacity: .6; cursor: default; }
</style>