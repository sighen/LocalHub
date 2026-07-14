<script setup>
import { tagLabel } from '../../utils/tagLabels'

defineProps({
  tag: { type: String, required: true },
  sort: { type: String, required: true },
  facets: { type: Object, required: true }
})

const emit = defineEmits(['select-tag', 'select-sort'])
</script>

<template>
  <aside class="bg-white border border-slate-100 rounded-3xl shadow-sm p-5 space-y-6 h-fit">
    <div class="space-y-2.5">
      <h4 class="text-xs font-black text-slate-700">태그</h4>
      <div class="flex flex-wrap gap-1.5">
        <button
          @click="emit('select-tag', '')"
          :class="['px-2.5 py-1.5 text-[11px] font-bold rounded-lg transition', !tag ? 'bg-blue-600 text-white' : 'bg-blue-50 text-blue-600 hover:bg-blue-100']"
        >
          전체
        </button>
        <button
          v-for="t in facets.tags"
          :key="t.value"
          @click="emit('select-tag', t.value)"
          :class="['px-2.5 py-1.5 text-[11px] font-bold rounded-lg transition', tag === t.value ? 'bg-blue-600 text-white' : 'bg-blue-50 text-blue-600 hover:bg-blue-100']"
        >
          {{ tagLabel(t.value) }} <span class="opacity-60">{{ t.count }}</span>
        </button>
      </div>
    </div>

    <div class="space-y-2.5 border-t border-slate-100 pt-5">
      <h4 class="text-xs font-black text-slate-700">정렬</h4>
      <select
        :value="sort"
        @change="emit('select-sort', $event.target.value)"
        class="w-full px-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white"
      >
        <option value="title">가나다순</option>
        <option value="latest">최신 등록순</option>
      </select>
    </div>
  </aside>
</template>
