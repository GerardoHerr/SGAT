<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <Sidebar :user="currentUser" :notificationCount="notifications" />
    
    <!-- Contenido Principal -->
    <main class="main-content" :class="{ 'main-content-collapsed': sidebarCollapsed }">
      <div class="content-wrapper">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Sidebar from './Sidebar.vue'

// Estado global (esto vendría de un store como Pinia)
const currentUser = ref({
  name: 'Carlos Mendoza',
  role: 'Estudiante', // Cambiar entre: 'Administrador', 'Docente', 'Estudiante'
  avatar: null
})

const notifications = ref(5)
const sidebarCollapsed = ref(false)
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f8fafc;
}

.main-content {
  flex: 1;
  margin-left: 280px;
  transition: margin-left 0.3s ease;
  min-height: 100vh;
}

.main-content-collapsed {
  margin-left: 70px;
}

.content-wrapper {
  padding: 2rem;
  max-width: 100%;
}

/* Responsive */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
  
  .main-content-collapsed {
    margin-left: 0;
  }
}
</style>
