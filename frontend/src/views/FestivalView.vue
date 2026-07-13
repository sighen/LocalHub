<template>
  <main>
    <h1>축제 · 공연 · 행사</h1>
    <!-- TODO: 캘린더 뷰(선택기능)로 확장 가능, 우선 리스트로 시작 -->
    <ul>
      <li v-for="f in festivals" :key="f.content_id">
        <strong>{{ f.title }}</strong>
        <span>{{ f.start_date }} ~ {{ f.end_date }}</span>
        <p>{{ f.summary }}</p>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import client from "../api/client";

const festivals = ref([]);

onMounted(async () => {
  const { data } = await client.get("/festivals");
  festivals.value = data;
});
</script>
