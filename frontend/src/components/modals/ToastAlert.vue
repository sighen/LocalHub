<script setup>
import { useToast } from '../../composables/useToast'

const { customAlert, closeToast } = useToast()
</script>

<template>
  <div v-if="customAlert.show" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[999999] flex items-center justify-center p-4" @click.self="closeToast">
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden animate-fade-in border border-slate-100">
      <div class="p-6 space-y-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center text-lg">
            <i class="fa-solid fa-circle-info"></i>
          </div>
          <h4 class="text-sm font-black text-slate-900">안내 사항</h4>
        </div>
        <p class="text-xs text-slate-600 leading-relaxed">{{ customAlert.message }}</p>
        <div class="flex justify-end pt-2">
          <button @click="closeToast" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold rounded-xl transition">확인</button>
        </div>
      </div>
    </div>
  </div>
</template>
