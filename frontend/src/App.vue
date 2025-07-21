<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import AppLayout from './components/AppLayout.vue'

const route = useRoute()
const isLoginPage = computed(() => route.name === 'login-simple' || route.name === 'login')
</script>

<template>
  <RouterView v-if="isLoginPage" />
  <AppLayout v-else>
    <RouterView />
  </AppLayout>
</template>

<style>
/* Reset y estilos globales */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f8fafc;
  color: #334155;
  line-height: 1.6;
}

/* Variables CSS */
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --info-color: #3b82f6;
  --light-color: #f8fafc;
  --dark-color: #1e293b;
}
</style>
