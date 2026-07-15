import { ref, nextTick } from 'vue'
import client from '../api/client'

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
        const { data } = await client.post('/chat', { message: userPrompt })
        if (data.answer) return data.answer
        throw new Error('Null answer content')
      } catch (e) {
        if (e?.response?.status === 429 && attempt < 2) {
          await new Promise((resolve) => setTimeout(resolve, delay))
          delay *= 2
          continue
        }
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
