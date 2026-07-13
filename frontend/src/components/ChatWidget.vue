<template>
  <div class="chat-widget">
    <button class="chat-toggle" @click="open = !open">💬</button>

    <div v-if="open" class="chat-panel">
      <div class="chat-history">
        <div v-for="(m, i) in history" :key="i" :class="['msg', m.role]">
          {{ m.content }}
        </div>
      </div>
      <div class="chat-input">
        <input
          v-model="message"
          placeholder="궁금한 걸 물어보세요"
          @keyup.enter="send"
        />
        <button @click="send">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import client from "../api/client";

const open = ref(false);
const message = ref("");
const history = ref([]);

async function send() {
  if (!message.value.trim()) return;
  const userMessage = { role: "user", content: message.value };
  history.value.push(userMessage);
  message.value = "";

  const { data } = await client.post("/chat", {
    message: userMessage.content,
    history: history.value,
  });
  history.value.push({ role: "assistant", content: data.reply });
}
</script>

<style scoped>
.chat-widget {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
}
.chat-toggle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  font-size: 24px;
  cursor: pointer;
}
.chat-panel {
  position: fixed;
  right: 20px;
  bottom: 88px;
  width: 320px;
  max-width: 90vw;
  height: 420px;
  max-height: 70vh;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}
.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}
.msg.user {
  text-align: right;
}
.chat-input {
  display: flex;
  border-top: 1px solid #eee;
}
.chat-input input {
  flex: 1;
  border: none;
  padding: 12px;
}
</style>
