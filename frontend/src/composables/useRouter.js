import { ref, computed } from 'vue'

// vue-router 없이 브라우저 주소창의 실제 URL/히스토리로 뒤로/앞으로가기가
// 동작하도록 하는 가벼운 싱글턴 라우터. pushState/replaceState로 URL을 바꾸고
// popstate(브라우저 뒤로/앞으로 버튼)를 들어서 상태를 동기화한다.
const state = ref(parseLocation())

function parseLocation() {
  return {
    path: window.location.pathname,
    query: new URLSearchParams(window.location.search)
  }
}

window.addEventListener('popstate', () => {
  state.value = parseLocation()
})

export function useRouter() {
  const path = computed(() => state.value.path)
  const query = computed(() => state.value.query)
  const segments = computed(() => path.value.split('/').filter(Boolean))

  const navigate = (to, { replace = false } = {}) => {
    if (replace) {
      window.history.replaceState(null, '', to)
    } else {
      window.history.pushState(null, '', to)
    }
    state.value = parseLocation()
  }

  // 실제 브라우저 뒤로가기와 동일하게 동작한다. "목록으로"/닫기 버튼처럼
  // 상세뷰를 벗어나는 동작에 쓰면, 다른 탭(예: 커뮤니티)에서 진입했을 때도
  // 항상 그 탭의 목록으로 되돌아가는 게 아니라 실제로 왔던 곳으로 돌아간다.
  const goBack = () => {
    window.history.back()
  }

  return { path, query, segments, navigate, goBack }
}
