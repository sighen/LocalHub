<template>
  <main>
    <h1>커뮤니티</h1>
    <div class="toolbar">
      <input v-model="keyword" placeholder="검색" @keyup.enter="fetchPosts" />
      <router-link to="/community/write">글쓰기</router-link>
    </div>

    <table>
      <thead>
        <tr>
          <th>제목</th>
          <th>조회수</th>
          <th>댓글</th>
          <th>작성일</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="post in posts"
          :key="post.id"
          @click="$router.push(`/community/${post.id}`)"
        >
          <td>{{ post.title }}</td>
          <td>{{ post.view_count }}</td>
          <td>{{ post.comment_count }}</td>
          <td>{{ post.created_at }}</td>
        </tr>
      </tbody>
    </table>

    <!-- TODO: 페이지네이션 UI -->
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import client from "../api/client";

const posts = ref([]);
const keyword = ref("");

async function fetchPosts() {
  const { data } = await client.get("/posts", {
    params: { keyword: keyword.value || undefined },
  });
  posts.value = data.items;
}

onMounted(fetchPosts);
</script>
