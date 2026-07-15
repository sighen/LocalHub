<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { usePosts } from '../../composables/usePosts'

const emit = defineEmits(['go-community'])

const { posts, loadPosts, fetchPostDetail } = usePosts()

const topPosts = ref([])
const slideIndex = ref(0)
let autoSlideTimer = null

const loadTopPosts = async () => {
  await loadPosts()
  const ranked = [...posts.value].sort((a, b) => b.likes - a.likes || b.views - a.views || b.commentCount - a.commentCount).slice(0, 5)

  topPosts.value = await Promise.all(
    ranked.map(async (p) => {
      const detail = await fetchPostDetail(p.id)
      return { ...p, content: detail?.content || '' }
    })
  )
}

const prevSlide = () => {
  if (!topPosts.value.length) return
  slideIndex.value = (slideIndex.value - 1 + topPosts.value.length) % topPosts.value.length
}
const nextSlide = () => {
  if (!topPosts.value.length) return
  slideIndex.value = (slideIndex.value + 1) % topPosts.value.length
}

onMounted(async () => {
  await loadTopPosts()
  autoSlideTimer = setInterval(nextSlide, 5000)
})

onUnmounted(() => clearInterval(autoSlideTimer))
</script>

<template>
  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
    <div class="text-center space-y-2">
      <span class="text-xs font-extrabold text-blue-600 uppercase tracking-widest">네티즌이 서울에서 추천하는 이색적인 여정</span>
      <h2 class="text-3xl font-black text-slate-900 tracking-tight">인기 커뮤니티 후기</h2>
    </div>

    <div v-if="topPosts.length" class="bg-white border border-slate-100 rounded-3xl shadow-sm p-8 sm:p-10 space-y-6">
      <div class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest">
        <span class="px-2.5 py-1 bg-blue-50 text-blue-600 rounded-lg border border-blue-100">{{ topPosts[slideIndex].category }}</span>
        <span class="text-slate-300">·</span>
        <span class="text-slate-400 normal-case font-bold">
          <i class="fa-solid fa-heart text-rose-400"></i> {{ topPosts[slideIndex].likes }} · 조회 {{ topPosts[slideIndex].views }} · 댓글 {{ topPosts[slideIndex].commentCount }}
        </span>
      </div>
      <h3 class="text-xl sm:text-2xl font-black text-slate-900 leading-snug">{{ topPosts[slideIndex].title }}</h3>
      <p class="text-sm text-slate-500 leading-relaxed line-clamp-3">{{ topPosts[slideIndex].content }}</p>

      <div class="flex items-center justify-between pt-4 border-t border-slate-100">
        <button
          @click="emit('go-community')"
          class="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-bold transition"
        >
          커뮤니티에서 더 보기 <i class="fa-solid fa-arrow-right ml-1"></i>
        </button>

        <div class="flex items-center gap-4">
          <button @click="prevSlide" class="text-slate-300 hover:text-slate-600 transition text-xs"><i class="fa-solid fa-chevron-left"></i></button>
          <div class="flex gap-2">
            <span
              v-for="(p, idx) in topPosts"
              :key="p.id"
              @click="slideIndex = idx"
              :class="['w-2 h-2 rounded-full cursor-pointer transition-all duration-300', slideIndex === idx ? 'bg-blue-600 w-6' : 'bg-slate-200']"
            ></span>
          </div>
          <button @click="nextSlide" class="text-slate-300 hover:text-slate-600 transition text-xs"><i class="fa-solid fa-chevron-right"></i></button>
        </div>
      </div>
    </div>
  </section>
</template>
