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
        <!-- Dashboard - Para todos los roles -->
        <li class="nav-item">
          <RouterLink to="/" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
            <span class="nav-icon">📊</span>
            <span v-show="!isCollapsed" class="nav-text">Dashboard</span>
          </RouterLink>
        </li>

        <!-- ADMINISTRADOR -->
        <template v-if="isAdmin">
          <li class="nav-item">
            <div class="nav-section">
              <span v-show="!isCollapsed" class="section-title">Administración</span>
            </div>
            <ul class="nav-submenu">
              <li>
                <RouterLink to="/usuarios" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">👤</span>
                  <span v-show="!isCollapsed" class="nav-text">Gestión Usuarios</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/periodos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">📅</span>
                  <span v-show="!isCollapsed" class="nav-text">Periodos Lectivos</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/asignaturas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">📖</span>
                  <span v-show="!isCollapsed" class="nav-text">Asignaturas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/configuracion" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">⚙️</span>
                  <span v-show="!isCollapsed" class="nav-text">Configuración</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </template>

        <!-- DOCENTE -->
        <template v-if="isDocente">
          <li class="nav-item">
            <div class="nav-section">
              <span v-show="!isCollapsed" class="section-title">Gestión de Tareas</span>
            </div>
            <ul class="nav-submenu">
              <li>
                <RouterLink to="/mis-tareas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
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
              <li>
                <RouterLink to="/retroalimentacion" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">💬</span>
                  <span v-show="!isCollapsed" class="nav-text">Retroalimentación</span>
                </RouterLink>
              </li>
            </ul>
          </li>
          
          <li class="nav-item">
            <div class="nav-section">
              <span v-show="!isCollapsed" class="section-title">Gestión Académica</span>
            </div>
            <ul class="nav-submenu">
              <li>
                <RouterLink to="/mis-cursos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">📚</span>
                  <span v-show="!isCollapsed" class="nav-text">Mis Cursos</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/grupos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">👥</span>
                  <span v-show="!isCollapsed" class="nav-text">Gestión Grupos</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiantes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">🎓</span>
                  <span v-show="!isCollapsed" class="nav-text">Mis Estudiantes</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </template>

        <!-- ESTUDIANTE -->
        <template v-if="isEstudiante">
          <li class="nav-item">
            <div class="nav-section">
              <span v-show="!isCollapsed" class="section-title">Mis Actividades</span>
            </div>
            <ul class="nav-submenu">
              <li>
                <RouterLink to="/tareas-asignadas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">�</span>
                  <span v-show="!isCollapsed" class="nav-text">Tareas Asignadas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/entregar-tarea" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">📤</span>
                  <span v-show="!isCollapsed" class="nav-text">Entregar Tarea</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/calendario" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">�</span>
                  <span v-show="!isCollapsed" class="nav-text">Calendario</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/historial" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">📜</span>
                  <span v-show="!isCollapsed" class="nav-text">Historial</span>
                </RouterLink>
              </li>
            </ul>
          </li>
          
          <li class="nav-item">
            <div class="nav-section">
              <span v-show="!isCollapsed" class="section-title">Académico</span>
            </div>
            <ul class="nav-submenu">
              <li>
                <RouterLink to="/mis-asignaturas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">📚</span>
                  <span v-show="!isCollapsed" class="nav-text">Mis Asignaturas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/solicitar-registro" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
                  <span class="nav-icon">✍️</span>
                  <span v-show="!isCollapsed" class="nav-text">Solicitar Registro</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </template>

        <!-- Reportes - Para Docentes y Admins -->
        <li class="nav-item" v-if="canViewReports">
          <RouterLink to="/reportes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
            <span class="nav-icon">📈</span>
            <span v-show="!isCollapsed" class="nav-text">Reportes</span>
          </RouterLink>
        </li>

        <!-- Notificaciones - Para todos -->
        <li class="nav-item">
          <RouterLink to="/notificaciones" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }">
            <span class="nav-icon">🔔</span>
            <span v-show="!isCollapsed" class="nav-text">Notificaciones</span>
            <span v-show="!isCollapsed && notificationCount > 0" class="notification-badge">{{ notificationCount }}</span>
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
const isDocente = computed(() => props.user.role === 'Docente')
const isEstudiante = computed(() => props.user.role === 'Estudiante')
const canManageTasks = computed(() => ['Docente', 'Administrador'].includes(props.user.role))
const canManageAcademic = computed(() => ['Docente', 'Administrador'].includes(props.user.role))
const canViewReports = computed(() => ['Docente', 'Administrador'].includes(props.user.role))

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
  background: #323232;
  color: #DDD0C8;
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
  border-bottom: 1px solid rgba(221, 208, 200, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(221, 208, 200, 0.05);
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
  background: #DDD0C8;
  padding: 5px;
}

.app-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
  color: #DDD0C8;
}

.toggle-btn {
  background: rgba(221, 208, 200, 0.1);
  border: none;
  color: #DDD0C8;
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
  background: rgba(221, 208, 200, 0.2);
}

/* Información del Usuario */
.user-info {
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(221, 208, 200, 0.1);
  background: rgba(221, 208, 200, 0.03);
}

.user-avatar {
  width: 45px;
  height: 45px;
  background: #DDD0C8;
  color: #323232;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.user-details h4 {
  margin: 0;
  font-size: 1rem;
  color: #DDD0C8;
}

.user-role {
  font-size: 0.85rem;
  color: rgba(221, 208, 200, 0.7);
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
  color: rgba(221, 208, 200, 0.6);
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
  color: rgba(221, 208, 200, 0.8);
  text-decoration: none;
  transition: all 0.2s;
  position: relative;
  border-radius: 0 25px 25px 0;
  margin: 2px 0;
}

.nav-link:hover {
  background: rgba(221, 208, 200, 0.1);
  color: #DDD0C8;
  transform: translateX(5px);
}

.nav-link.router-link-active {
  background: #DDD0C8;
  color: #323232;
  font-weight: 600;
}

.nav-link.router-link-active:hover {
  background: #DDD0C8;
  color: #323232;
}

.nav-link-collapsed {
  justify-content: center;
  gap: 0;
  border-radius: 8px;
  margin: 2px 8px;
}

.nav-icon {
  font-size: 1.2rem;
  width: 20px;
  text-align: center;
  flex-shrink: 0;
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
  font-weight: bold;
}

/* Footer del Sidebar */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(221, 208, 200, 0.1);
  background: rgba(221, 208, 200, 0.03);
}

.logout-btn {
  width: 100%;
  background: rgba(221, 208, 200, 0.1);
  border: none;
  color: #DDD0C8;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.logout-btn:hover {
  background: rgba(221, 208, 200, 0.2);
  transform: translateY(-1px);
}

.logout-btn-collapsed {
  justify-content: center;
  gap: 0;
}

/* Scrollbar personalizada */
.sidebar-nav::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: rgba(221, 208, 200, 0.1);
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(221, 208, 200, 0.3);
  border-radius: 3px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(221, 208, 200, 0.5);
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
