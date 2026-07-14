<script setup>
const props = defineProps({
  filteredPosts: { type: Array, required: true },
  boardTagFilter: { type: String, required: true },
  filterBookmarkedOnly: { type: Boolean, required: true },
  searchQuery: { type: String, required: true }
})

const emit = defineEmits([
  'update:boardTagFilter',
  'update:filterBookmarkedOnly',
  'update:searchQuery',
  'open-create',
  'open-read',
  'like-post',
  'toggle-bookmark'
])
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8 animate-fade-in">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-6">
      <div>
        <h2 class="text-3xl font-black text-slate-900 tracking-tight">익명 자유 소통방</h2>
        <p class="text-sm text-slate-500 mt-1">로그인 없이 자유롭게 이야기를 공유하고 비밀번호를 등록해 수정/삭제하세요.</p>
      </div>
      <button @click="emit('open-create')" class="px-5 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-black shadow-lg shadow-blue-500/10 transition flex items-center gap-2">
        <i class="fa-solid fa-pen"></i> 글쓰기 등록
      </button>
    </div>

    <div class="bg-white border border-slate-100 rounded-3xl p-5 shadow-sm grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
      <div class="md:col-span-5 relative">
        <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 transform -translate-y-1/2 text-slate-400"></i>
        <input
          type="text"
          :value="searchQuery"
          @input="emit('update:searchQuery', $event.target.value)"
          placeholder="글 제목, 본문, 태그 검색..."
          class="w-full pl-10 pr-4 py-2.5 text-xs bg-slate-50 border border-slate-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition"
        />
      </div>

      <div class="md:col-span-5 flex flex-wrap gap-1.5">
        <button
          v-for="tagOpt in ['', '축제', '맛집', '여행정보']"
          :key="tagOpt || 'all'"
          @click="emit('update:boardTagFilter', tagOpt)"
          :class="['px-3 py-1.5 text-xs font-bold rounded-lg transition', boardTagFilter === tagOpt ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200']"
        >
          {{ tagOpt ? `#${tagOpt}` : '#전체' }}
        </button>
      </div>

      <div class="md:col-span-2 flex justify-end">
        <label class="flex items-center gap-2 cursor-pointer">
          <input
            type="checkbox"
            :checked="filterBookmarkedOnly"
            @change="emit('update:filterBookmarkedOnly', $event.target.checked)"
            class="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
          />
          <span class="text-xs font-bold text-slate-600">북마크만 보기</span>
        </label>
      </div>
    </div>

    <div class="bg-white border border-slate-100 rounded-3xl shadow-sm overflow-hidden">
      <div class="px-6 py-4 bg-slate-50 border-b border-slate-100 flex justify-between items-center text-xs text-slate-400 font-semibold">
        <span>총 {{ filteredPosts.length }}개의 주민 정보</span>
        <span>암호 기반 자율 수정·삭제 보장</span>
      </div>

      <div v-if="filteredPosts.length === 0" class="p-16 text-center text-slate-400 space-y-2">
        <i class="fa-regular fa-folder-open text-4xl block mb-2"></i>
        <p class="text-sm font-semibold">게시글이 존재하지 않습니다.</p>
        <p class="text-xs text-slate-300">첫 소식의 주인공이 되어보세요!</p>
      </div>

      <div v-else class="divide-y divide-slate-100">
        <div
          v-for="post in filteredPosts"
          :key="post.id"
          @click="emit('open-read', post)"
          class="p-6 hover:bg-slate-50/50 cursor-pointer transition flex flex-col sm:flex-row justify-between gap-4 items-start sm:items-center"
        >
          <div class="space-y-2 flex-grow">
            <div class="flex items-center gap-2 text-xs">
              <span class="px-2 py-0.5 bg-blue-50 text-blue-600 font-extrabold rounded">{{ post.category }}</span>
              <span class="text-slate-400">👤 익명인</span>
              <span class="text-slate-300">•</span>
              <span class="text-slate-400">{{ post.date }}</span>
            </div>
            <h3 class="text-base font-black text-slate-800 leading-snug hover:text-blue-600 transition truncate">{{ post.title }}</h3>
            <div class="flex gap-1 flex-wrap">
              <span v-for="tag in post.tags" :key="tag" class="text-[10px] bg-slate-100 text-slate-500 font-extrabold px-2 py-0.5 rounded">#{{ tag }}</span>
            </div>
          </div>

          <div @click.stop class="flex items-center gap-4 text-xs font-bold text-slate-400 shrink-0 self-end sm:self-center">
            <span><i class="fa-regular fa-eye mr-1"></i> {{ post.views }}</span>
            <button @click="emit('like-post', post.id)" class="hover:text-red-500 transition"><i class="fa-solid fa-heart mr-1 text-red-400"></i> {{ post.likes }}</button>
            <button
              @click="emit('toggle-bookmark', post.id)"
              :class="['p-1.5 bg-slate-50 hover:bg-slate-100 rounded-lg transition', post.bookmarked ? 'text-yellow-500' : 'text-slate-300']"
            >
              <i class="fa-solid fa-star"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
