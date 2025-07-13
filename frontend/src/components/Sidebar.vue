<template>
  <aside class="sidebar" :class="{ 'sidebar-collapsed': isCollapsed }">
    <!-- Header del Sidebar -->
    <div class="sidebar-header">
      <div class="logo-container">
        <img src="@/assets/logo.svg" alt="SGAT Logo" class="logo" />
        <h2 v-show="!isCollapsed" class="app-title">SGAT</h2>
      </div>
      <button @click="toggleSidebar" class="toggle-btn">
        <span class="toggle-icon">{{ isCollapsed ? '→' : '←' }}</span>
      </button>
    </div>

    <!-- Información del Usuario -->
    <div class="user-info" v-show="!isCollapsed">
      <div class="user-avatar">
        <span class="avatar-text">{{ userInitials }}</span>
      </div>
      <div class="user-details">
        <h4>{{ userName }}</h4>
        <span class="user-role">{{ userRole }}</span>
      </div>
    </div>

    <!-- Navegación Principal -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <!-- Dashboard -->
        <li class="nav-item">
          <RouterLink to="/" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
            <span class="nav-icon">📊</span>
            <span v-show="!isCollapsed" class="nav-text">Dashboard</span>
          </RouterLink>
        </li>

        <!-- Gestión de Tareas -->
        <li class="nav-item" v-if="canManageTasks">
          <div class="nav-section">
            <span v-show="!isCollapsed" class="section-title">Gestión de Tareas</span>
          </div>
          <ul class="nav-submenu">
            <li>
              <RouterLink to="/tareas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                <span class="nav-icon">📝</span>
                <span v-show="!isCollapsed" class="nav-text">Mis Tareas</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/asignar-tarea" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                <span class="nav-icon">➕</span>
                <span v-show="!isCollapsed" class="nav-text">Asignar Tarea</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/calificar" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                <span class="nav-icon">✅</span>
                <span v-show="!isCollapsed" class="nav-text">Calificar</span>
              </RouterLink>
            </li>
          </ul>
        </li>

        <!-- Gestión Académica -->
        <li class="nav-item" v-if="canManageAcademic">
          <div class="nav-section">
            <span v-show="!isCollapsed" class="section-title">Gestión Académica</span>
          </div>
          <ul class="nav-submenu">
            <li>
              <RouterLink to="/cursos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                <span class="nav-icon">📚</span>
                <span v-show="!isCollapsed" class="nav-text">Cursos</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/grupos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                <span class="nav-icon">👥</span>
                <span v-show="!isCollapsed" class="nav-text">Grupos</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/estudiantes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                <span class="nav-icon">🎓</span>
                <span v-show="!isCollapsed" class="nav-text">Estudiantes</span>
              </RouterLink>
            </li>
          </ul>
        </li>

        <!-- Reportes -->
        <li class="nav-item">
          <RouterLink to="/reportes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
            <span class="nav-icon">📈</span>
            <span v-show="!isCollapsed" class="nav-text">Reportes</span>
          </RouterLink>
        </li>

        <!-- Notificaciones -->
        <li class="nav-item">
          <RouterLink to="/notificaciones" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
            <span class="nav-icon">🔔</span>
            <span v-show="!isCollapsed" class="nav-text">Notificaciones</span>
            <span v-show="!isCollapsed && notificationCount > 0" class="notification-badge">{{ notificationCount }}</span>
          </RouterLink>
        </li>

        <!-- Configuración (Solo Admin) -->
        <li class="nav-item" v-if="isAdmin">
          <RouterLink to="/configuracion" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
            <span class="nav-icon">⚙️</span>
            <span v-show="!isCollapsed" class="nav-text">Configuración</span>
          </RouterLink>
        </li>
      </ul>
    </nav>

    <!-- Footer del Sidebar -->
    <div class="sidebar-footer">
      <button @click="logout" class="logout-btn" :class="{ 'logout-btn-collapsed': isCollapsed }">
        <span class="nav-icon">🚪</span>
        <span v-show="!isCollapsed" class="nav-text">Cerrar Sesión</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'

// Estado del sidebar
const isCollapsed = ref(false)

// Props (datos que vendrían del estado global/store)
const props = defineProps({
  user: {
    type: Object,
    default: () => ({
      name: 'Usuario Demo',
      role: 'Docente',
      avatar: null
    })
  },
  notificationCount: {
    type: Number,
    default: 3
  }
})

// Computed properties
const userName = computed(() => props.user.name)
const userRole = computed(() => props.user.role)
const userInitials = computed(() => {
  const names = props.user.name.split(' ')
  return names.map(name => name[0]).join('').toUpperCase()
})

const isAdmin = computed(() => props.user.role === 'Administrador')
const canManageTasks = computed(() => ['Docente', 'Administrador'].includes(props.user.role))
const canManageAcademic = computed(() => ['Docente', 'Administrador'].includes(props.user.role))

// Métodos
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const logout = () => {
  // Aquí iría la lógica de logout
  console.log('Cerrando sesión...')
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 280px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  z-index: 1000;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.sidebar-collapsed {
  width: 70px;
}

/* Header del Sidebar */
.sidebar-header {
  padding: 1.5rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  width: 35px;
  height: 35px;
  border-radius: 8px;
}

.app-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
  color: white;
}

.toggle-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Información del Usuario */
.user-info {
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 45px;
  height: 45px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.user-details h4 {
  margin: 0;
  font-size: 1rem;
}

.user-role {
  font-size: 0.85rem;
  opacity: 0.8;
}

/* Navegación */
.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
  overflow-y: auto;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 0.5rem;
}

.nav-section {
  padding: 0.75rem 1rem 0.5rem;
}

.section-title {
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  opacity: 0.7;
  letter-spacing: 1px;
}

.nav-submenu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  transition: all 0.2s;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border-right: 3px solid #ffd700;
}

.nav-link-collapsed {
  justify-content: center;
  gap: 0;
}

.nav-icon {
  font-size: 1.2rem;
  width: 20px;
  text-align: center;
}

.nav-text {
  font-size: 0.9rem;
}

.notification-badge {
  background: #ff4757;
  color: white;
  font-size: 0.7rem;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  margin-left: auto;
}

/* Footer del Sidebar */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-btn {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.logout-btn-collapsed {
  justify-content: center;
  gap: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar.sidebar-open {
    transform: translateX(0);
  }
}
</style>
