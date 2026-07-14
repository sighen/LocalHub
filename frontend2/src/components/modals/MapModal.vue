<script setup>
const emit = defineEmits(['close'])
</script>

<template>
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-3xl overflow-hidden animate-fade-in">
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
        <h3 class="text-base font-black text-slate-900">📍 서울 관광 / 맛집 지도 시각화</h3>
        <button @click="emit('close')" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
      </div>
      <div class="p-6 space-y-4">
        <div id="leaflet-modal-map" class="w-full h-96 rounded-2xl border border-slate-200 shadow-inner overflow-hidden relative z-10 bg-slate-100"></div>
        <div class="flex flex-wrap gap-2 text-xs font-semibold">
          <span class="px-2 py-1 bg-red-100 text-red-700 rounded-lg">#지도 핀 연동</span>
          <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded-lg">#Leaflet.js 시각화</span>
          <span class="px-2 py-1 bg-emerald-100 text-emerald-700 rounded-lg">#공공데이터 좌표 매핑</span>
        </div>
      </div>
    </div>
  </div>
</template>
