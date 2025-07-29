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
                  <span class="nav-icon">📚</span>
                  <span v-show="!isCollapsed" class="nav-text">Registrar Asignaturas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/admin/asignar-docente" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Asignar Docentes">
                  <span class="nav-icon">👨‍</span>
                  <span v-show="!isCollapsed" class="nav-text">Asignar Docentes</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/admin/crear-curso" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Crear Curso">
                  <span class="nav-icon">👥</span>
                  <span v-show="!isCollapsed" class="nav-text">Crear Curso</span>
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
                <RouterLink to="/docente/cursos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Mis Cursos">
                  <span class="nav-icon">🔔</span>
                  <span v-show="!isCollapsed" class="nav-text">Mis Cursos</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/asignar-tareas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Asignación de Tareas">
                  <span class="nav-icon">📝</span>
                  <span v-show="!isCollapsed" class="nav-text">Asignación de Tareas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/gestion-grupos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Gestión de Grupos">
                  <span class="nav-icon">👥</span>
                  <span v-show="!isCollapsed" class="nav-text">Gestión de Grupos</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/reportes" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Generación de Reportes">
                  <span class="nav-icon">📊</span>
                  <span v-show="!isCollapsed" class="nav-text">Generación de Reportes</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/visualizar-entregas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Visualizar Entregas">
                  <span class="nav-icon">📂</span>
                  <span v-show="!isCollapsed" class="nav-text">Visualizar Entregas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/docente/aceptar-solicitud" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Registrar Estudiantes">
                  <span class="nav-icon">🎓</span>
                  <span v-show="!isCollapsed" class="nav-text">Registrar Estudiantes</span>
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
                <RouterLink to="/estudiante/calendario-tareas" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Calendario de Tareas">
                  <span class="nav-icon">📅</span>
                  <span v-show="!isCollapsed" class="nav-text">Calendario de Tareas</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiante/cursos-estudiante" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Solicitar Registro">
                  <span class="nav-icon">✍️</span>
                  <span v-show="!isCollapsed" class="nav-text">Solicitar Registro</span>
                </RouterLink>
              </li>
              <li>
                <RouterLink to="/estudiante/mis-cursos" class="nav-link" :class="{ 'nav-link-collapsed': isCollapsed }" title="Calendario de Tareas">
                  <span class="nav-icon">📅</span>
                  <span v-show="!isCollapsed" class="nav-text">Mis cursos</span>
                </RouterLink>
              </li>
            </ul>
          </li>
        </template>
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
const emit = defineEmits(['toggle'])

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  emit('toggle', isCollapsed.value)
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
  background: #323232; /* Color principal (fondo) */
  color: #DDD0C8; /* Color de texto principal */
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  z-index: 1000;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.sidebar-collapsed {
  width: 105px;
}

/* Header del Sidebar */
.sidebar-header {
  padding: 1.5rem 1rem;
  border-bottom: 1px solid #7A6F66; /* Color de acento secundario */
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(154, 143, 132, 0.1); /* Color de acento principal con opacidad */
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
  background: #C4B8AD; /* Color de énfasis */
  padding: 5px;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
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
  background: #C4B8AD; /* Color de énfasis */
  color: #323232; /* Color principal (fondo) */
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
  color: #9A8F84; /* Color de acento principal */
  letter-spacing: 1px;
  opacity: 0.9;
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
  color: #DDD0C8; /* Color de texto principal */
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  border-radius: 0 25px 25px 0;
  margin: 2px 0;
  border-left: 3px solid transparent;
}

.nav-link:hover {
  background: rgba(221, 208, 200, 0.15);
  color: #DDD0C8;
  transform: translateX(8px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-link.router-link-active {
  background: rgba(154, 143, 132, 0.2); /* Color de acento principal con opacidad */
  color: #C4B8AD; /* Color de énfasis */
  font-weight: 600;
  border-left: 3px solid #9A8F84; /* Color de acento principal */
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

/* Secciones por módulo con colores más sutiles */
.admin-section .section-title {
  color: rgba(155, 89, 182, 0.7); /* Morado atenuado */
}

.docente-section .section-title {
  color: rgba(52, 152, 219, 0.7); /* Azul atenuado */
}

.estudiante-section .section-title {
  color: rgba(39, 174, 96, 0.7); /* Verde atenuado */
}

.usuarios-section .section-title {
  color: rgba(231, 76, 60, 0.7); /* Rojo atenuado */
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
  background: rgba(122, 111, 102, 0.2); /* Color de acento secundario con opacidad */
  border: 1px solid #7A6F66; /* Color de acento secundario */
  color: #DDD0C8; /* Color de texto principal */
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
  background: rgba(196, 184, 173, 0.2); /* Color de énfasis con opacidad */
  transform: translateY(-1px);
  border-color: #C4B8AD; /* Color de énfasis */
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
