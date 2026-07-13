<template>
  <main>
    <h1>글쓰기</h1>
    <form @submit.prevent="submit">
      <input v-model="title" placeholder="제목" required />
      <textarea v-model="content" placeholder="내용" required></textarea>
      <input v-model="password" type="password" placeholder="수정/삭제용 비밀번호" required />
      <button type="submit">등록</button>
    </form>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import client from "../api/client";

const router = useRouter();
const title = ref("");
const content = ref("");
const password = ref("");

async function submit() {
  const { data } = await client.post("/posts", {
    title: title.value,
    content: content.value,
    password: password.value,
  });
  router.push(`/community/${data.id}`);
}
</script>
