import { ref, nextTick } from 'vue'
import { baseURL } from '../api/client'

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

  // 초기 인삿말(HTML 고정 문구)과 지금 막 보낸 사용자 메시지를 뺀 이전
  // 대화만 히스토리로 보낸다. 너무 길어지지 않게 최근 12턴만 유지한다.
  const buildHistoryPayload = () =>
    chatHistory.value
      .slice(1, -1)
      .slice(-12)
      .map((m) => ({ role: m.role === 'user' ? 'user' : 'assistant', content: m.text.slice(0, 1000) }))

  // 백엔드가 text/event-stream(SSE)으로 답변을 토큰 단위로 흘려보낸다.
  // 검색 조건 추출 단계(첫 응답까지 시간이 걸림)가 끝나고 실제 답변 생성이
  // 시작되면 onChunk가 조금씩 불려서, 다 만들어질 때까지 기다리지 않고
  // 글자가 실제로 생성되는 속도 그대로 화면에 나타난다.
  const streamChatApi = async (userPrompt, history, onChunk) => {
    const res = await fetch(`${baseURL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userPrompt, history })
    })

    if (!res.ok || !res.body) {
      throw new Error('HTTP failure status: ' + res.status)
    }

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let sawChunk = false

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      buffer += decoder.decode(value, { stream: true })

      let sepIndex
      while ((sepIndex = buffer.indexOf('\n\n')) !== -1) {
        const frame = buffer.slice(0, sepIndex)
        buffer = buffer.slice(sepIndex + 2)
        const dataLine = frame.split('\n').find((line) => line.startsWith('data:'))
        if (!dataLine) continue

        const payload = JSON.parse(dataLine.slice(5).trim())
        if (payload.type === 'chunk' && payload.text) {
          sawChunk = true
          onChunk(payload.text)
        }
      }
    }

    if (!sawChunk) throw new Error('Empty stream')
  }

  const handleChatSubmit = async () => {
    const text = chatInput.value.trim()
    if (!text) return

    chatHistory.value.push({ role: 'user', text })
    const history = buildHistoryPayload()
    chatInput.value = ''
    isChatLoading.value = true
    scrollToBottom()

    // chatHistory.value.push(raw)로 넣은 뒤에도 raw 변수를 계속 들고 mutate하면
    // Vue의 reactive proxy를 거치지 않은 변경이라 화면이 갱신되지 않는다.
    // push 직후 배열에서 다시 읽어온(=proxy로 감싸진) 참조를 mutate해야 한다.
    let reactiveMessage = null
    let started = false

    try {
      await streamChatApi(text, history, (delta) => {
        if (!started) {
          started = true
          isChatLoading.value = false
          chatHistory.value.push({ role: 'bot', text: '' })
          reactiveMessage = chatHistory.value[chatHistory.value.length - 1]
        }
        reactiveMessage.text += delta
        scrollToBottom()
      })
    } catch (err) {
      if (!started) {
        chatHistory.value.push({ role: 'bot', text: '' })
        reactiveMessage = chatHistory.value[chatHistory.value.length - 1]
      }
      reactiveMessage.text =
        '죄송합니다. 실시간 데이터센터 연결이 원활하지 않습니다. 여름 대표 행사인 서울썸머비치는 7월 중순 광화문광장에서 정상 진행 예정입니다!'
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
