<script setup>
import { ref, computed, watch } from 'vue'
import { usePosts } from '../../composables/usePosts'
import { useToast } from '../../composables/useToast'
import { useAppNavigation } from '../../composables/useAppNavigation'
import { useRouter } from '../../composables/useRouter'
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
  placeFilter,
  setPlaceFilter,
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
const { goToPlace } = useAppNavigation()
const { segments, query, navigate } = useRouter()

// 현재 쿼리스트링을 유지한 채 목록/작성 경로를 오갈 때 쓰는 헬퍼.
// (예: ?place=123으로 필터링된 채 글을 읽고 다시 목록으로 돌아와도 필터 유지)
const qs = computed(() => {
  const s = query.value.toString()
  return s ? `?${s}` : ''
})

// /community/post/:id 면 해당 글 상세, /community/write면 새 글 작성.
const postId = computed(() => (segments.value[0] === 'community' && segments.value[1] === 'post' ? segments.value[2] || null : null))
const isWriteRoute = computed(() => segments.value[0] === 'community' && segments.value[1] === 'write')
const placeFilterId = computed(() => query.value.get('place') || null)
const placeFilterTitle = computed(() => query.value.get('placeTitle') || '')

const isReadModalOpen = ref(false)
const isEditingLocally = ref(false)
const isWriteModalOpen = computed(() => isWriteRoute.value || isEditingLocally.value)
const isPwModalOpen = ref(false)
const pwError = ref(false)
const pwVerifyInput = ref('')
const writeError = ref('')

const currentActivePost = ref({})
const blankPostForm = () => ({
  id: null,
  category: '관광지',
  title: '',
  content: '',
  password: '',
  tagsRaw: '',
  image: '',
  placeContentId: null,
  placeTitle: '',
  placeContentTypeId: null
})
const postForm = ref(blankPostForm())

let activeAction = ''

const closeReadModal = () => {
  isReadModalOpen.value = false
  navigate(`/community${qs.value}`)
}

const closeWriteModal = () => {
  isEditingLocally.value = false
  if (isWriteRoute.value) navigate(`/community${qs.value}`)
}

const openCreatePostModal = () => {
  postForm.value = blankPostForm()
  writeError.value = ''
  navigate(`/community/write${qs.value}`)
}

const clearPlaceFilter = () => {
  navigate('/community')
}

const openReadPostModal = (post) => {
  navigate(`/community/post/${post.id}${qs.value}`)
}

const savePostForm = async () => {
  writeError.value = ''
  try {
    if (postForm.value.id) {
      await updatePost(postForm.value)
    } else {
      await createPost(postForm.value)
    }
    closeWriteModal()
  } catch (e) {
    if (e?.response?.status === 403) {
      writeError.value = '비밀번호가 일치하지 않습니다.'
    } else if (e?.response?.status === 400) {
      writeError.value = e.response.data?.detail || '등록할 수 없는 내용입니다.'
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
      image: currentActivePost.value.image,
      placeContentId: currentActivePost.value.placeContentId,
      placeTitle: currentActivePost.value.placeTitle,
      placeContentTypeId: currentActivePost.value.placeContentTypeId
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
    isEditingLocally.value = true
    return
  }

  try {
    await deletePost(currentActivePost.value.id, pwVerifyInput.value)
    isPwModalOpen.value = false
    closeReadModal()
  } catch (e) {
    if (e?.response?.status === 403) {
      pwError.value = true
    } else {
      isPwModalOpen.value = false
      closeReadModal()
      showToast('삭제에 실패했어요. 잠시 후 다시 시도해주세요.')
    }
  }
}

// postId가 바뀌면(다른 글을 열거나, 뒤로가기로 글을 닫거나) 진행 중이던
// 로컬 수정 오버레이는 더 이상 유효하지 않으므로 정리한다.
watch(postId, async (id) => {
  isEditingLocally.value = false

  if (!id) {
    isReadModalOpen.value = false
    return
  }

  const detail = await fetchPostDetail(id)
  if (!detail) {
    showToast('게시글을 불러오지 못했어요. 잠시 후 다시 시도해주세요.')
    navigate('/community', { replace: true })
    return
  }
  currentActivePost.value = detail
  isReadModalOpen.value = true
}, { immediate: true })

watch(isWriteRoute, (isWrite) => {
  if (!isWrite) return
  postForm.value = {
    ...blankPostForm(),
    category: '관광지',
    placeContentId: query.value.get('placeId') || null,
    placeTitle: query.value.get('placeTitle') || '',
    placeContentTypeId: query.value.get('placeType') ? Number(query.value.get('placeType')) : null
  }
  writeError.value = ''
}, { immediate: true })

watch(placeFilterId, (id) => {
  setPlaceFilter(id)
}, { immediate: true })
</script>

<template>
  <div>
    <CommunityBoard
      :filtered-posts="filteredPosts"
      :is-loading="isLoading"
      :load-error="loadError"
      :place-filter-title="placeFilterTitle"
      v-model:board-tag-filter="boardTagFilter"
      v-model:filter-bookmarked-only="filterBookmarkedOnly"
      v-model:search-query="searchQuery"
      @open-create="openCreatePostModal"
      @open-read="openReadPostModal"
      @like-post="likePost"
      @toggle-bookmark="toggleBookmark"
      @retry="loadPosts"
      @clear-place-filter="clearPlaceFilter"
      @go-to-place="(p) => goToPlace(p.contentId, p.contentTypeId)"
    />

    <PostReadModal
      v-if="isReadModalOpen"
      :post="currentActivePost"
      @close="closeReadModal"
      @like="likePost"
      @toggle-bookmark="toggleBookmark"
      @edit="triggerAction('edit')"
      @delete="triggerAction('delete')"
    />

    <PostWriteModal
      v-if="isWriteModalOpen"
      v-model="postForm"
      :error="writeError"
      @close="closeWriteModal"
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
