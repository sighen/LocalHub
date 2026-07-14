<script setup>
import HeroSlider from './HeroSlider.vue'
import UpcomingEvents from './UpcomingEvents.vue'
import ExploreSpots from './ExploreSpots.vue'
import EditorCourses from './EditorCourses.vue'
import HallyuBanner from './HallyuBanner.vue'
import TravelInfoLinks from './TravelInfoLinks.vue'
import SnsFeeds from './SnsFeeds.vue'

const emit = defineEmits(['go-community', 'open-calendar', 'open-location'])

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="space-y-16 animate-fade-in">
    <HeroSlider @scroll-to-upcoming="scrollToSection('upcoming-section')" @go-community="emit('go-community')" />
    <UpcomingEvents @open-calendar="emit('open-calendar')" />
    <ExploreSpots @open-location="(spot) => emit('open-location', spot)" />
    <EditorCourses />
    <HallyuBanner />
    <TravelInfoLinks />
    <SnsFeeds />
  </div>
</template>
