// 백엔드 이미지 URL이 http://로 내려오면 https 페이지에서 혼합 콘텐츠로 차단되어 렌더링되지 않는다.
export const secureImageUrl = (url) => (url ? url.replace(/^http:\/\//, 'https://') : url)
