import { useRouter } from './useRouter'

// 탭 간 딥링크(장소 상세 ↔ 커뮤니티) 이동을 실제 브라우저 URL 이동으로 처리하는
// 헬퍼 모음. 각 화면(App.vue/CommunityView/ExploreView/FestivalsView)은 이
// 함수들이 만든 URL을 자신의 라우트 상태(useRouter의 segments/query)로 읽어서
// 반응적으로 화면을 구성한다.
const CONTENT_TYPE_TAB = {
  12: 'explore',
  14: 'explore',
  28: 'explore',
  15: 'festivals'
}

export function useAppNavigation() {
  const { navigate } = useRouter()

  const requestWriteReview = (place) => {
    const params = new URLSearchParams({
      placeId: place.content_id,
      placeType: place.content_type_id,
      placeTitle: place.title
    })
    navigate(`/community/write?${params.toString()}`)
  }

  const requestViewReviews = (place) => {
    const params = new URLSearchParams({
      place: place.content_id,
      placeTitle: place.title
    })
    navigate(`/community?${params.toString()}`)
  }

  const goToPlace = (contentId, contentTypeId) => {
    const tab = CONTENT_TYPE_TAB[contentTypeId]
    if (!tab) return
    navigate(`/${tab}/${contentId}`)
  }

  return {
    requestWriteReview,
    requestViewReviews,
    goToPlace
  }
}
