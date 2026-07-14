<script setup>
import { travelInfoLinks } from '../../data/mockData'
import { useToast } from '../../composables/useToast'

const { showToast } = useToast()

const handleInfoClick = (info) => {
  showToast(`"${info.title}" 가이드북 다운로드가 준비되었습니다. 공식 사이트 연동 규정을 확인해 주십시오.`)
}
</script>

<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
    <div class="text-center space-y-2">
      <span class="text-xs font-extrabold text-blue-600 uppercase tracking-widest">서울 여행의 기본 가이드를 한 곳에</span>
      <h2 class="text-3xl font-black text-slate-900 tracking-tight">서울 여행정보</h2>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-5 gap-4">
      <div
        v-for="info in travelInfoLinks"
        :key="info.id"
        @click="handleInfoClick(info)"
        class="bg-white border border-slate-100 rounded-2xl p-6 text-center hover:shadow-md hover:border-blue-200 transition duration-150 cursor-pointer group"
      >
        <div class="w-14 h-14 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center text-xl mx-auto mb-4 group-hover:scale-110 transition duration-150 shadow-sm">
          <i :class="info.icon"></i>
        </div>
        <h4 class="text-xs font-bold text-slate-800">{{ info.title }}</h4>
      </div>
    </div>
  </section>
</template>
