<template>
  <div class="mis-calificaciones">
    <h2>Mis Calificaciones</h2>
    
    <div v-if="loading" class="loading">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
      <p>Cargando tus calificaciones...</p>
    </div>
    
    <div v-else>
      <div v-if="calificaciones.length === 0" class="alert alert-info">
        No tienes calificaciones registradas aún.
      </div>
      
      <div v-else>
        <div class="filtros mb-4">
          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label>Filtrar por asignatura:</label>
                <select v-model="filtroAsignatura" class="form-select">
                  <option value="">Todas las asignaturas</option>
                  <option v-for="asignatura in asignaturasUnicas" :key="asignatura" :value="asignatura">
                    {{ asignatura }}
                  </option>
                </select>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label>Filtrar por período:</label>
                <select v-model="filtroPeriodo" class="form-select">
                  <option value="">Todos los períodos</option>
                  <option v-for="periodo in periodosUnicos" :key="periodo" :value="periodo">
                    {{ periodo }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>
        
        <div class="calificaciones-container">
          <div v-for="calificacion in calificacionesFiltradas" :key="calificacion.id" class="calificacion-card">
            <div class="calificacion-header">
              <h3>{{ calificacion.tarea_titulo }}</h3>
              <span class="badge" :class="getBadgeClass(calificacion.tarea_tipo)">
                {{ getTipoTarea(calificacion.tarea_tipo) }}
              </span>
            </div>
            
            <div class="calificacion-info">
              <div class="info-item">
                <span class="label">Asignatura:</span>
                <span class="value">{{ calificacion.asignatura_nombre }}</span>
              </div>
              <div class="info-item">
                <span class="label">Período:</span>
                <span class="value">{{ calificacion.periodo_nombre }}</span>
              </div>
              <div class="info-item">
                <span class="label">Fecha de calificación:</span>
                <span class="value">{{ formatFecha(calificacion.fecha_calificacion) }}</span>
              </div>
              <div class="info-item">
                <span class="label">Calificación:</span>
                <span class="calificacion-numero" :class="getCalificacionClass(calificacion.calificacion)">
                  {{ calificacion.calificacion.toFixed(1) }} / {{ getMaxPuntos(calificacion.tarea_tipo) }}
                </span>
              </div>
              
              <div v-if="calificacion.retroalimentacion" class="retroalimentacion">
                <div class="label">Retroalimentación:</div>
                <div class="content">{{ calificacion.retroalimentacion }}</div>
              </div>
            </div>
            
            <div class="calificado-por">
              <small>Calificado por: {{ calificacion.calificado_por_nombre }}</small>
            </div>
          </div>
        </div>
        
        <div class="resumen mt-4">
          <h4>Resumen de calificaciones</h4>
          <div class="resumen-grid">
            <div class="resumen-item">
              <div class="resumen-label">Promedio general:</div>
              <div class="resumen-value">{{ promedioGeneral.toFixed(2) }}</div>
            </div>
            <div class="resumen-item">
              <div class="resumen-label">Tareas calificadas:</div>
              <div class="resumen-value">{{ calificacionesFiltradas.length }}</div>
            </div>
            <div class="resumen-item">
              <div class="resumen-label">Mejor calificación:</div>
              <div class="resumen-value">{{ mejorCalificacion.toFixed(1) }}</div>
            </div>
            <div class="resumen-item">
              <div class="resumen-label">Peor calificación:</div>
              <div class="resumen-value">{{ peorCalificacion.toFixed(1) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import calificacionService from '@/services/calificacionService';

export default {
  name: 'MisCalificaciones',
  
  setup() {
    const authStore = useAuthStore();
    const loading = ref(true);
    const calificaciones = ref([]);
    const filtroAsignatura = ref('');
    const filtroPeriodo = ref('');
    
    // Cargar calificaciones del estudiante
    const cargarCalificaciones = async () => {
      try {
        loading.value = true;
        // En una implementación real, obtendríamos el ID del estudiante autenticado
        const estudianteId = authStore.user?.id;
        
        if (!estudianteId) {
          console.error('No se pudo obtener el ID del estudiante');
          return;
        }
        
        // En una implementación real, usaríamos el servicio para obtener las calificaciones
        // const response = await calificacionService.getCalificacionesEstudiante(estudianteId);
        // calificaciones.value = response.data;
        
        // Datos de ejemplo para la demostración
        calificaciones.value = [
          {
            id: 1,
            tarea_titulo: 'Tarea 1 - Introducción',
            tarea_tipo: 'ACD',
            asignatura_nombre: 'Matemáticas',
            periodo_nombre: '2023-1',
            calificacion: 2.3,
            fecha_calificacion: '2023-04-15T14:30:00Z',
            retroalimentacion: 'Buen trabajo en general, pero podrías profundizar más en los conceptos teóricos.',
            calificado_por_nombre: 'Prof. Juan Pérez'
          },
          {
            id: 2,
            tarea_titulo: 'Tarea 2 - Álgebra',
            tarea_tipo: 'AA',
            asignatura_nombre: 'Matemáticas',
            periodo_nombre: '2023-1',
            calificacion: 1.2,
            fecha_calificacion: '2023-05-20T10:15:00Z',
            retroalimentacion: 'Necesitas practicar más los ejercicios de factorización.',
            calificado_por_nombre: 'Prof. Juan Pérez'
          },
          {
            id: 3,
            tarea_titulo: 'Tarea 1 - Lectura',
            tarea_tipo: 'APE',
            asignatura_nombre: 'Literatura',
            periodo_nombre: '2023-1',
            calificacion: 0.8,
            fecha_calificacion: '2023-04-10T16:45:00Z',
            retroalimentacion: 'Excelente análisis de la obra literaria.',
            calificado_por_nombre: 'Prof. Ana Gómez'
          }
        ];
        
      } catch (error) {
        console.error('Error al cargar calificaciones:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // Filtrar calificaciones según los filtros seleccionados
    const calificacionesFiltradas = computed(() => {
      return calificaciones.value.filter(cal => {
        const cumpleAsignatura = !filtroAsignatura.value || 
                               cal.asignatura_nombre === filtroAsignatura.value;
        const cumplePeriodo = !filtroPeriodo.value || 
                            cal.periodo_nombre === filtroPeriodo.value;
        return cumpleAsignatura && cumplePeriodo;
      });
    });
    
    // Obtener lista única de asignaturas para el filtro
    const asignaturasUnicas = computed(() => {
      const asignaturas = new Set(calificaciones.value.map(c => c.asignatura_nombre));
      return Array.from(asignaturas).sort();
    });
    
    // Obtener lista única de períodos para el filtro
    const periodosUnicos = computed(() => {
      const periodos = new Set(calificaciones.value.map(c => c.periodo_nombre));
      return Array.from(periodos).sort().reverse();
    });
    
    // Calcular estadísticas
    const promedioGeneral = computed(() => {
      if (calificacionesFiltradas.value.length === 0) return 0;
      const suma = calificacionesFiltradas.value.reduce((acc, cal) => acc + cal.calificacion, 0);
      return suma / calificacionesFiltradas.value.length;
    });
    
    const mejorCalificacion = computed(() => {
      if (calificacionesFiltradas.value.length === 0) return 0;
      return Math.max(...calificacionesFiltradas.value.map(c => c.calificacion));
    });
    
    const peorCalificacion = computed(() => {
      if (calificacionesFiltradas.value.length === 0) return 0;
      return Math.min(...calificacionesFiltradas.value.map(c => c.calificacion));
    });
    
    // Funciones de utilidad
    const getTipoTarea = (tipo) => {
      const tipos = {
        'ACD': 'Actividad en Clase',
        'AA': 'Actividad Autónoma',
        'APE': 'Actividad de Proceso de Enseñanza'
      };
      return tipos[tipo] || tipo;
    };
    
    const getBadgeClass = (tipo) => {
      return {
        'badge-acd': tipo === 'ACD',
        'badge-aa': tipo === 'AA',
        'badge-ape': tipo === 'APE'
      };
    };
    
    const getCalificacionClass = (calificacion) => {
      if (calificacion >= 2.0) return 'excelente';
      if (calificacion >= 1.0) return 'bueno';
      return 'mejorable';
    };
    
    const getMaxPuntos = (tipo) => {
      const maxPuntos = {
        'ACD': 2.5,
        'AA': 1.5,
        'APE': 1.0
      };
      return maxPuntos[tipo] || 0;
    };
    
    const formatFecha = (fechaStr) => {
      if (!fechaStr) return '';
      const fecha = new Date(fechaStr);
      return fecha.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    };
    
    // Cargar datos al montar el componente
    onMounted(() => {
      cargarCalificaciones();
    });
    
    return {
      loading,
      calificaciones: calificacionesFiltradas,
      filtroAsignatura,
      filtroPeriodo,
      asignaturasUnicas,
      periodosUnicos,
      promedioGeneral,
      mejorCalificacion,
      peorCalificacion,
      getTipoTarea,
      getBadgeClass,
      getCalificacionClass,
      getMaxPuntos,
      formatFecha
    };
  }
};
</script>

<style scoped>
.mis-calificaciones {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading .spinner-border {
  margin-bottom: 15px;
}

.calificaciones-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.calificacion-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.calificacion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.calificacion-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.calificacion-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: #2c3e50;
  flex: 1;
}

.badge {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 0.75em;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-acd {
  background-color: #e3f2fd;
  color: #1565c0;
}

.badge-aa {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge-ape {
  background-color: #fff3e0;
  color: #e65100;
}

.calificacion-info {
  flex: 1;
}

.info-item {
  margin-bottom: 10px;
  display: flex;
  flex-wrap: wrap;
}

.label {
  font-weight: 600;
  color: #555;
  width: 140px;
  flex-shrink: 0;
}

.value {
  flex: 1;
  color: #333;
}

.calificacion-numero {
  font-weight: 700;
  font-size: 1.1em;
}

.calificacion-numero.excelente {
  color: #2e7d32; /* Verde para calificaciones altas */
}

.calificacion-numero.bueno {
  color: #f9a825; /* Amarillo/naranja para calificaciones medias */
}

.calificacion-numero.mejorable {
  color: #c62828; /* Rojo para calificaciones bajas */
}

.retroalimentacion {
  margin-top: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border-left: 3px solid #6c757d;
}

.retroalimentacion .label {
  font-style: italic;
  margin-bottom: 5px;
  width: 100%;
}

.retroalimentacion .content {
  line-height: 1.5;
}

.calificado-por {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px dashed #ddd;
  font-size: 0.85em;
  color: #666;
  text-align: right;
}

.resumen {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 30px;
}

.resumen h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #2c3e50;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 10px;
}

.resumen-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.resumen-item {
  background: white;
  padding: 15px;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.resumen-label {
  font-size: 0.9em;
  color: #6c757d;
  margin-bottom: 5px;
}

.resumen-value {
  font-size: 1.5em;
  font-weight: 600;
  color: #2c3e50;
}

/* Estilos para los filtros */
.filtros {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 0;
}

.form-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1em;
  background-color: white;
}

/* Estilos responsivos */
@media (max-width: 768px) {
  .calificaciones-container {
    grid-template-columns: 1fr;
  }
  
  .resumen-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 576px) {
  .resumen-grid {
    grid-template-columns: 1fr;
  }
  
  .info-item {
    flex-direction: column;
  }
  
  .label {
    width: 100%;
    margin-bottom: 2px;
  }
}
</style>
