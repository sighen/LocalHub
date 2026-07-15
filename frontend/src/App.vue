<script setup>
import { ref, onMounted } from 'vue'
import NavBar from './components/layout/NavBar.vue'
import FooterBar from './components/layout/FooterBar.vue'
import HomeView from './components/home/HomeView.vue'
import CommunityView from './components/community/CommunityView.vue'
import ExploreView from './components/explore/ExploreView.vue'
import FestivalsView from './components/festivals/FestivalsView.vue'
import ToastAlert from './components/modals/ToastAlert.vue'
import ChatWidget from './components/chat/ChatWidget.vue'
import { useWeather } from './composables/useWeather'

const currentTab = ref('home')
const exploreCategory = ref('관광지')
const exploreTag = ref('')

const { fetchLiveWeather } = useWeather()

onMounted(() => {
  fetchLiveWeather()
})

const openExplore = (category) => {
  exploreCategory.value = category
  exploreTag.value = ''
  currentTab.value = 'explore'
}

const openExploreTag = (tag) => {
  exploreCategory.value = '관광지'
  exploreTag.value = tag
  currentTab.value = 'explore'
}
</script>

<template>
  <div class="min-h-screen flex flex-col relative">
    <NavBar v-model:current-tab="currentTab" />

    <main class="flex-grow">
      <HomeView
        v-if="currentTab === 'home'"
        @go-community="currentTab = 'community'"
        @open-calendar="currentTab = 'festivals'"
        @open-explore="openExplore"
        @open-explore-tag="openExploreTag"
      />
      <CommunityView v-else-if="currentTab === 'community'" />
      <ExploreView v-else-if="currentTab === 'explore'" :initial-category="exploreCategory" :initial-tag="exploreTag" />
      <FestivalsView v-else />
    </main>

    <ChatWidget />
    <ToastAlert />

    <FooterBar />
  </div>
</template>
