<script setup>
import { ref, onMounted } from 'vue'
import { usePosts } from '../../composables/usePosts'
import CommunityBoard from './CommunityBoard.vue'
import PostReadModal from './PostReadModal.vue'
import PostWriteModal from './PostWriteModal.vue'
import PasswordModal from './PasswordModal.vue'

const {
  boardTagFilter,
  filterBookmarkedOnly,
  searchQuery,
  filteredPosts,
  loadPosts,
  incrementViews,
  upsertPost,
  deletePost,
  likePost,
  toggleBookmark
} = usePosts()

const isReadModalOpen = ref(false)
const isWriteModalOpen = ref(false)
const isPwModalOpen = ref(false)
const pwError = ref(false)
const pwVerifyInput = ref('')

const currentActivePost = ref({})
const postForm = ref({ id: null, category: '관광지', title: '', content: '', password: '', tagsRaw: '', image: '' })

let activeAction = ''

const openCreatePostModal = () => {
  postForm.value = { id: null, category: '관광지', title: '', content: '', password: '', tagsRaw: '', image: '' }
  isWriteModalOpen.value = true
}

const openReadPostModal = (post) => {
  incrementViews(post)
  currentActivePost.value = post
  isReadModalOpen.value = true
}

const savePostForm = () => {
  upsertPost(postForm.value)
  isWriteModalOpen.value = false
}

const triggerAction = (type) => {
  activeAction = type
  pwVerifyInput.value = ''
  pwError.value = false
  isPwModalOpen.value = true
}

const submitPasswordVerification = () => {
  if (pwVerifyInput.value === currentActivePost.value.password) {
    isPwModalOpen.value = false
    isReadModalOpen.value = false
    if (activeAction === 'edit') {
      postForm.value = {
        id: currentActivePost.value.id,
        category: currentActivePost.value.category,
        title: currentActivePost.value.title,
        content: currentActivePost.value.content,
        password: currentActivePost.value.password,
        tagsRaw: currentActivePost.value.tags.join(', '),
        image: currentActivePost.value.image
      }
      isWriteModalOpen.value = true
    } else {
      deletePost(currentActivePost.value.id)
    }
  } else {
    pwError.value = true
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
      v-model:board-tag-filter="boardTagFilter"
      v-model:filter-bookmarked-only="filterBookmarkedOnly"
      v-model:search-query="searchQuery"
      @open-create="openCreatePostModal"
      @open-read="openReadPostModal"
      @like-post="likePost"
      @toggle-bookmark="toggleBookmark"
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
