<script setup lang="ts">
import Console from './components/WSChat.vue'
</script>

<template>
  <Console wsServer="ws://localhost:8765"></Console>
</template>

<style scoped>
#Console {
  width: 30vw;
  height: 80vh;
  margin: auto;
}
</style>
