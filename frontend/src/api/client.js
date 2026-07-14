import axios from 'axios'

// Netlify 배포 시 환경변수 VITE_API_BASE_URL로 실제 Render 백엔드 주소 지정
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const client = axios.create({ baseURL })

export default client
