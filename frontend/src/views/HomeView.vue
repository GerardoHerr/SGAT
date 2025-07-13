<script setup>
import { ref } from 'vue'

const stats = ref({
  tareasAsignadas: 12,
  estudiantes: 45,
  cursosActivos: 3,
  tareasPorCalificar: 8
})
</script>

<template>
  <div class="home-view">
    <!-- Header de la página -->
    <div class="page-header">
      <h1>Dashboard SGAT</h1>
      <p>Sistema de Gestión Académica de Tareas</p>
    </div>

    <!-- Cards de estadísticas -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <h3>12</h3>
          <p>Tareas Asignadas</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>45</h3>
          <p>Estudiantes</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-content">
          <h3>3</h3>
          <p>Cursos Activos</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <h3>8</h3>
          <p>Tareas por Calificar</p>
        </div>
      </div>
    </div>

    <!-- Sección principal -->
    <div class="main-section">
      <div class="card">
        <h2>Bienvenido al Sistema SGAT</h2>
        <p>
          Este es un ejemplo de cómo se ve el sidebar adaptado para tu aplicación. 
          El sidebar incluye navegación específica para los módulos de tu sistema:
        </p>
        <ul>
          <li><strong>Gestión de Tareas:</strong> Asignar, calificar y gestionar tareas</li>
          <li><strong>Gestión Académica:</strong> Cursos, grupos y estudiantes</li>
          <li><strong>Reportes:</strong> Estadísticas y análisis</li>
          <li><strong>Notificaciones:</strong> Alertas del sistema</li>
        </ul>
        
        <div class="action-buttons">
          <router-link to="/asignar-tarea" class="btn btn-primary">
            ➕ Asignar Nueva Tarea
          </router-link>
          <router-link to="/reportes" class="btn btn-secondary">
            📈 Ver Reportes
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  max-width: 1200px;
}

.page-header {
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.page-header p {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2.5rem;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content h3 {
  font-size: 2rem;
  color: var(--text-primary);
  margin: 0;
}

.stat-content p {
  color: var(--text-secondary);
  margin: 0;
  font-size: 0.9rem;
}

.main-section {
  margin-top: 2rem;
}

.main-section h2 {
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.main-section p {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.main-section ul {
  margin: 1.5rem 0;
  padding-left: 1.5rem;
}

.main-section li {
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
}
</style>
