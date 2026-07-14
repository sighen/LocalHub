<script setup>
defineProps({
  post: { type: Object, required: true }
})

const emit = defineEmits(['close', 'like', 'toggle-bookmark', 'edit', 'delete'])
</script>

<template>
  <div class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[9999] flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl shadow-2xl w-full max-w-xl overflow-hidden animate-fade-in">
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center">
        <span class="px-2.5 py-1 bg-blue-50 text-blue-600 text-xs font-bold rounded-lg border border-blue-100">{{ post.category }}</span>
        <button @click="emit('close')" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <div class="p-6 space-y-5">
        <div class="space-y-1.5">
          <h3 class="text-xl font-black text-slate-900 leading-tight">{{ post.title }}</h3>
          <div class="flex items-center gap-3 text-xs text-slate-400">
            <span>👤 익명</span>
            <span>•</span>
            <span>{{ post.date }}</span>
            <span>•</span>
            <span>조회수 {{ post.views }}</span>
          </div>
        </div>

        <div class="border-t border-b border-slate-100 py-4">
          <div v-if="post.image" class="mb-4 rounded-xl overflow-hidden max-h-56 border border-slate-200">
            <img :src="post.image" alt="Uploaded post item" class="w-full h-full object-cover" />
          </div>
          <p class="text-xs text-slate-600 leading-relaxed whitespace-pre-line">{{ post.content }}</p>
        </div>

        <div class="flex flex-wrap gap-1">
          <span v-for="tag in post.tags" :key="tag" class="text-[10px] bg-slate-100 text-slate-500 font-extrabold px-2 py-0.5 rounded">#{{ tag }}</span>
        </div>

        <div class="flex items-center justify-between pt-2">
          <div class="flex gap-4 text-xs font-bold text-slate-400">
            <button @click="emit('like', post.id)" class="hover:text-red-500 transition"><i class="fa-regular fa-heart mr-1"></i> 좋아요 {{ post.likes }}</button>
            <button @click="emit('toggle-bookmark', post.id)" :class="['transition', post.bookmarked ? 'text-yellow-500' : 'hover:text-yellow-500']">
              <i class="fa-regular fa-star"></i> 북마크
            </button>
          </div>

          <div class="flex gap-2">
            <button @click="emit('edit')" class="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg transition">수정</button>
            <button @click="emit('delete')" class="px-3.5 py-1.5 bg-red-50 hover:bg-red-100 text-red-600 text-xs font-bold rounded-lg transition">삭제</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
