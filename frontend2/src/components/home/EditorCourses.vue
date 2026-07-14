<script setup>
import { ref } from 'vue'
import { editorCourses } from '../../data/mockData'

const editorIndex = ref(0)

const prevEditor = () => {
  editorIndex.value = (editorIndex.value - 1 + editorCourses.length) % editorCourses.length
}
const nextEditor = () => {
  editorIndex.value = (editorIndex.value + 1) % editorCourses.length
}
</script>

<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
    <div class="text-center space-y-2">
      <span class="text-xs font-extrabold text-blue-600 uppercase tracking-widest">네티즌서울에서 추천하는 이색적인 여정</span>
      <h2 class="text-3xl font-black text-slate-900 tracking-tight">에디터 추천여행</h2>
    </div>

    <div class="relative overflow-hidden bg-white border border-slate-100 rounded-3xl p-8 shadow-sm">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <div class="lg:col-span-5 space-y-5">
          <span class="px-3 py-1 bg-amber-50 text-amber-700 border border-amber-100 rounded-full text-xs font-bold">인기 에디터 가이드</span>
          <h3 class="text-2xl font-black text-slate-900 leading-tight">
            {{ editorCourses[editorIndex].title }}
          </h3>
          <p class="text-sm text-slate-500 leading-relaxed">
            {{ editorCourses[editorIndex].desc }}
          </p>
          <div class="pt-4 border-t border-slate-100 flex items-center gap-4">
            <span class="text-xs font-bold text-slate-800">여행 시간: <strong class="text-slate-800">{{ editorCourses[editorIndex].duration }}</strong></span>
            <span class="text-xs font-bold text-slate-800">이동 수단: <strong class="text-slate-800">{{ editorCourses[editorIndex].transport }}</strong></span>
          </div>
          <div class="flex gap-2 pt-2">
            <button @click="prevEditor" class="p-2.5 bg-slate-50 hover:bg-slate-100 text-slate-600 rounded-xl text-xs transition border border-slate-100"><i class="fa-solid fa-chevron-left"></i></button>
            <button @click="nextEditor" class="p-2.5 bg-slate-50 hover:bg-slate-100 text-slate-600 rounded-xl text-xs transition border border-slate-100"><i class="fa-solid fa-chevron-right"></i></button>
          </div>
        </div>

        <div class="lg:col-span-7 h-80 bg-slate-100 rounded-2xl overflow-hidden relative group">
          <img :src="editorCourses[editorIndex].img" :alt="editorCourses[editorIndex].title" class="w-full h-full object-cover transition-all duration-1000" />
          <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent"></div>
          <div class="absolute bottom-4 left-4 text-white text-xs font-semibold backdrop-blur-md bg-black/30 px-3 py-1 rounded-full border border-white/10">
            📷 {{ editorCourses[editorIndex].location }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
