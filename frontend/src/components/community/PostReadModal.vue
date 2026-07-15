<script setup>
import { ref, onMounted } from 'vue'
import client from '../../api/client'
import { useToast } from '../../composables/useToast'
import { useAppNavigation } from '../../composables/useAppNavigation'

const props = defineProps({
  post: { type: Object, required: true },
  readOnly: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'like', 'toggle-bookmark', 'edit', 'delete'])

const { showToast } = useToast()
const { goToPlace } = useAppNavigation()

const openLinkedPlace = () => {
  goToPlace(props.post.placeContentId, props.post.placeContentTypeId)
  emit('close')
}

const comments = ref([])
const isCommentsLoading = ref(false)
const commentsError = ref(false)

const newCommentContent = ref('')
const newCommentPassword = ref('')

const deletingCommentId = ref(null)
const deletePasswordInput = ref('')

const formatCommentDate = (isoString) => {
  const d = new Date(isoString)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  const hh = String(d.getHours()).padStart(2, '0')
  const min = String(d.getMinutes()).padStart(2, '0')
  return `${yyyy}.${mm}.${dd} ${hh}:${min}`
}

const fetchComments = async () => {
  isCommentsLoading.value = true
  commentsError.value = false
  try {
    const { data } = await client.get(`/posts/${props.post.id}/comments`)
    comments.value = data
  } catch (e) {
    commentsError.value = true
  } finally {
    isCommentsLoading.value = false
  }
}

const submitComment = async () => {
  if (!newCommentContent.value.trim() || !newCommentPassword.value) return
  try {
    await client.post(`/posts/${props.post.id}/comments`, {
      content: newCommentContent.value,
      password: newCommentPassword.value
    })
    newCommentContent.value = ''
    newCommentPassword.value = ''
    await fetchComments()
  } catch (e) {
    if (e?.response?.status === 400) {
      showToast(e.response.data?.detail || '등록할 수 없는 내용입니다.')
    } else {
      showToast('댓글 등록에 실패했어요. 잠시 후 다시 시도해주세요.')
    }
  }
}

const toggleDeleteInput = (commentId) => {
  deletingCommentId.value = deletingCommentId.value === commentId ? null : commentId
  deletePasswordInput.value = ''
}

const confirmDeleteComment = async (commentId) => {
  try {
    await client.delete(`/comments/${commentId}`, { data: { password: deletePasswordInput.value } })
    comments.value = comments.value.filter((c) => c.id !== commentId)
    deletingCommentId.value = null
  } catch (e) {
    if (e?.response?.status === 403) {
      showToast('비밀번호가 일치하지 않습니다.')
    } else {
      showToast('댓글 삭제에 실패했어요. 잠시 후 다시 시도해주세요.')
    }
  }
}

onMounted(() => {
  fetchComments()
})
</script>

<template>
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-xl overflow-hidden animate-fade-in flex flex-col max-h-[90vh]">
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center shrink-0">
        <span class="px-2.5 py-1 bg-blue-50 text-blue-600 text-xs font-bold rounded-lg border border-blue-100">{{ post.category }}</span>
        <button @click="emit('close')" class="p-1.5 text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <div class="p-6 space-y-5 overflow-y-auto">
        <div class="space-y-1.5">
          <button
            v-if="post.placeContentId"
            @click="openLinkedPlace"
            class="text-[11px] font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg hover:bg-emerald-100 transition"
          >
            <i class="fa-solid fa-location-dot mr-1"></i>{{ post.placeTitle }}
          </button>
          <h3 class="text-xl font-black text-slate-900 leading-tight">{{ post.title }}</h3>
          <div class="flex items-center gap-3 text-xs text-slate-400">
            <span>👤 익명</span>
            <span>•</span>
            <span>{{ post.date }}</span>
            <span>•</span>
            <span>조회수 {{ post.views }}</span>
          </div>
        </div>

        <div class="border-t border-b border-slate-100 py-4">
          <div v-if="post.image" class="mb-4 rounded-xl overflow-hidden max-h-56 border border-slate-200">
            <img :src="post.image" alt="Uploaded post item" class="w-full h-full object-cover" />
          </div>
          <p class="text-xs text-slate-600 leading-relaxed whitespace-pre-line">{{ post.content }}</p>
        </div>

        <div class="flex flex-wrap gap-1">
          <span v-for="tag in post.tags" :key="tag" class="text-[10px] bg-slate-100 text-slate-500 font-extrabold px-2 py-0.5 rounded">#{{ tag }}</span>
        </div>

        <div class="flex items-center justify-between pt-2">
          <div class="flex gap-4 text-xs font-bold text-slate-400">
            <button @click="emit('like', post.id)" class="hover:text-red-500 transition"><i class="fa-regular fa-heart mr-1"></i> 좋아요 {{ post.likes }}</button>
            <button @click="emit('toggle-bookmark', post.id)" :class="['transition', post.bookmarked ? 'text-yellow-500' : 'hover:text-yellow-500']">
              <i class="fa-regular fa-star"></i> 북마크
            </button>
          </div>

          <div v-if="!readOnly" class="flex gap-2">
            <button @click="emit('edit')" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition">수정</button>
            <button @click="emit('delete')" class="px-3.5 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 text-xs font-bold rounded-lg transition">삭제</button>
          </div>
        </div>

        <div class="border-t border-slate-100 pt-4 space-y-3">
          <h4 class="text-xs font-black text-slate-700">댓글 {{ comments.length }}개</h4>

          <div v-if="isCommentsLoading" class="text-[11px] text-slate-400 py-3 text-center">댓글을 불러오는 중입니다...</div>
          <div v-else-if="commentsError" class="text-[11px] text-slate-400 py-3 text-center">댓글을 불러오지 못했어요. 잠시 후 다시 시도해주세요.</div>
          <div v-else-if="comments.length === 0" class="text-[11px] text-slate-300 py-3 text-center">아직 댓글이 없습니다.</div>

          <div v-else class="space-y-2">
            <div v-for="comment in comments" :key="comment.id" class="bg-slate-50 rounded-xl px-3.5 py-2.5 space-y-1.5">
              <div class="flex items-start justify-between gap-2">
                <p class="text-xs text-slate-600 leading-relaxed whitespace-pre-line flex-grow">{{ comment.content }}</p>
                <button @click="toggleDeleteInput(comment.id)" class="p-1.5 text-slate-300 hover:text-red-500 transition shrink-0">
                  <i class="fa-solid fa-trash text-[11px]"></i>
                </button>
              </div>
              <p class="text-[10px] text-slate-400">{{ formatCommentDate(comment.created_at) }}</p>

              <div v-if="deletingCommentId === comment.id" class="flex gap-2 pt-1">
                <input
                  type="password"
                  v-model="deletePasswordInput"
                  placeholder="비밀번호 입력"
                  class="flex-grow px-3 py-1.5 text-[11px] bg-white border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button @click="confirmDeleteComment(comment.id)" class="px-3 py-1.5 text-[10px] font-bold text-white bg-red-500 hover:bg-red-600 rounded-lg">삭제 확인</button>
                <button @click="toggleDeleteInput(comment.id)" class="px-3 py-1.5 text-[10px] font-bold text-slate-500 hover:bg-slate-100 rounded-lg">취소</button>
              </div>
            </div>
          </div>

          <form @submit.prevent="submitComment" class="flex flex-col gap-2 pt-2">
            <textarea
              v-model="newCommentContent"
              rows="2"
              placeholder="댓글을 입력하세요..."
              class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white resize-none"
              required
            ></textarea>
            <div class="flex gap-2">
              <input
                type="password"
                v-model="newCommentPassword"
                placeholder="비밀번호"
                class="w-32 px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white"
                required
              />
              <button type="submit" class="ml-auto px-4 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 rounded-xl transition">댓글 등록</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
