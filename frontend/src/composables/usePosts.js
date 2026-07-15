import { ref, computed } from 'vue'
import client from '../api/client'

// 좋아요/북마크/태그/이미지는 백엔드 컬럼이 없어 브라우저별 localStorage 오버레이로만 관리한다.
// (다른 브라우저/기기에서는 이 값들이 다르게 보이는 게 정상 동작)
const OVERLAY_KEY = 'visit_seoul_post_overlay'

const loadOverlay = () => {
  const raw = localStorage.getItem(OVERLAY_KEY)
  return raw ? JSON.parse(raw) : {}
}

const saveOverlay = (overlay) => {
  localStorage.setItem(OVERLAY_KEY, JSON.stringify(overlay))
}

const getOverlayFor = (overlay, id) => overlay[id] || { likes: 0, bookmarked: false, tags: [], image: '' }

const formatDate = (isoString) => {
  const d = new Date(isoString)
  const yyyy = d.getFullYear()
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${yyyy}.${mm}.${dd}`
}

export function usePosts() {
  const posts = ref([])
  const boardTagFilter = ref('')
  const filterBookmarkedOnly = ref(false)
  const searchQuery = ref('')
  const isLoading = ref(false)
  const loadError = ref(false)
  const placeFilter = ref(null)

  const decorateListItem = (p) => {
    const overlay = loadOverlay()
    const ov = getOverlayFor(overlay, p.id)
    return {
      id: p.id,
      category: p.category,
      title: p.title,
      date: formatDate(p.created_at),
      views: p.view_count,
      commentCount: p.comment_count,
      likes: ov.likes,
      bookmarked: ov.bookmarked,
      tags: ov.tags,
      image: ov.image,
      placeContentId: p.place_content_id,
      placeTitle: p.place_title,
      placeContentTypeId: p.place_content_type_id
    }
  }

  const decorateDetail = (p) => {
    const overlay = loadOverlay()
    const ov = getOverlayFor(overlay, p.id)
    return {
      id: p.id,
      category: p.category,
      title: p.title,
      content: p.content,
      date: formatDate(p.created_at),
      views: p.view_count,
      likes: ov.likes,
      bookmarked: ov.bookmarked,
      tags: ov.tags,
      image: ov.image,
      placeContentId: p.place_content_id,
      placeTitle: p.place_title,
      placeContentTypeId: p.place_content_type_id
    }
  }

  const updatePostInList = (id, patch) => {
    const idx = posts.value.findIndex((p) => p.id === id)
    if (idx !== -1) {
      posts.value[idx] = { ...posts.value[idx], ...patch }
    }
  }

  const filteredPosts = computed(() =>
    posts.value.filter((p) => {
      const matchesTag = !boardTagFilter.value || p.category === boardTagFilter.value
      const matchesBookmark = !filterBookmarkedOnly.value || p.bookmarked
      const query = searchQuery.value.toLowerCase()
      const matchesSearch = !query || p.title.toLowerCase().includes(query)
      return matchesTag && matchesBookmark && matchesSearch
    })
  )

  const loadPosts = async () => {
    isLoading.value = true
    loadError.value = false
    try {
      const { data } = await client.get('/posts', {
        params: { size: 100, place_content_id: placeFilter.value || undefined }
      })
      posts.value = data.items.map(decorateListItem)
    } catch (e) {
      loadError.value = true
    } finally {
      isLoading.value = false
    }
  }

  const setPlaceFilter = (placeContentId) => {
    placeFilter.value = placeContentId
    loadPosts()
  }

  const fetchPostDetail = async (id) => {
    try {
      const { data } = await client.get(`/posts/${id}`)
      const detail = decorateDetail(data)
      updatePostInList(id, { views: detail.views })
      return detail
    } catch (e) {
      return null
    }
  }

  const createPost = async (form) => {
    const { data } = await client.post('/posts', {
      title: form.title,
      content: form.content,
      category: form.category,
      password: form.password,
      place_content_id: form.placeContentId || undefined
    })

    const overlay = loadOverlay()
    overlay[data.id] = {
      likes: 0,
      bookmarked: false,
      tags: form.tagsRaw.split(',').map((t) => t.trim()).filter(Boolean),
      image: form.image
    }
    saveOverlay(overlay)

    posts.value.unshift({
      id: data.id,
      category: form.category,
      title: form.title,
      date: formatDate(data.created_at),
      views: 0,
      commentCount: 0,
      placeContentId: form.placeContentId || null,
      placeTitle: form.placeTitle || null,
      placeContentTypeId: form.placeContentTypeId || null,
      ...overlay[data.id]
    })
  }

  const updatePost = async (form) => {
    const { data } = await client.put(`/posts/${form.id}`, {
      title: form.title,
      content: form.content,
      category: form.category,
      password: form.password,
      place_content_id: form.placeContentId || undefined
    })

    const overlay = loadOverlay()
    overlay[form.id] = {
      ...getOverlayFor(overlay, form.id),
      tags: form.tagsRaw.split(',').map((t) => t.trim()).filter(Boolean),
      image: form.image
    }
    saveOverlay(overlay)

    updatePostInList(form.id, {
      category: data.category,
      title: data.title,
      tags: overlay[form.id].tags,
      image: overlay[form.id].image,
      placeContentId: data.place_content_id,
      placeTitle: data.place_title,
      placeContentTypeId: data.place_content_type_id
    })
  }

  const verifyPassword = async (id, password) => {
    await client.post(`/posts/${id}/verify-password`, { password })
  }

  const deletePost = async (id, password) => {
    await client.delete(`/posts/${id}`, { data: { password } })

    const overlay = loadOverlay()
    delete overlay[id]
    saveOverlay(overlay)

    posts.value = posts.value.filter((p) => p.id !== id)
  }

  const likePost = (id) => {
    const overlay = loadOverlay()
    const ov = getOverlayFor(overlay, id)
    ov.likes += 1
    overlay[id] = ov
    saveOverlay(overlay)
    updatePostInList(id, { likes: ov.likes })
  }

  const toggleBookmark = (id) => {
    const overlay = loadOverlay()
    const ov = getOverlayFor(overlay, id)
    ov.bookmarked = !ov.bookmarked
    overlay[id] = ov
    saveOverlay(overlay)
    updatePostInList(id, { bookmarked: ov.bookmarked })
  }

  return {
    posts,
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
  }
}
