<template>
  <aside class="sidebar" :class="{ 'sidebar-collapsed': isCollapsed }">
    <!-- Header del Sidebar -->
    <div class="sidebar-header">
      <div class="logo-container">
        <img src="@/assets/logo.svg" alt="SGAT Logo" class="logo" />
        <h2 v-show="!isCollapsed" class="app-title">SGAT</h2>
      </div>
      <button @click="toggleSidebar" class="toggle-btn">
        <span class="toggle-icon">{{ isCollapsed ? '>' : '<' }}</span>
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
          <RouterLink to="/" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Dashboard">
            <span class="nav-icon">📊</span>
            <span v-show="!isCollapsed" class="nav-text">Dashboard</span>
          </RouterLink>
        </li>

        <!-- ADMINISTRADOR - Módulo Morado 🟣 -->
        <template v-if="isAdmin">
          <li class="nav-item">
            <div class="nav-section admin-section">
              <span v-show="!isCollapsed" class="section-title">🟣 Administración</span>
            </div>
            <ul class="nav-submenu">
              <!-- Prioridad Alta -->
              <li>
                <RouterLink to="/admin/usuarios" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Registrar Usuarios">
                  <span class="nav-icon">👥</span>
                  <span v-show="!isCollapsed" class="nav-text">Registrar Usuarios</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/admin/asignaturas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Registrar Asignaturas">
                  <span class="nav-icon">�</span>
                  <span v-show="!isCollapsed" class="nav-text">Registrar Asignaturas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/admin/asignar-docente" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Asignar Docentes">
                  <span class="nav-icon">👨‍�</span>
                  <span v-show="!isCollapsed" class="nav-text">Asignar Docentes</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/admin/registrar-periodo" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Periodos Lectivos">
                  <span class="nav-icon">�</span>
                  <span v-show="!isCollapsed" class="nav-text">Periodos Lectivos</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/admin/reportes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Reportes de Actividad">
                  <span class="nav-icon">�</span>
                  <span v-show="!isCollapsed" class="nav-text">Reportes de Actividad</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/admin/roles" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Gestión de Roles">
                  <span class="nav-icon">🎭</span>
                  <span v-show="!isCollapsed" class="nav-text">Gestión de Roles</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </template>

        <!-- DOCENTE - Módulo Celeste 🔵 -->
        <template v-if="isDocente">
          <li class="nav-item">
            <div class="nav-section docente-section">
              <span v-show="!isCollapsed" class="section-title">🔵 Gestión de Tareas</span>
            </div>
            <ul class="nav-submenu">
              <!-- Prioridad Alta -->
              <li>
                <RouterLink to="/docente/asignar-tareas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Asignación de Tareas">
                  <span class="nav-icon">📝</span>
                  <span v-show="!isCollapsed" class="nav-text">Asignación de Tareas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/listar-tareas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Mis Tareas">
                  <span class="nav-icon">📋</span>
                  <span v-show="!isCollapsed" class="nav-text">Mis Tareas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/gestion-grupos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Gestión de Grupos">
                  <span class="nav-icon">👥</span>
                  <span v-show="!isCollapsed" class="nav-text">Gestión de Grupos</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/calificar" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Calificación de Tareas">
                  <span class="nav-icon">✅</span>
                  <span v-show="!isCollapsed" class="nav-text">Calificación de Tareas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/retroalimentacion" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Retroalimentación">
                  <span class="nav-icon">�</span>
                  <span v-show="!isCollapsed" class="nav-text">Retroalimentación</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/reportes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Generación de Reportes">
                  <span class="nav-icon">📊</span>
                  <span v-show="!isCollapsed" class="nav-text">Generación de Reportes</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/entregas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Visualizar Entregas">
                  <span class="nav-icon">📂</span>
                  <span v-show="!isCollapsed" class="nav-text">Visualizar Entregas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/entrega-unica" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Entrega Única">
                  <span class="nav-icon">📄</span>
                  <span v-show="!isCollapsed" class="nav-text">Entrega Única</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/registrar-estudiantes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Registrar Estudiantes">
                  <span class="nav-icon">🎓</span>
                  <span v-show="!isCollapsed" class="nav-text">Registrar Estudiantes</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/notificaciones-revision" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Notificación de Revisión">
                  <span class="nav-icon">🔔</span>
                  <span v-show="!isCollapsed" class="nav-text">Notificación de Revisión</span>
                </RouterLink>
              </li>
            </ul>
          </li>
          
          <li class="nav-item">
            <div class="nav-section">
              <span v-show="!isCollapsed" class="section-title">Configuraciones</span>
            </div>
            <ul class="nav-submenu">
              <!-- Prioridad Media -->
              <li>
                <RouterLink to="/docente/tareas-atrasadas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Permitir Tareas Atrasadas">
                  <span class="nav-icon">⏰</span>
                  <span v-show="!isCollapsed" class="nav-text">Permitir Tareas Atrasadas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/retroalimentacion-cambios" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Cambios en Retroalimentación">
                  <span class="nav-icon">🔄</span>
                  <span v-show="!isCollapsed" class="nav-text">Cambios en Retroalimentación</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </template>

        <!-- ESTUDIANTE - Módulo Verde 🟢 -->
        <template v-if="isEstudiante">
          <li class="nav-item">
            <div class="nav-section estudiante-section">
              <span v-show="!isCollapsed" class="section-title">🟢 Mis Actividades</span>
            </div>
            <ul class="nav-submenu">
              <!-- Prioridad Alta -->
              <li>
                <RouterLink to="/estudiante/calendario" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Calendario de Tareas">
                  <span class="nav-icon">📅</span>
                  <span v-show="!isCollapsed" class="nav-text">Calendario de Tareas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiante/solicitar-asignatura" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Solicitar Registro">
                  <span class="nav-icon">✍️</span>
                  <span v-show="!isCollapsed" class="nav-text">Solicitar Registro</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiante/editar-entrega" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Editar Entrega">
                  <span class="nav-icon">✏️</span>
                  <span v-show="!isCollapsed" class="nav-text">Editar Entrega</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiante/notificaciones" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Notificaciones">
                  <span class="nav-icon">🔔</span>
                  <span v-show="!isCollapsed" class="nav-text">Notificaciones</span>
                  <span v-show="!isCollapsed && notificationCount > 0" class="notification-badge">{{ notificationCount }}</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiante/historial" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Historial de Tareas">
                  <span class="nav-icon">📜</span>
                  <span v-show="!isCollapsed" class="nav-text">Historial de Tareas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiante/entregar" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Entregar Tareas">
                  <span class="nav-icon">📤</span>
                  <span v-show="!isCollapsed" class="nav-text">Entregar Tareas</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </template>

        <!-- MÓDULO USUARIOS - Para todos los roles 🔴 -->
        <li class="nav-item">
          <div class="nav-section usuarios-section">
            <span v-show="!isCollapsed" class="section-title">🔴 Mi Perfil</span>
          </div>
          <ul class="nav-submenu">
            <li>
              <RouterLink to="/perfil" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Perfil Personal">
                <span class="nav-icon">👤</span>
                <span v-show="!isCollapsed" class="nav-text">Perfil Personal</span>
              </RouterLink>
            </li>
            <li>
              <RouterLink to="/configuracion" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Configuración">
                <span class="nav-icon">⚙️</span>
                <span v-show="!isCollapsed" class="nav-text">Configuración</span>
              </RouterLink>
            </li>
          </ul>
        </li>
      </ul>
    </nav>

    <!-- Footer del Sidebar -->
    <div class="sidebar-footer">
      <RouterLink to="/login-simple" class="logout-btn" :class="{ 'logout-btn-collapsed': isCollapsed }" title="Cerrar Sesión">
        <span class="nav-icon">🚪</span>
        <span v-show="!isCollapsed" class="nav-text">Cerrar Sesión</span>
      </RouterLink>
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
    default: () => null
  },
  notificationCount: {
    type: Number,
    default: 3
  }
})

// Computed properties
const userName = computed(() => {
  if (!props.user) return 'Usuario Demo'
  return props.user.name || 'Usuario Demo'
})

const userRole = computed(() => {
  if (!props.user) return 'Docente'
  return props.user.role || 'Docente'
})

const userInitials = computed(() => {
  const name = userName.value
  const names = name.split(' ')
  return names.map(name => name[0]).join('').toUpperCase()
})

const isAdmin = computed(() => userRole.value === 'Administrador')
const isDocente = computed(() => userRole.value === 'Docente')
const isEstudiante = computed(() => userRole.value === 'Estudiante')

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
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  border-radius: 0 25px 25px 0;
  margin: 2px 0;
}

.nav-link:hover {
  background: rgba(221, 208, 200, 0.15);
  color: #DDD0C8;
  transform: translateX(8px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  margin: 4px 8px;
  padding: 0.75rem;
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

/* Secciones por módulo */
.admin-section .section-title {
  color: #9b59b6; /* Morado para admin */
}

.docente-section .section-title {
  color: #3498db; /* Celeste para docente */
}

.estudiante-section .section-title {
  color: #27ae60; /* Verde para estudiante */
}

.usuarios-section .section-title {
  color: #e74c3c; /* Rojo para usuarios */
}

/* Mejoras para el estado colapsado */
.sidebar-collapsed .notification-badge {
  display: none;
}

.sidebar-collapsed .nav-link:hover::after {
  content: attr(title);
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%);
  background: #323232;
  color: #DDD0C8;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  white-space: nowrap;
  font-size: 0.8rem;
  margin-left: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  opacity: 0;
  animation: fadeIn 0.2s ease forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
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
  text-decoration: none;
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
    width: 100vw;
    max-width: 280px;
  }
  
  .sidebar.sidebar-open {
    transform: translateX(0);
  }
}
</style>
