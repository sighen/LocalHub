<script setup>
import HeroSlider from './HeroSlider.vue'
import UpcomingEvents from './UpcomingEvents.vue'
import ExploreSpots from './ExploreSpots.vue'
import CommunityHighlights from './CommunityHighlights.vue'
import TravelInfoLinks from './TravelInfoLinks.vue'
import SnsFeeds from './SnsFeeds.vue'

const emit = defineEmits(['go-community', 'open-calendar', 'open-explore', 'open-explore-tag', 'open-weather-detail'])

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="space-y-16 animate-fade-in">
    <HeroSlider @scroll-to-upcoming="scrollToSection('upcoming-section')" @go-community="emit('go-community')" />
    <UpcomingEvents @open-calendar="emit('open-calendar')" />
    <ExploreSpots @open-explore-tag="(tag) => emit('open-explore-tag', tag)" />
    <CommunityHighlights @go-community="emit('go-community')" />
    <TravelInfoLinks
      @go-community="emit('go-community')"
      @open-calendar="emit('open-calendar')"
      @open-explore="(category) => emit('open-explore', category)"
      @open-weather-detail="emit('open-weather-detail')"
    />
    <SnsFeeds />
  </div>
</template>
