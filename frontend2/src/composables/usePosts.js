import { ref, computed } from 'vue'
import { defaultPosts } from '../data/mockData'

const STORAGE_KEY = 'visit_seoul_posts'

export function usePosts() {
  const posts = ref([])
  const boardTagFilter = ref('')
  const filterBookmarkedOnly = ref(false)
  const searchQuery = ref('')

  const loadPosts = () => {
    const local = localStorage.getItem(STORAGE_KEY)
    if (local) {
      posts.value = JSON.parse(local)
    } else {
      posts.value = defaultPosts
      localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultPosts))
    }
  }

  const savePosts = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(posts.value))
  }

  const filteredPosts = computed(() =>
    posts.value.filter((p) => {
      const matchesTag = !boardTagFilter.value || p.tags.includes(boardTagFilter.value)
      const matchesBookmark = !filterBookmarkedOnly.value || p.bookmarked
      const query = searchQuery.value.toLowerCase()
      const matchesSearch =
        !query || p.title.toLowerCase().includes(query) || p.content.toLowerCase().includes(query)
      return matchesTag && matchesBookmark && matchesSearch
    })
  )

  const incrementViews = (post) => {
    post.views += 1
    savePosts()
  }

  const upsertPost = (form) => {
    if (form.id) {
      const idx = posts.value.findIndex((p) => p.id === form.id)
      if (idx !== -1) {
        posts.value[idx] = {
          ...posts.value[idx],
          category: form.category,
          title: form.title,
          content: form.content,
          tags: form.tagsRaw.split(',').map((t) => t.trim()).filter(Boolean),
          image: form.image
        }
      }
    } else {
      const newPost = {
        id: `post-${Date.now()}`,
        category: form.category,
        title: form.title,
        content: form.content,
        password: form.password,
        date: new Date()
          .toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' })
          .replace(/ /g, '')
          .slice(0, -1),
        views: 0,
        likes: 0,
        bookmarked: false,
        tags: form.tagsRaw.split(',').map((t) => t.trim()).filter(Boolean),
        image: form.image
      }
      posts.value.unshift(newPost)
    }
    savePosts()
  }

  const deletePost = (id) => {
    posts.value = posts.value.filter((p) => p.id !== id)
    savePosts()
  }

  const likePost = (id) => {
    const post = posts.value.find((p) => p.id === id)
    if (post) {
      post.likes += 1
      savePosts()
    }
  }

  const toggleBookmark = (id) => {
    const post = posts.value.find((p) => p.id === id)
    if (post) {
      post.bookmarked = !post.bookmarked
      savePosts()
    }
  }

  return {
    posts,
    boardTagFilter,
    filterBookmarkedOnly,
    searchQuery,
    filteredPosts,
    loadPosts,
    savePosts,
    incrementViews,
    upsertPost,
    deletePost,
    likePost,
    toggleBookmark
  }
}
