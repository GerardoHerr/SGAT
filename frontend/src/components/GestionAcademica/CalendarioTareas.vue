<template>
  <div class="container">
    <h2><i class="fas fa-calendar-alt me-2"></i>Calendario de Tareas</h2>
    
    <div v-if="loading" class="alert alert-info">
      <i class="fas fa-spinner fa-spin me-2"></i>Cargando tareas...
    </div>
    
    <div v-else>
      <div v-if="Object.keys(tareasPorFecha).length === 0" class="alert alert-light text-center">
        <i class="fas fa-info-circle me-2"></i>No hay tareas registradas.
      </div>
      
      <div v-else>
        <div v-for="(tareas, fecha) in tareasPorFecha" :key="fecha" class="card mb-4">
          <div class="card-header bg-light">
            <h3 class="h5 mb-0">
              <i class="fas fa-calendar-day me-2"></i>
              {{ formatFecha(fecha) }}
            </h3>
          </div>
          
          <ul class="list-group list-group-flush">
            <li v-for="tarea in tareas" :key="tarea.id" class="list-group-item">
              <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                  <i class="fas fa-tasks me-2 text-primary"></i>
                  <div>
                    <div class="fw-bold">{{ tarea.tarea_titulo || tarea.titulo || 'Sin título' }}</div>
                    <div v-if="tarea.calificacion !== undefined" class="text-muted small">
                      <i class="fas fa-star text-warning"></i>
                      {{ tarea.calificacion ?? 'Sin calificación' }}
                    </div>
                    
                  </div>
                </div>
                
                <button 
                  @click="irASubirTarea(tarea.id)" 
                  class="btn btn-sm btn-outline-primary"
                >
                  <i class="fas fa-eye me-1"></i> Revisar
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CalendarioTareas',
  data() {
    return {
      tareas: [],
      loading: true,
      estudianteEmail: ''
    }
  },
  computed: {
    tareasPorFecha() {
      // Agrupa las tareas por la fecha de entrega de la asignación (fecha_entrega)
      const agrupadas = {};
      for (const tarea of this.tareas) {
        // Puede venir como tarea.fecha_entrega o fecha_entrega
        const fecha = tarea.fecha_entrega || (tarea.tarea && tarea.tarea.fecha_entrega);
        if (!fecha) continue;
        const fechaKey = fecha.split('T')[0]; // Solo la parte de la fecha
        if (!agrupadas[fechaKey]) agrupadas[fechaKey] = [];
        agrupadas[fechaKey].push(tarea);
      }
      return agrupadas;
    }
  },
  async mounted() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    this.estudianteEmail = currentUser?.email || '';
    await this.cargarTareas();
  },
  methods: {
    async cargarTareas() {
      this.loading = true;
      try {
        const response = await axios.get(`http://localhost:8000/api/entregas/?estudiante_email=${this.estudianteEmail}`);
        // Solo tareas del usuario logeado
        this.tareas = response.data.filter(
          t => t.estudiante_email === this.estudianteEmail
        );
        console.log('Tareas cargadas:', this.tareas);
      } catch (error) {
        this.tareas = [];
      }
      this.loading = false;
    },
    formatFecha(fecha) {
      if (!fecha) return '';
      return new Date(fecha).toLocaleDateString();
    },
    irASubirTarea(id) {
      this.$router.push({ name: 'SubirTareaEstudiante', params: { id } });
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.card {
  .card-header {
    i {
      color: $color-primary;
    }
  }
}

.list-group-item {
  transition: background-color 0.2s ease;
  
  &:hover {
    background-color: rgba($color-primary, 0.05);
  }
}

.btn-link {
  text-decoration: none;
  transition: color 0.2s ease;
  
  &:hover {
    text-decoration: underline;
  }
}

/* Ajustes responsivos */
@media (max-width: 768px) {
  .card {
    .card-header {
      padding: 0.75rem 1rem;
    }
    
    .list-group-item {
      padding: 1rem;
    }
  }
  
  .btn-outline-primary {
    width: 100%;
    margin-top: 0.5rem;
    text-align: center;
  }
}
</style>