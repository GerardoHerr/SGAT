<template>
  <div class="mostrar-tareas">
    <div class="header-section">
      <div class="page-title">
        <h2>
          <i class="fas fa-tasks"></i>
          Tareas del Curso
        </h2>
        <div v-if="cursoSeleccionado && tareas.length > 0" class="curso-stats">
          <div class="stat-card">
            <i class="fas fa-clipboard-list"></i>
            <div class="stat-info">
              <span class="stat-number">{{ tareas.length }}</span>
              <span class="stat-label">Total de tareas</span>
            </div>
          </div>
          <div class="stat-card">
            <i class="fas fa-chart-pie"></i>
            <div class="stat-info">
              <span class="stat-number">{{ totalEntregas }}</span>
              <span class="stat-label">Entregas registradas</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="cursoSeleccionado" class="content-section">
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner">
          <i class="fas fa-spinner fa-spin"></i>
          <span>Cargando tareas del curso...</span>
        </div>
      </div>

      <div v-else-if="tareas.length === 0" class="no-tareas">
        <div class="empty-state">
          <i class="fas fa-inbox"></i>
          <h3>No hay tareas registradas</h3>
          <p>Aún no se han creado tareas para este curso.</p>
        </div>
      </div>

      <div v-else class="tareas-container">
        <div v-for="tipo in tiposTareaConTareas" :key="tipo" class="tipo-seccion">
          <div class="tipo-header">
            <div class="tipo-info">
              <h3>
                <i :class="tipoIcons[tipo]"></i>
                {{ tipoLabels[tipo] }}
              </h3>
              
            </div>
            <div class="tipo-resumen">
              <span class="entregas-total">
                <i class="fas fa-upload"></i>
              </span>
            </div>
          </div>

          <div class="tareas-grid">
            <div v-for="tarea in tareasPorTipo(tipo)" :key="tarea.id" class="tarea-card">
              <div class="tarea-header">
                <div class="tarea-titulo-section">
                  <h4 class="tarea-titulo">{{ tarea.titulo }}</h4>
                  <div class="tarea-meta">
                    <span class="tarea-modalidad" :class="{ 'grupal': tarea.es_grupal, 'individual': !tarea.es_grupal }">
                      <i :class="tarea.es_grupal ? 'fas fa-users' : 'fas fa-user'"></i>
                      {{ tarea.es_grupal ? 'Grupal' : 'Individual' }}
                    </span>
                  </div>
                </div>
                
                <div class="tarea-stats">
                  <div class="stat-item">
                    <i class="fas fa-file-upload"></i>
                    <div class="stat-details">
                      <span class="stat-value">{{ tarea.cantidad_entregas }}</span>
                      <span class="stat-text">entregas</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="tarea-info-adicional" v-if="tarea.fecha_vencimiento || tarea.descripcion">
                <div v-if="tarea.fecha_vencimiento" class="info-item">
                  <i class="fas fa-calendar-alt"></i>
                  <span>Vence: {{ formatearFecha(tarea.fecha_vencimiento) }}</span>
                </div>
                <div v-if="tarea.descripcion" class="info-item descripcion">
                  <i class="fas fa-align-left"></i>
                  <span>{{ tarea.descripcion }}</span>
                </div>
              </div>

              <div class="tarea-actions">
                <button 
                  class="btn-calificar" 
                  @click="irACalificarTarea(tarea.id, tarea.tipo_tarea)"
                  :disabled="tarea.cantidad_entregas === 0"
                >
                  <i class="fas fa-clipboard-check"></i>
                  <span v-if="tarea.cantidad_entregas === 0">Sin entregas</span>
                  <span v-else>Calificar ({{ tarea.cantidad_entregas }})</span>
                </button>
                
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-curso-seleccionado">
      <div class="empty-state">
        <i class="fas fa-graduation-cap"></i>
        <h3>Selecciona un curso</h3>
        <p>Para ver las tareas, primero selecciona un curso desde el menú.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MostrarTareas',
  data() {
    return {
      cursoSeleccionado: '',
      tareas: [],
      docenteEmail: '',
      loading: false,
      tiposTarea: ['AA', 'ACD', 'APE'],
      tipoLabels: {
        AA: 'AA - Actividades de Aplicación',
        ACD: 'ACD - Construcción del Conocimiento',
        APE: 'APE - Prácticas de Experimentación'
      },
      tipoIcons: {
        AA: 'fas fa-puzzle-piece',
        ACD: 'fas fa-lightbulb',
        APE: 'fas fa-flask'
      }
    }
  },
  
  computed: {
    tiposTareaConTareas() {
      return this.tiposTarea.filter(tipo => this.tareasPorTipo(tipo).length > 0);
    },
    
    totalEntregas() {
      return this.tareas.reduce((total, tarea) => total + (tarea.cantidad_entregas || 0), 0);
    }
  },
  
  async mounted() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'))
    if (!currentUser || currentUser.rol !== 'DOC') {
      this.$router.push('/login')
      return
    }
    this.docenteEmail = currentUser.email
    this.setCursoSeleccionadoYcargar()
  },

  watch: {
    '$route'(to, from) {
      this.setCursoSeleccionadoYcargar()
    }
  },

  methods: {
    setCursoSeleccionadoYcargar() {
      let cursoId = this.$route.query.curso
      if (!cursoId && this.$route.params.id) {
        cursoId = this.$route.params.id
      }
      if (cursoId) {
        this.cursoSeleccionado = String(cursoId)
        this.cargarTareas()
      } else {
        this.cursoSeleccionado = ''
        this.tareas = []
      }
    },
    
    async cargarTareas() {
      if (!this.cursoSeleccionado) {
        this.tareas = []
        return
      }
      
      this.loading = true
      try {
        const url = `http://localhost:8000/api/asignaciones/?curso=${this.cursoSeleccionado}&docente_email=${this.docenteEmail}`
        console.log('Cargando tareas desde:', url)
        const response = await axios.get(url)
        this.tareas = Array.isArray(response.data) ? response.data : []
      } catch (error) {
        console.error('Error al cargar tareas:', error)
        this.tareas = []
      } finally {
        this.loading = false
      }
    },
    
    tareasPorTipo(tipo) {
      return this.tareas.filter(t => t.tipo_tarea === tipo)
    },
    
    totalEntregasPorTipo(tipo) {
      return this.tareasPorTipo(tipo).reduce((total, tarea) => total + (tarea.cantidad_entregas || 0), 0);
    },
    
    irACalificarTarea(tareaId, tipoTarea) {
      if (tipoTarea === 'tipo_tarea') {
        const tarea = this.tareas.find(t => t.id === tareaId);
        tipoTarea = tarea ? tarea.tipo_tarea : '';
      }
      console.log('Ir a calificar tarea:', tareaId, 'Tipo:', tipoTarea);
      this.$router.push({ name: 'CalificarTarea', params: { id: tareaId, tipo_tarea: tipoTarea } })
    },
    
    verDetallesTarea(tarea) {
      // Aquí podrías implementar un modal o navegación a detalles
      console.log('Ver detalles de tarea:', tarea);
    },
    
    formatearFecha(fecha) {
      if (!fecha) return '';
      return new Date(fecha).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    getStatusClass(tarea) {
      if (tarea.cantidad_entregas === 0) return 'sin-entregas';
      if (tarea.fecha_vencimiento && new Date(tarea.fecha_vencimiento) < new Date()) return 'vencida';
      return 'activa';
    },
    
    getStatusIcon(tarea) {
      if (tarea.cantidad_entregas === 0) return 'fas fa-inbox';
      if (tarea.fecha_vencimiento && new Date(tarea.fecha_vencimiento) < new Date()) return 'fas fa-exclamation-triangle';
      return 'fas fa-check-circle';
    },
    
    getStatusText(tarea) {
      if (tarea.cantidad_entregas === 0) return 'Sin entregas';
      if (tarea.fecha_vencimiento && new Date(tarea.fecha_vencimiento) < new Date()) return 'Vencida';
      return 'Activa';
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
.mostrar-tareas {
  background: #f8f8f8;
  min-height: 100vh;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  width: 90%;
}

.header-section {
  max-width: 1200px;
  margin: 0 auto 2rem;
  
  .page-title {
    background: #ffffff;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    border: 1px solid #e0e0e0;
    
    h2 {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: #46d37f;
      margin: 0 0 1.5rem 0;
      font-size: 2rem;
      font-weight: 600;
      text-align: center;
      justify-content: center;
      
      i {
        font-size: 1.8rem;
        color: #86f54b;
      color: #43a047;
      }
    }
    
    .curso-stats {
      display: flex;
      justify-content: center;
      gap: 2rem;
      padding-top: 1.5rem;
      border-top: 1px solid #e0e0e0;
      
      .stat-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: #e8f5e9;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 1px solid #a5d6a7;
        
        i {
          font-size: 1.5rem;
          color: #43a047;
        }
        
        .stat-info {
          display: flex;
          flex-direction: column;
          
          .stat-number {
            font-size: 1.5rem;
            font-weight: 700;
            color: #323232;
            line-height: 1;
          }
          
          .stat-label {
            font-size: 0.85rem;
            color: #666666;
            font-weight: 500;
          }
        }
      }
    }
  }
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  
  .loading-spinner {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    color: #3498db;
    
    i {
      font-size: 2.5rem;
    }
    
    span {
      font-size: 1.1rem;
      font-weight: 500;
    }
  }
}

.no-tareas,
.no-curso-seleccionado {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  
  .empty-state {
    text-align: center;
    background: #ffffff;
    padding: 3rem;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    border: 2px dashed #e0e0e0;
    max-width: 400px;
    
    i {
      font-size: 4rem;
      color: #b94a48;
      margin-bottom: 1.5rem;
    }
    
    h3 {
      color: #323232;
      margin: 0 0 0.75rem 0;
      font-size: 1.5rem;
      font-weight: 600;
    }
    
    p {
      color: #666666;
      margin: 0;
      font-size: 1rem;
      line-height: 1.5;
    }
  }
}

.tareas-container {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.tipo-seccion {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  overflow: hidden;
  border: 1px solid #e0e0e0;
  
  .tipo-header {
      background: linear-gradient(135deg, #43a047, #388e3c);
    color: #ffffff;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    
    .tipo-info {
      display: flex;
      align-items: center;
      gap: 1rem;
      
      h3 {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
        
        i {
          font-size: 1.2rem;
        }
      }
      
      .tipo-badge {
        background: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.3);
      }
    }
    
    .tipo-resumen {
      .entregas-total {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.15);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        border: 1px solid rgba(255, 255, 255, 0.2);
        
        i {
          font-size: 0.9rem;
        }
      }
    }
  }
  
  .tareas-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 1.5rem;
    padding: 2rem;
    border-left: 4px solid #43a047;
}

.tarea-card {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(52,152,219,0.15);
    border-color: #3498db;
  }
  
  .tarea-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
    gap: 1rem;
  }
  
  .tarea-titulo-section {
    flex: 1;
    
    .tarea-titulo {
      color: #3498db;
      font-weight: 600;
      font-size: 1.2rem;
      margin: 0 0 0.75rem 0;
      line-height: 1.3;
    }
    
    .tarea-meta {
      .tarea-modalidad {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        
        &.grupal {
          background: #e8f5e9;
          color: #1e874b;
          border: 1px solid #4caf50;
        }
        
        &.individual {
          background: #fff3e0;
          color: #f57c00;
          border: 1px solid #ff9800;
        }
        
        i {
          font-size: 0.8rem;
        }
      }
    }
  }
  
  .tarea-stats {
    .stat-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      background: #f8f9fa;
      padding: 0.75rem 1rem;
      border-radius: 8px;
      border: 1px solid #e9ecef;
      
      i {
        color: #50c93a;
        font-size: 1.1rem;
      }
      
      .stat-details {
        display: flex;
        flex-direction: column;
        align-items: center;
        
        .stat-value {
          font-size: 1.2rem;
          font-weight: 700;
          color: #323232;
          line-height: 1;
        }
        
        .stat-text {
          font-size: 0.75rem;
          color: #666666;
          font-weight: 500;
        }
      }
    }
  }
  
  .tarea-info-adicional {
    margin: 1rem 0;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #6bea75;
    
    .info-item {
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      margin-bottom: 0.75rem;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      i {
        color: #3498db;
        font-size: 0.9rem;
        margin-top: 0.1rem;
        flex-shrink: 0;
      }
      
      span {
        color: #555555;
        font-size: 0.9rem;
        line-height: 1.4;
      }
      
      &.descripcion span {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
    }
  }
  
  .tarea-actions {
    display: flex;
    gap: 0.75rem;
    margin-top: 1.5rem;
    padding-top: 1rem;
    border-top: 1px solid #e9ecef;
  }
  
  .tarea-status {
    position: absolute;
    top: 1rem;
    right: 1rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.7rem;
    border-radius: 15px;
    font-size: 0.75rem;
    font-weight: 500;
    
    &.activa {
      background: #e8f5e9;
      color: #1e874b;
      border: 1px solid #4caf50;
    }
    
    &.sin-entregas {
      background: #fff3e0;
      color: #f57c00;
      border: 1px solid #ff9800;
    }
    
    &.vencida {
      background: #ffebee;
      color: #c62828;
      border: 1px solid #f44336;
    }
    
    i {
      font-size: 0.7rem;
    }
  }
}

// Botones
%btn-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.7rem 1.2rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  text-decoration: none;
  flex: 1;
  
  i {
    font-size: 0.85rem;
  }
  
  &:disabled {
    cursor: not-allowed;
    opacity: 0.6;
    transform: none !important;
  }
}

.btn-calificar {
  @extend %btn-base;
  background: #43a047;
  color: #ffffff;
  border-color: #43a047;
  
  &:hover:not(:disabled) {
    background: #388e3c;
    border-color: #388e3c;
    transform: translateY(-2px);
  }
  
  &:disabled {
    background: #bdc3c7;
    border-color: #bdc3c7;
  }
}

.btn-secundario {
  @extend %btn-base;
  background: #ffffff;
  color: #43a047;
  border-color: #31c238;
  
  &:hover {
    background: #43db4a;
    color: #ffffff;
    transform: translateY(-2px);
  }
}

// Responsive
@media (max-width: 1024px) {
  .tareas-grid {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  }
  
  .curso-stats {
    flex-direction: column;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .mostrar-tareas {
    padding: 1rem;
  }
  
  .tareas-grid {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .tarea-card {
    padding: 1rem;
  }
  
  .tarea-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .tarea-actions {
    flex-direction: column;
  }
  
  .tipo-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .page-title h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .tarea-card {
    .tarea-status {
      position: static;
      align-self: flex-start;
      margin-bottom: 0.5rem;
    }
  }
}

}

</style>