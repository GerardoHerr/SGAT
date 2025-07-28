<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <Sidebar @toggle="handleSidebarToggle" :user="currentUser" :notificationCount="notifications" />
    
    <!-- Contenido principal -->
    <main class="main-content" :class="{ 'main-content-collapsed': isCollapsed }">
      <div class="content-wrapper">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Sidebar from './Sidebar.vue'
import { authService } from '@/services/authService.js'

// Estado global del usuario autenticado
const currentUser = ref(null)
const notifications = ref(5)
const isCollapsed = ref(false)

const handleSidebarToggle = (collapsed) => {
  isCollapsed.value = collapsed
}

// Cargar usuario al montar el componente
onMounted(() => {
  const user = authService.getCurrentUser()
  if (user) {
    currentUser.value = {
      name: `${user.nombre} ${user.apellido}`,
      role: user.rol === 'ADM' ? 'Administrador' : 
            user.rol === 'DOC' ? 'Docente' : 
            user.rol === 'EST' ? 'Estudiante' : 'Docente',
      email: user.email,
      avatar: null
    }
  } else {
    // Usuario por defecto si no hay autenticación
    currentUser.value = {
      name: 'Usuario Demo',
      role: 'Docente',
      email: 'demo@universidad.edu',
      avatar: null
    }
  }
})
</script>

<style scoped>
.app-layout {
  display: flex;
  width: 100vw;
  height: 100vh;
  min-height: 100%;
  background-color: #ffffff;
  position: relative;
  overflow: hidden;
}

.main-content {
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  transition: all 0.3s ease;
  background-color: #ffffff;
  position: relative;
  flex: 1;
  margin-left: 280px;
  width: calc(100vw - 280px);
  display: flex;
  flex-direction: column;
}

.main-content-collapsed {
  margin-left: 20px;
  width: calc(100vw - 20px);
}

.content-wrapper {
  flex: 1;
  padding: 4rem;
  padding-right: 13rem;
  width: 100%;
  max-width: 100%; /* Ancho máximo del contenido */
  margin: 0 auto; /* Centra el contenido */
  box-sizing: border-box;
  overflow-x: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center; /* Centra los elementos horizontalmente */
}

/* Asegurar que el contenido no se desborde en móviles */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0 !important;
    width: 100% !important;
  }
  
  .main-content-collapsed {
    margin-left: 0 !important;
    width: 100% !important;
  }
}
</style>
