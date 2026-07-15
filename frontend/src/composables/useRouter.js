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

  return { path, query, segments, navigate }
}
