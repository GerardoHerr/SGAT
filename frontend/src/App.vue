<!-- filepath: c:\Users\Usuario iTC\Desktop\Procesos_Project\SGAT\frontend\src\App.vue -->
<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import AppLayout from './components/AppLayout.vue'

const route = useRoute()
const isLoginPage = computed(() => route.name === 'login')
const isRegisterPage = computed(() => route.name === 'registrarUsuario')
const isAuthPage = computed(() => isLoginPage.value || isRegisterPage.value)
</script>

<template>
  <!-- Solo mostrar navegación si no es la página de login -->
  <header v-if="!isLoginPage">
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/registrarUsuario">Registrar Usuario</RouterLink>
        <RouterLink to="/registrar-asignatura">Registrar Asignatura</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
      </nav>
    </div>
  </header>

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
  --warning-color: #f59e0b;
  --danger-color: #ef4444;
  --info-color: #3b82f6;
  --background-color: #f8fafc;
  --surface-color: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
  --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

/* Utilidades */

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.card {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: #5a67d8;
  transform: translateY(-1px);
}

.btn-secondary {
  background: var(--border-color);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background: #cbd5e1;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    padding: 0 0.5rem;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;
    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
