import { ref, computed } from 'vue'

// 탭 간 딥링크(장소 상세 ↔ 커뮤니티) 상태 공유용 싱글턴.
// vue-router가 없는 탭 전환 구조라, 다른 탭으로 넘어가면서 "무엇을 보여줄지"를
// 전달하는 용도로만 쓴다. 소비하는 쪽(App.vue/CommunityView/ExploreView/FestivalsView)이
// onMounted 시점에 꺼내 쓰고 즉시 비운다.
const requestedTab = ref(null)
const pendingCommunityIntent = ref(null)
const pendingPlaceIntent = ref(null)

// 사이트 전역 "뒤로가기" 히스토리. 탭 전환이나 상세뷰/모달 오픈처럼
// 화면이 바뀌는 시점마다 이전 상태로 되돌리는 함수를 쌓아두고,
// 뒤로가기 버튼은 이 스택의 맨 위 함수만 꺼내 실행한다.
const backStack = ref([])
let backIdSeq = 0

const CONTENT_TYPE_TAB = {
  12: 'explore',
  14: 'explore',
  28: 'explore',
  15: 'festivals'
}

const CONTENT_TYPE_CATEGORY = {
  12: '관광지',
  14: '문화시설',
  28: '레포츠'
}

export function useAppNavigation() {
  const goToTab = (tab) => {
    requestedTab.value = tab
  }

  const consumeRequestedTab = () => {
    const tab = requestedTab.value
    requestedTab.value = null
    return tab
  }

  const requestWriteReview = (place) => {
    pendingCommunityIntent.value = {
      type: 'write',
      placeContentId: place.content_id,
      placeTitle: place.title,
      placeContentTypeId: place.content_type_id
    }
    goToTab('community')
  }

  const requestViewReviews = (place) => {
    pendingCommunityIntent.value = {
      type: 'view-reviews',
      placeContentId: place.content_id,
      placeTitle: place.title
    }
    goToTab('community')
  }

  const consumeCommunityIntent = () => {
    const intent = pendingCommunityIntent.value
    pendingCommunityIntent.value = null
    return intent
  }

  const goToPlace = (contentId, contentTypeId) => {
    const tab = CONTENT_TYPE_TAB[contentTypeId]
    if (!tab) return
    pendingPlaceIntent.value = { contentId, contentTypeId, category: CONTENT_TYPE_CATEGORY[contentTypeId] }
    goToTab(tab)
  }

  const consumePlaceIntent = () => {
    const intent = pendingPlaceIntent.value
    pendingPlaceIntent.value = null
    return intent
  }

  // pushBack: 화면 전환 시점에 "되돌리는 함수"를 스택에 쌓고 id를 돌려준다.
  // 뒤로가기 버튼이 아니라 화면 자체의 닫기/목록 버튼으로 되돌아간 경우에는
  // popBack(id)로 스택에서 제거해서, 나중에 뒤로가기를 눌렀을 때 이미 닫힌
  // 화면을 다시 닫으려는 헛동작(빈 클릭)이 생기지 않게 한다.
  const pushBack = (restoreFn) => {
    const id = ++backIdSeq
    backStack.value.push({ id, restoreFn })
    return id
  }

  const popBack = (id) => {
    const idx = backStack.value.findIndex((entry) => entry.id === id)
    if (idx !== -1) backStack.value.splice(idx, 1)
  }

  const goBack = () => {
    const entry = backStack.value.pop()
    if (entry) entry.restoreFn()
  }

  const canGoBack = computed(() => backStack.value.length > 0)

  return {
    requestedTab,
    goToTab,
    consumeRequestedTab,
    requestWriteReview,
    requestViewReviews,
    consumeCommunityIntent,
    goToPlace,
    consumePlaceIntent,
    pushBack,
    popBack,
    goBack,
    canGoBack
  }
}
