<script setup>
import { useToast } from '../../composables/useToast'

const { showToast } = useToast()

const openHallyuGuide = () => {
  showToast('K-콘텐츠 속 서울 여행지 순례 도보 코스로 바로 연결됩니다.')
}
</script>

<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="bg-gradient-to-r from-emerald-800 to-teal-900 text-white rounded-3xl p-8 sm:p-12 relative overflow-hidden shadow-xl shadow-emerald-950/10 flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="relative z-10 space-y-3 max-w-xl text-center md:text-left">
        <span class="px-3 py-1 bg-white/20 text-emerald-200 rounded-full text-[10px] font-black border border-white/20 uppercase tracking-widest">K-spot</span>
        <h3 class="text-2xl sm:text-3xl font-black tracking-tight text-white leading-tight">
          K-콘텐츠 속 서울 여행지
        </h3>
        <p class="text-sm text-emerald-100 font-medium">
          한류 드라마와 시네마, 세계적으로 열광하는 영상 콘텐츠 배경 속 그 장소들을 테마별 도보관광 가이드로 추적해보세요.
        </p>
      </div>
      <button @click="openHallyuGuide" class="relative z-10 px-6 py-3.5 bg-white text-emerald-800 font-bold rounded-2xl text-xs shadow-md shadow-black/10 hover:bg-slate-50 transition shrink-0 transform hover:scale-102">
        한류 가이드 바로가기 <i class="fa-solid fa-arrow-right ml-1"></i>
      </button>
      <div class="absolute -right-10 -bottom-10 text-9xl text-white/5 pointer-events-none font-black"><i class="fa-solid fa-film"></i></div>
    </div>
  </section>
</template>
