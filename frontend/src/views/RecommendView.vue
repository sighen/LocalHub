<template>
  <main>
    <h1>관광지 · 레포츠 · 문화시설 · 쇼핑</h1>

    <div class="filters">
      <select v-model="category">
        <option value="">전체</option>
        <option value="관광지">관광지</option>
        <option value="문화시설">문화시설</option>
        <option value="레포츠">레포츠</option>
        <option value="쇼핑">쇼핑</option>
        <option value="음식">음식</option>
      </select>
      <input v-model="keyword" placeholder="검색어" @keyup.enter="fetchLocations" />
      <button @click="fetchLocations">검색</button>
    </div>

    <ul class="location-list">
      <li v-for="loc in locations" :key="loc.content_id">
        <img v-if="loc.image" :src="loc.image" :alt="loc.title" />
        <div>
          <strong>{{ loc.title }}</strong>
          <p>{{ loc.address }}</p>
        </div>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import client from "../api/client";

const locations = ref([]);
const category = ref("");
const keyword = ref("");

async function fetchLocations() {
  const { data } = await client.get("/locations", {
    params: { category: category.value || undefined, keyword: keyword.value || undefined },
  });
  locations.value = data;
}

onMounted(fetchLocations);
</script>
