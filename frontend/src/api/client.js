import axios from 'axios'

// Netlify 배포 시 환경변수 VITE_API_BASE_URL로 실제 Render 백엔드 주소 지정
export const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// 배열 파라미터(district=강남구&district=마포구)를 axios 기본값인 district[]= 형태가 아니라
// FastAPI가 List[str]로 바로 받을 수 있는 형태로 직렬화한다.
const client = axios.create({ baseURL, paramsSerializer: { indexes: null } })

export default client
