import { ref } from 'vue'

// 탭 간 딥링크(장소 상세 ↔ 커뮤니티) 상태 공유용 싱글턴.
// vue-router가 없는 탭 전환 구조라, 다른 탭으로 넘어가면서 "무엇을 보여줄지"를
// 전달하는 용도로만 쓴다. 소비하는 쪽(App.vue/CommunityView/ExploreView/FestivalsView)이
// onMounted 시점에 꺼내 쓰고 즉시 비운다.
const requestedTab = ref(null)
const pendingCommunityIntent = ref(null)
const pendingPlaceIntent = ref(null)

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

  return {
    requestedTab,
    goToTab,
    consumeRequestedTab,
    requestWriteReview,
    requestViewReviews,
    consumeCommunityIntent,
    goToPlace,
    consumePlaceIntent
  }
}
