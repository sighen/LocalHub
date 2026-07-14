import axios from 'axios'

// .env 에 VITE_API_BASE_URL=http://localhost:8000/api 형태로 설정
// (배포 시에는 Render 백엔드 주소로 교체)
const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'

const client = axios.create({
  baseURL,
  timeout: 8000,
})

export default client