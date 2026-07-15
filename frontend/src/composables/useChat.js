import { ref, nextTick } from 'vue'

/**
 * 원본 데모는 API 키가 런타임에 자동 주입되는 특수 샌드박스 환경(Google AI Studio 캔버스)을
 * 전제로 작성되었습니다. 실서비스에서는 API 키를 프론트엔드에 절대 노출하면 안 되므로,
 * 아래 fetch는 여러분의 백엔드(BFF) 프록시 엔드포인트를 호출하도록 구성하는 것을 권장합니다.
 *
 * 예) VITE_CHAT_API_URL=/api/chat  (백엔드에서 실제 LLM/OpenAPI 호출 + 키 관리)
 */
const CHAT_API_URL = import.meta.env.VITE_CHAT_API_URL || '/api/chat'

export function useChat() {
  const isChatOpen = ref(false)
  const chatInput = ref('')
  const chatHistory = ref([
    {
      role: 'bot',
      text: '안녕하세요! <strong>LocalHub 서울 AI 어시스턴트</strong>입니다. <br>축제 정보나 맛집 명소에 대해 궁금한 점을 실제로 검색하여 해결해 드립니다!'
    }
  ])
  const isChatLoading = ref(false)
  const chatScrollContainer = ref(null)

  const scrollToBottom = () => {
    nextTick(() => {
      if (chatScrollContainer.value) {
        chatScrollContainer.value.scrollTop = chatScrollContainer.value.scrollHeight
      }
    })
  }

  const formatChatText = (text) =>
    text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')

  const queryChatApi = async (userPrompt) => {
    let delay = 1000
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const res = await fetch(CHAT_API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userPrompt })
        })

        if (!res.ok) {
          if (res.status === 429) {
            await new Promise((resolve) => setTimeout(resolve, delay))
            delay *= 2
            continue
          }
          throw new Error('HTTP failure status: ' + res.status)
        }

        const data = await res.json()
        if (data.reply) return data.reply
        throw new Error('Null answer content')
      } catch (e) {
        if (attempt === 2) throw e
        await new Promise((resolve) => setTimeout(resolve, delay))
        delay *= 2
      }
    }
  }

  const handleChatSubmit = async () => {
    const text = chatInput.value.trim()
    if (!text) return

    chatHistory.value.push({ role: 'user', text })
    chatInput.value = ''
    isChatLoading.value = true
    scrollToBottom()

    try {
      const reply = await queryChatApi(text)
      chatHistory.value.push({ role: 'bot', text: reply })
    } catch (err) {
      chatHistory.value.push({
        role: 'bot',
        text: '죄송합니다. 실시간 데이터센터 연결이 원활하지 않습니다. 여름 대표 행사인 서울썸머비치는 7월 중순 광화문광장에서 정상 진행 예정입니다!'
      })
    } finally {
      isChatLoading.value = false
      scrollToBottom()
    }
  }

  const sendQuickQuery = (queryText) => {
    chatInput.value = queryText
    handleChatSubmit()
  }

  return {
    isChatOpen,
    chatInput,
    chatHistory,
    isChatLoading,
    chatScrollContainer,
    handleChatSubmit,
    sendQuickQuery,
    formatChatText
  }
}
