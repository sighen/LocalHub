<script setup>
const form = defineModel({ required: true })

defineProps({
  error: { type: String, default: '' }
})

const emit = defineEmits(['close', 'submit'])

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (e) => {
    form.value.image = e.target.result
  }
  reader.readAsDataURL(file)
}
</script>

<template>
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4" @click.self="emit('close')">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-xl overflow-hidden animate-fade-in">
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
        <h3 class="text-base font-black text-slate-900">{{ form.id ? '익명 소식 수정하기' : '새로운 소식 등록하기' }}</h3>
        <button @click="emit('close')" class="p-1.5 text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <form @submit.prevent="emit('submit')" class="p-6 space-y-4">
        <div v-if="form.placeContentId" class="flex items-center justify-between gap-2 px-3 py-2 bg-blue-50 border border-blue-100 rounded-xl">
          <span class="text-xs font-bold text-blue-700"><i class="fa-solid fa-location-dot mr-1"></i>{{ form.placeTitle }}</span>
          <button
            type="button"
            @click="form.placeContentId = null; form.placeTitle = ''; form.placeContentTypeId = null"
            class="text-[10px] font-bold text-blue-400 hover:text-blue-600"
          >
            연결 해제
          </button>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-600 mb-1">카테고리</label>
          <select v-model="form.category" class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white">
            <option value="관광지">관광지 정보</option>
            <option value="맛집">맛집 추천</option>
            <option value="축제">축제 및 행사 소식</option>
            <option value="잡담">일상/잡담</option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-600 mb-1">제목</label>
          <input type="text" v-model="form.title" placeholder="제목을 입력하세요" class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white" required />
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-600 mb-1">본문 내용</label>
          <textarea v-model="form.content" rows="4" placeholder="익명으로 공유할 내용을 작성하세요..." class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white resize-none" required></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">수정/삭제 비밀번호</label>
            <input type="password" v-model="form.password" placeholder="비밀번호 설정" class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white" required />
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-600 mb-1">태그 (쉼표로 구분)</label>
            <input type="text" v-model="form.tagsRaw" placeholder="예: 맛집, 을지로, 삼겹살" class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white" />
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-600 mb-1">이미지 첨부 (시뮬레이션)</label>
          <input type="file" @change="handleImageUpload" class="block w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
          <div v-if="form.image" class="mt-2 relative w-24 h-24 border rounded-xl overflow-hidden">
            <img :src="form.image" alt="preview" class="w-full h-full object-cover" />
            <button type="button" @click="form.image = ''" class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 text-[10px]"><i class="fa-solid fa-trash"></i></button>
          </div>
        </div>

        <p v-if="error" class="text-[11px] text-red-500 font-bold">{{ error }}</p>

        <div class="px-4 py-2 bg-slate-50 border-t flex justify-end gap-2 -mx-6 -mb-6">
          <button type="button" @click="emit('close')" class="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl">취소</button>
          <button type="submit" class="px-4 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 rounded-xl">저장 완료</button>
        </div>
      </form>
    </div>
  </div>
</template>
