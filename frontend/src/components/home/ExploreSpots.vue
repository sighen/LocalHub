<script setup>
import { exploreCategories } from '../../data/mockData'

const emit = defineEmits(['open-explore-tag'])
</script>

<template>
  <section class="bg-gradient-to-b from-white to-sky-50/50 py-16 border-t border-b border-slate-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-10">
      <div class="text-center space-y-2">
        <span class="text-xs font-extrabold text-blue-600 uppercase tracking-widest">서울 명소 99곳 & 추천 코스 다채롭게 만나기</span>
        <h2 class="text-3xl font-black text-slate-900 tracking-tight">서울 탐험하기</h2>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="category in exploreCategories"
          :key="category.id"
          @click="emit('open-explore-tag', category.code)"
          class="group bg-white rounded-2xl border border-slate-100 overflow-hidden hover:shadow-lg hover:border-blue-100 transition duration-300 cursor-pointer"
        >
          <div class="h-44 bg-slate-100 overflow-hidden relative">
            <img :src="category.img" :alt="category.title" class="w-full h-full object-cover group-hover:scale-105 transition-all duration-500" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition duration-300 flex items-end p-4">
              <span class="text-white text-xs font-bold"><i class="fa-solid fa-tags mr-1 text-red-500"></i> 관광지 추천에서 모아보기</span>
            </div>
          </div>
          <div class="p-5 space-y-2">
            <h3 class="text-base font-extrabold text-slate-800 group-hover:text-blue-600 transition">{{ category.title }}</h3>
            <p class="text-xs text-slate-500 leading-relaxed line-clamp-2">{{ category.desc }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
