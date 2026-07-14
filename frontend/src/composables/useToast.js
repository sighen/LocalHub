import { reactive } from 'vue'

// 여러 컴포넌트에서 공유해야 하므로 모듈 스코프에서 하나의 상태만 생성합니다 (싱글턴 패턴).
const customAlert = reactive({
  show: false,
  message: ''
})

export function useToast() {
  const showToast = (msg) => {
    customAlert.message = msg
    customAlert.show = true
  }

  const closeToast = () => {
    customAlert.show = false
  }

  return { customAlert, showToast, closeToast }
}
