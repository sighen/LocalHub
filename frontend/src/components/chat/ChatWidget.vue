<script setup>
import { useChat } from '../../composables/useChat'

const {
  isChatOpen,
  chatInput,
  chatHistory,
  isChatLoading,
  chatScrollContainer,
  handleChatSubmit,
  sendQuickQuery,
  formatChatText
} = useChat()
</script>

<template>
  <div class="fixed bottom-6 left-6 z-[9990] flex flex-col items-start gap-3">
    <div v-if="isChatOpen" class="w-[360px] h-[480px] bg-white rounded-3xl shadow-2xl border border-slate-100 flex flex-col overflow-hidden animate-fade-in">
      <div class="bg-gradient-to-tr from-slate-900 to-indigo-900 text-white p-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-indigo-500/20 text-indigo-300 rounded-xl flex items-center justify-center text-lg animate-pulse">
            <i class="fa-solid fa-robot"></i>
          </div>
          <div>
            <h4 class="text-xs font-black">서울 스마트 AI 가이드</h4>
            <p class="text-[10px] text-indigo-300 font-semibold"><span class="inline-block w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1"></span>실시간 검색 연동</p>
          </div>
        </div>
        <button @click="isChatOpen = false" class="text-indigo-200 hover:text-white transition"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <div ref="chatScrollContainer" class="flex-grow p-4 overflow-y-auto custom-scrollbar space-y-3 bg-slate-50 flex flex-col">
        <div
          v-for="(msg, idx) in chatHistory"
          :key="idx"
          :class="['max-w-[85%] p-3 rounded-2xl text-xs leading-relaxed shadow-sm', msg.role === 'user' ? 'self-end bg-blue-600 text-white' : 'self-start bg-white border border-slate-150 text-slate-700']"
        >
          <span v-html="formatChatText(msg.text)"></span>
        </div>
        <div v-if="isChatLoading" class="self-start px-3 py-2 bg-slate-100 rounded-xl text-[10px] text-slate-500 flex items-center gap-2 border">
          <i class="fa-solid fa-spinner animate-spin text-blue-600"></i> 서울 정보 검색중...
        </div>
      </div>

      <div class="p-3 border-t border-slate-100 flex gap-1.5 overflow-x-auto custom-scrollbar bg-white whitespace-nowrap">
        <button @click="sendQuickQuery('2026년 7월 서울에서 열리는 축제 추천해줘')" class="px-2.5 py-1 bg-slate-50 hover:bg-slate-100 text-[10px] text-slate-600 font-bold border rounded-full">🎉 7월 축제 목록</button>
        <button @click="sendQuickQuery('경복궁 입장료와 관람시간 알려줘')" class="px-2.5 py-1 bg-slate-50 hover:bg-slate-100 text-[10px] text-slate-600 font-bold border rounded-full">🏰 경복궁 정보</button>
        <button @click="sendQuickQuery('을지로 노포 삼겹살 맛집 추천해줘')" class="px-2.5 py-1 bg-slate-50 hover:bg-slate-100 text-[10px] text-slate-600 font-bold border rounded-full">😋 을지로 맛집</button>
      </div>

      <form @submit.prevent="handleChatSubmit" class="p-3 border-t border-slate-100 bg-white flex gap-2">
        <input type="text" v-model="chatInput" placeholder="서울 축제나 맛집 정보를 질문하세요..." class="flex-grow px-4 py-2.5 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white" />
        <button type="submit" class="px-4 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold transition"><i class="fa-solid fa-paper-plane"></i></button>
      </form>
    </div>

    <button @click="isChatOpen = !isChatOpen" class="w-14 h-14 bg-gradient-to-tr from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white rounded-full flex items-center justify-center text-xl shadow-xl shadow-indigo-500/20 transition duration-300 transform hover:scale-105">
      <i class="fa-solid fa-comments"></i>
      <span class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-[9px] font-black rounded-full flex items-center justify-center animate-bounce">1</span>
    </button>
  </div>
</template>
