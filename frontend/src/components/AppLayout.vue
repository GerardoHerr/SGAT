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
import { ref, computed, onMounted } from 'vue'
import Sidebar from './Sidebar.vue'
import { authService } from '@/services/authService.js'

// Estado global del usuario autenticado
const currentUser = ref(null)
const notifications = ref(5)
const sidebarCollapsed = ref(false)

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
