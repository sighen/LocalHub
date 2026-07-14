// TourAPI 신분류체계(lclsSystm1) 코드 → 한글 라벨. 공식 코드표가 없어 실제 데이터 샘플로 추정한 값이며
// VE는 정확한 공식 명칭을 확인하지 못해 가장 근접한 표현으로 표기함.
export const TAG_LABELS = {
  NA: '자연',
  HS: '역사·인문',
  EX: '체험',
  VE: '여가·공원/거리',
  EV: '축제·행사',
  AC: '캠핑',
  LS: '스포츠·레저시설'
}

export const tagLabel = (code) => TAG_LABELS[code] || code
