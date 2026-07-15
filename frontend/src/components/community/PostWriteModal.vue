<script setup>
import { ref, watch } from 'vue'
import client from '../../api/client'

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

// 관광지/문화시설/레포츠/축제·행사를 한 번에 검색해서 리뷰 대상 장소를 고를 수 있게 한다.
const PLACE_CATEGORY_LABEL = { 12: '관광지', 14: '문화시설', 28: '레포츠', 15: '축제·행사' }
const LOCATION_TYPES = ['관광지', '문화시설', '레포츠']

const placeSearchKeyword = ref('')
const placeSearchResults = ref([])
const isPlaceSearching = ref(false)
const placeSearchError = ref(false)

const clearLinkedPlace = () => {
  form.value.placeContentId = null
  form.value.placeTitle = ''
  form.value.placeContentTypeId = null
}

const searchPlaces = async (keyword) => {
  isPlaceSearching.value = true
  placeSearchError.value = false
  try {
    const [locationLists, festivalList] = await Promise.all([
      Promise.all(
        LOCATION_TYPES.map((type) =>
          client.get('/locations', { params: { q: keyword, type, size: 5 } }).then((r) => r.data.items)
        )
      ),
      client.get('/festivals', { params: { q: keyword, size: 5 } }).then((r) => r.data.items)
    ])
    placeSearchResults.value = [...locationLists.flat(), ...festivalList]
  } catch (e) {
    placeSearchError.value = true
    placeSearchResults.value = []
  } finally {
    isPlaceSearching.value = false
  }
}

let searchDebounceId = null
watch(placeSearchKeyword, (keyword) => {
  clearTimeout(searchDebounceId)
  const trimmed = keyword.trim()
  if (!trimmed) {
    placeSearchResults.value = []
    isPlaceSearching.value = false
    return
  }
  searchDebounceId = setTimeout(() => searchPlaces(trimmed), 300)
})

const selectPlace = (item) => {
  form.value.placeContentId = item.content_id
  form.value.placeTitle = item.title
  form.value.placeContentTypeId = item.content_type_id
  placeSearchKeyword.value = ''
  placeSearchResults.value = []
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
          <button type="button" @click="clearLinkedPlace" class="text-[10px] font-bold text-blue-400 hover:text-blue-600">
            연결 해제
          </button>
        </div>

        <div v-else class="space-y-1.5 relative">
          <label class="block text-xs font-bold text-slate-600 mb-1">관광지·행사 검색해서 리뷰 연결하기 (선택)</label>
          <div class="relative">
            <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-300 text-xs"></i>
            <input
              type="text"
              v-model="placeSearchKeyword"
              placeholder="장소명, 축제명으로 검색"
              class="w-full pl-8 pr-3 py-2 text-xs bg-slate-50 border rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white"
            />
          </div>

          <div v-if="placeSearchKeyword.trim()" class="border border-slate-100 rounded-xl overflow-hidden max-h-56 overflow-y-auto shadow-sm">
            <div v-if="isPlaceSearching" class="px-3 py-4 text-center text-[11px] text-slate-400">검색 중입니다...</div>
            <div v-else-if="placeSearchError" class="px-3 py-4 text-center text-[11px] text-slate-400">검색에 실패했어요. 잠시 후 다시 시도해주세요.</div>
            <div v-else-if="placeSearchResults.length === 0" class="px-3 py-4 text-center text-[11px] text-slate-400">검색 결과가 없습니다.</div>
            <button
              v-else
              v-for="item in placeSearchResults"
              :key="`${item.content_type_id}-${item.content_id}`"
              type="button"
              @click="selectPlace(item)"
              class="w-full flex items-center justify-between gap-2 px-3 py-2 text-left hover:bg-slate-50 border-b border-slate-50 last:border-b-0"
            >
              <span class="text-xs font-semibold text-slate-700 truncate">{{ item.title }}</span>
              <span class="text-[10px] font-bold text-blue-500 bg-blue-50 px-1.5 py-0.5 rounded shrink-0">{{ PLACE_CATEGORY_LABEL[item.content_type_id] }}</span>
            </button>
          </div>
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
