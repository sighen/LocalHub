<script setup>
import { ref, onMounted } from 'vue'
import { usePosts } from '../../composables/usePosts'
import { useToast } from '../../composables/useToast'
import CommunityBoard from './CommunityBoard.vue'
import PostReadModal from './PostReadModal.vue'
import PostWriteModal from './PostWriteModal.vue'
import PasswordModal from './PasswordModal.vue'

const {
  boardTagFilter,
  filterBookmarkedOnly,
  searchQuery,
  filteredPosts,
  isLoading,
  loadError,
  loadPosts,
  fetchPostDetail,
  createPost,
  updatePost,
  verifyPassword,
  deletePost,
  likePost,
  toggleBookmark
} = usePosts()

const { showToast } = useToast()

const isReadModalOpen = ref(false)
const isWriteModalOpen = ref(false)
const isPwModalOpen = ref(false)
const pwError = ref(false)
const pwVerifyInput = ref('')
const writeError = ref('')

const currentActivePost = ref({})
const postForm = ref({ id: null, category: '관광지', title: '', content: '', password: '', tagsRaw: '', image: '' })

let activeAction = ''

const openCreatePostModal = () => {
  postForm.value = { id: null, category: '관광지', title: '', content: '', password: '', tagsRaw: '', image: '' }
  writeError.value = ''
  isWriteModalOpen.value = true
}

const openReadPostModal = async (post) => {
  const detail = await fetchPostDetail(post.id)
  if (!detail) {
    showToast('게시글을 불러오지 못했어요. 잠시 후 다시 시도해주세요.')
    return
  }
  currentActivePost.value = detail
  isReadModalOpen.value = true
}

const savePostForm = async () => {
  writeError.value = ''
  try {
    if (postForm.value.id) {
      await updatePost(postForm.value)
    } else {
      await createPost(postForm.value)
    }
    isWriteModalOpen.value = false
  } catch (e) {
    if (e?.response?.status === 403) {
      writeError.value = '비밀번호가 일치하지 않습니다.'
    } else {
      writeError.value = '저장에 실패했어요. 잠시 후 다시 시도해주세요.'
    }
  }
}

const triggerAction = (type) => {
  activeAction = type
  pwVerifyInput.value = ''
  pwError.value = false
  isPwModalOpen.value = true
}

const submitPasswordVerification = async () => {
  if (activeAction === 'edit') {
    const form = {
      id: currentActivePost.value.id,
      category: currentActivePost.value.category,
      title: currentActivePost.value.title,
      content: currentActivePost.value.content,
      password: pwVerifyInput.value,
      tagsRaw: currentActivePost.value.tags.join(', '),
      image: currentActivePost.value.image
    }

    try {
      await verifyPassword(currentActivePost.value.id, pwVerifyInput.value)
    } catch (e) {
      if (e?.response?.status === 403) {
        pwError.value = true
      } else {
        isPwModalOpen.value = false
        showToast('비밀번호 확인에 실패했어요. 잠시 후 다시 시도해주세요.')
      }
      return
    }

    postForm.value = form
    writeError.value = ''
    isPwModalOpen.value = false
    isReadModalOpen.value = false
    isWriteModalOpen.value = true
    return
  }

  try {
    await deletePost(currentActivePost.value.id, pwVerifyInput.value)
    isPwModalOpen.value = false
    isReadModalOpen.value = false
  } catch (e) {
    if (e?.response?.status === 403) {
      pwError.value = true
    } else {
      isPwModalOpen.value = false
      isReadModalOpen.value = false
      showToast('삭제에 실패했어요. 잠시 후 다시 시도해주세요.')
    }
  }
}

onMounted(() => {
  loadPosts()
})
</script>

<template>
  <div>
    <CommunityBoard
      :filtered-posts="filteredPosts"
      :is-loading="isLoading"
      :load-error="loadError"
      v-model:board-tag-filter="boardTagFilter"
      v-model:filter-bookmarked-only="filterBookmarkedOnly"
      v-model:search-query="searchQuery"
      @open-create="openCreatePostModal"
      @open-read="openReadPostModal"
      @like-post="likePost"
      @toggle-bookmark="toggleBookmark"
      @retry="loadPosts"
    />

    <PostReadModal
      v-if="isReadModalOpen"
      :post="currentActivePost"
      @close="isReadModalOpen = false"
      @like="likePost"
      @toggle-bookmark="toggleBookmark"
      @edit="triggerAction('edit')"
      @delete="triggerAction('delete')"
    />

    <PostWriteModal
      v-if="isWriteModalOpen"
      v-model="postForm"
      :error="writeError"
      @close="isWriteModalOpen = false"
      @submit="savePostForm"
    />

    <PasswordModal
      v-if="isPwModalOpen"
      v-model:pw-verify-input="pwVerifyInput"
      :pw-error="pwError"
      @close="isPwModalOpen = false"
      @confirm="submitPasswordVerification"
    />
  </div>
</template>
