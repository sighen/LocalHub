<script setup>
const pwVerifyInput = defineModel('pwVerifyInput', { required: true })

defineProps({
  pwError: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'confirm'])
</script>

<template>
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[99999] flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-xs overflow-hidden animate-fade-in">
      <div class="px-4 py-3 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
        <h4 class="text-xs font-black text-slate-900">비밀번호 확인</h4>
        <button @click="emit('close')" class="p-1.5 text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
      </div>
      <div class="p-4 space-y-3">
        <p class="text-[11px] text-slate-500 leading-relaxed">글 작성 시 등록했던 비밀번호를 입력하십시오.</p>
        <input
          type="password"
          v-model="pwVerifyInput"
          placeholder="비밀번호 입력"
          class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p v-if="pwError" class="text-[10px] text-red-500 font-bold">비밀번호가 일치하지 않습니다.</p>
      </div>
      <div class="px-4 py-2.5 bg-slate-50 border-t flex justify-end gap-2">
        <button @click="emit('close')" class="px-3 py-1.5 text-[10px] font-bold text-slate-600 hover:bg-slate-100 rounded-lg">취소</button>
        <button @click="emit('confirm')" class="px-3.5 py-1.5 text-[10px] font-bold text-white bg-blue-600 hover:bg-blue-500 rounded-lg">확인</button>
      </div>
    </div>
  </div>
</template>
