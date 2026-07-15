<script setup>
import { snsFeeds } from '../../data/mockData'
</script>

<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8 pb-16">
    <div class="text-center space-y-2">
      <span class="text-xs font-extrabold text-blue-600 uppercase tracking-widest">Discover Now!</span>
      <h2 class="text-3xl font-black text-slate-900 tracking-tight">Youtube</h2>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <a
        v-for="sns in snsFeeds"
        :key="sns.id"
        :href="`https://www.youtube.com/watch?v=${sns.videoId}`"
        target="_blank"
        rel="noopener noreferrer"
        class="group bg-white rounded-2xl border border-slate-100 overflow-hidden hover:shadow-lg transition duration-150"
      >
        <div class="aspect-video bg-slate-100 relative overflow-hidden">
          <img :src="sns.img" :alt="sns.title" class="w-full h-full object-cover group-hover:scale-102 transition" />
          <div class="absolute inset-0 bg-black/20 flex items-center justify-center opacity-80 group-hover:opacity-100 transition">
            <span class="w-12 h-12 bg-white/20 hover:bg-white/35 backdrop-blur-md text-white border border-white/20 rounded-full flex items-center justify-center text-lg shadow-md transition duration-150"><i class="fa-solid fa-play"></i></span>
          </div>
        </div>
        <div class="p-5 space-y-1">
          <h3 class="text-sm font-bold text-slate-800 leading-snug line-clamp-1">{{ sns.title }}</h3>
          <span class="text-[10px] text-slate-400 font-semibold uppercase tracking-wider"><i class="fa-brands fa-youtube text-red-500 mr-1"></i> {{ sns.channel }}</span>
        </div>
      </a>
    </div>
  </section>
</template>
