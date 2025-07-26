<template>
  <div class="app-layout">
    <!-- Sidebar -->
    <Sidebar />
    
    <!-- Contenido Principal -->
    <main class="main-content" :class="{ 'main-content-collapsed': sidebarCollapsed }">
      <div class="content-wrapper">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from './Sidebar.vue'

// Usar el store de autenticación
const authStore = useAuthStore()
const router = useRouter()

// Estado del layout
const sidebarCollapsed = ref(false)

// Verificar autenticación al cargar el componente
onMounted(() => {
  // Si no hay token, redirigir al login
  if (!authStore.token) {
    router.push('/login')
    return
  }
  
  // Si está autenticado pero no tiene datos de usuario, intentar cargarlos
  if (!authStore.user) {
    authStore.fetchUserData().catch((error) => {
      console.error('Error al cargar los datos del usuario:', error)
      // Si hay un error al cargar los datos del usuario, hacer logout
      authStore.logout()
      router.push('/login')
    })
  }
})

// Observar cambios en la autenticación
watch(() => authStore.isAuthenticated, (isAuthenticated) => {
  if (!isAuthenticated) {
    router.push('/login')
  }
})

// Exponer el estado del sidebar para que pueda ser modificado desde los componentes hijos
defineExpose({
  toggleSidebar: () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
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
