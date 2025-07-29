<template>
  <div class="mostrar-tareas-estudiante">
    <div class="header-section">
      <h2>
        <i class="fas fa-graduation-cap"></i>
        Mis Tareas del Curso
      </h2>
      <p class="subtitle">Revisa y entrega tus asignaciones</p>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Cargando tareas...</p>
    </div>
    
    <div v-else class="content-section">
      <div v-if="tareas.length === 0" class="no-tareas">
        <i class="fas fa-clipboard-list"></i>
        <h3>No hay tareas registradas</h3>
        <p>Aún no tienes tareas asignadas para este curso.</p>
      </div>
      
      <div v-else class="tareas-container">
        <div class="tareas-stats">
          <div class="stat-item">
            <span class="stat-number">{{ tareas.length }}</span>
            <span class="stat-label">Total de tareas</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ tareasCalificadas }}</span>
            <span class="stat-label">Calificadas</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ tareasPendientes }}</span>
            <span class="stat-label">Pendientes</span>
          </div>
        </div>

        <div class="tareas-grid">
          <div v-for="tarea in tareas" :key="tarea.id" class="tarea-card">
            <div class="card-header">
              <div class="tarea-info">
                <div class="tarea-titulo">
                  <i class="fas fa-tasks"></i>
                  <span>{{ tarea.titulo || tarea.tarea_titulo || (tarea.tarea && tarea.tarea.titulo) || 'Sin título' }}</span>
                </div>
              </div>
              
              <div class="status-badge" :class="getStatusClass(tarea)">
                <i :class="getStatusIcon(tarea)"></i>
                <span>{{ getStatusText(tarea) }}</span>
              </div>
            </div>

            <div class="card-content">
              <div class="calificacion-section" v-if="tarea.calificacion !== undefined">
                <div class="calificacion-container">
                  <label class="calificacion-label">Calificación:</label>
                  <div class="calificacion-value" :class="getCalificacionClass(tarea.calificacion)">
                    {{ tarea.calificacion !== null && tarea.calificacion !== undefined ? tarea.calificacion : 'Pendiente' }}
                  </div>
                </div>
              </div>
            </div>

            <div class="card-footer">
              <button class="btn-revisar-tarea" @click="revisarTarea(tarea)">
                <i class="fas fa-eye"></i>
                <span>Revisar Entrega</span>
                <i class="fas fa-chevron-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MostarTareasEstudiante',

  data() {
    return {
      tareas: [],
      loading: true,
      cursoId: null,
      estudianteEmail: ''
    }
  },

  computed: {
    tareasCalificadas() {
      return this.tareas.filter(t => t.calificacion !== null && t.calificacion !== undefined).length
    },
    tareasPendientes() {
      return this.tareas.filter(t => t.calificacion === null || t.calificacion === undefined).length
    }
  },

  async mounted() {
    const cursoId = this.$route.query.curso;
    console.log('Curso ID:', cursoId);
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    this.estudianteEmail = currentUser?.email || '';
    this.cursoId = cursoId;
    await this.cargarTareas();
  },

  methods: {
    async cargarTareas() {
      this.loading = true
      try {
        const response = await axios.get(`http://localhost:8000/api/entregas/?curso_id=${this.cursoId}`)
        this.tareas = response.data.filter(t => t.estudiante_email === this.estudianteEmail);
        console.log('Tareas cargadas:', this.tareas)
      } catch (error) {
        this.tareas = []
      }
      this.loading = false
    },

    async revisarTarea(tarea) {
      this.$router.push({
        name: 'SubirTareaEstudiante',
        params: { id: tarea.id }
      });
    },

    getStatusClass(tarea) {
      if (tarea.calificacion !== null && tarea.calificacion !== undefined) {
        return 'status-calificada'
      }
      return 'status-pendiente'
    },

    getStatusIcon(tarea) {
      if (tarea.calificacion !== null && tarea.calificacion !== undefined) {
        return 'fas fa-check-circle'
      }
      return 'fas fa-clock'
    },

    getStatusText(tarea) {
      if (tarea.calificacion !== null && tarea.calificacion !== undefined) {
        return 'Calificada'
      }
      return 'Pendiente'
    },

    getCalificacionClass(calificacion) {
      if (calificacion !== null && calificacion !== undefined) {
        return calificacion >= 7 ? 'calif-alta' : calificacion >= 5 ? 'calif-media' : 'calif-baja'
      }
      return 'calif-pendiente'
    }
  },

  filters: {
    fecha(val) {
      if (!val) return ''
      return new Date(val).toLocaleString()
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.mostrar-tareas-estudiante {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  min-height: 80vh;
  width: 100%;
}

.header-section {
  text-align: center;
  margin-bottom: 40px;
  
  h2 {
    color: #2e7d32;
    font-size: 2.2em;
    font-weight: 700;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    
    i {
      font-size: 0.9em;
      color: #4caf50;
    }
  }
  
  .subtitle {
    color: #666;
    font-size: 1.1em;
    font-weight: 400;
    margin: 0;
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  
  .loading-spinner {
    width: 48px;
    height: 48px;
    border: 4px solid #e8f5e8;
    border-top: 4px solid #4caf50;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 16px;
  }
  
  .loading-text {
    color: #666;
    font-size: 1.1em;
    margin: 0;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.content-section {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(67, 233, 123, 0.12);
  padding: 32px;
  border: 1px solid rgba(76, 175, 80, 0.08);
}

.no-tareas {
  text-align: center;
  padding: 80px 20px;
  color: #666;
  
  i {
    font-size: 4em;
    color: #ffcc02;
    margin-bottom: 24px;
    display: block;
  }
  
  h3 {
    color: #2e7d32;
    font-size: 1.5em;
    font-weight: 600;
    margin: 0 0 12px 0;
  }
  
  p {
    font-size: 1.1em;
    margin: 0;
    opacity: 0.8;
  }
}

.tareas-container {
  .tareas-stats {
    display: flex;
    justify-content: center;
    gap: 32px;
    margin-bottom: 40px;
    padding: 24px;
    background: linear-gradient(135deg, #f8fff8 0%, #e8f5e8 100%);
    border-radius: 16px;
    border: 1px solid rgba(76, 175, 80, 0.1);
    
    .stat-item {
      text-align: center;
      
      .stat-number {
        display: block;
        font-size: 2.2em;
        font-weight: 700;
        color: #2e7d32;
        line-height: 1;
      }
      
      .stat-label {
        display: block;
        font-size: 0.9em;
        color: #666;
        font-weight: 500;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
    }
  }
}

.tareas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 28px;
}

.tarea-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(67, 233, 123, 0.08);
  border: 1px solid rgba(76, 175, 80, 0.12);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(67, 233, 123, 0.16);
    border-color: rgba(76, 175, 80, 0.2);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  }
}

.card-header {
  padding: 24px 24px 16px 24px;
  border-bottom: 1px solid #f5f5f5;
  
  .tarea-info {
    margin-bottom: 16px;
    
    .tarea-titulo {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 1.2em;
      font-weight: 600;
      color: #323232;
      margin-bottom: 8px;
      
      i {
        color: #4caf50;
        font-size: 1.1em;
      }
    }
    
    .tarea-meta {
      .tarea-id {
        display: inline-block;
        background: #f0f0f0;
        color: #666;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 500;
      }
    }
  }
  
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 600;
    
    &.status-calificada {
      background: rgba(76, 175, 80, 0.1);
      color: #2e7d32;
      border: 1px solid rgba(76, 175, 80, 0.2);
    }
    
    &.status-pendiente {
      background: rgba(255, 204, 2, 0.1);
      color: #f57f17;
      border: 1px solid rgba(255, 204, 2, 0.2);
    }
  }
}

.card-content {
  padding: 16px 24px;
  
  .calificacion-section {
    .calificacion-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px;
      background: #fafafa;
      border-radius: 12px;
      border: 1px solid #eee;
      
      .calificacion-label {
        font-weight: 500;
        color: #666;
        font-size: 1em;
      }
      
      .calificacion-value {
        font-weight: 700;
        font-size: 1.2em;
        padding: 6px 16px;
        border-radius: 8px;
        
        &.calif-alta {
          background: rgba(76, 175, 80, 0.1);
          color: #2e7d32;
          border: 1px solid rgba(76, 175, 80, 0.2);
        }
        
        &.calif-media {
          background: rgba(255, 193, 7, 0.1);
          color: #f57f17;
          border: 1px solid rgba(255, 193, 7, 0.2);
        }
        
        &.calif-baja {
          background: rgba(244, 67, 54, 0.1);
          color: #c62828;
          border: 1px solid rgba(244, 67, 54, 0.2);
        }
        
        &.calif-pendiente {
          background: rgba(158, 158, 158, 0.1);
          color: #757575;
          border: 1px solid rgba(158, 158, 158, 0.2);
        }
      }
    }
  }
}

.card-footer {
  padding: 16px 24px 24px 24px;
}

.btn-revisar-tarea {
  width: 100%;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  border: none;
  border-radius: 12px;
  padding: 14px 24px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  outline: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
  
  &:hover,
  &:focus {
    background: linear-gradient(135deg, #38f9d7 0%, #43e97b 100%);
    box-shadow: 0 8px 24px rgba(67, 233, 123, 0.3);
    transform: translateY(-2px);
  }
  
  &:active {
    transform: translateY(0);
  }
  
  span {
    flex: 1;
    text-align: center;
  }
}

// Responsive Design
@media (max-width: 1024px) {
  .tareas-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 20px;
  }
  
  .tareas-stats {
    gap: 24px !important;
  }
}

@media (max-width: 768px) {
  .mostrar-tareas-estudiante {
    padding: 20px 16px;
  }
  
  .content-section {
    padding: 20px;
    border-radius: 16px;
  }
  
  .header-section {
    h2 {
      font-size: 1.8em;
      flex-direction: column;
      gap: 8px;
    }
    
    .subtitle {
      font-size: 1em;
    }
  }
  
  .tareas-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .tareas-stats {
    flex-direction: column;
    gap: 16px !important;
    
    .stat-item {
      .stat-number {
        font-size: 1.8em;
      }
    }
  }
  
  .card-header,
  .card-content,
  .card-footer {
    padding-left: 16px;
    padding-right: 16px;
  }
}

@media (max-width: 480px) {
  .mostrar-tareas-estudiante {
    padding: 16px 12px;
  }
  
  .content-section {
    padding: 16px;
  }
  
  .btn-revisar-tarea {
    padding: 12px 20px;
    font-size: 0.95em;
  }
}</style>