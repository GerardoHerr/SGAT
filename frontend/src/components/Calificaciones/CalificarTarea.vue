<template>
  <div class="calificar-tarea">
    <h2>Calificar Tarea: {{ tarea.titulo }}</h2>
    
    <div v-if="loading" class="loading">Cargando estudiantes...</div>
    
    <div v-else>
      <div class="estudiantes-container">
        <div v-for="estudiante in estudiantes" :key="estudiante.id" class="estudiante-card">
          <div class="estudiante-header">
            <h3>{{ estudiante.nombre }} {{ estudiante.apellido }}</h3>
            <span class="email">{{ estudiante.email }}</span>
          </div>
          
          <div class="calificacion-form">
            <div class="form-group">
              <label>Calificación (0 - {{ maxPuntos }} puntos):</label>
              <input 
                type="number" 
                v-model.number="estudiante.calificacion" 
                :min="0" 
                :max="maxPuntos" 
                step="0.1"
                class="form-control"
                :class="{ 'is-invalid': estudiante.error }"
              >
              <div v-if="estudiante.error" class="invalid-feedback">
                {{ estudiante.error }}
              </div>
            </div>
            
            <div class="form-group">
              <label>Retroalimentación:</label>
              <textarea 
                v-model="estudiante.retroalimentacion" 
                class="form-control" 
                rows="3"
                placeholder="Escribe aquí tus comentarios..."
              ></textarea>
            </div>
            
            <button 
              @click="guardarCalificacion(estudiante)" 
              class="btn btn-primary"
              :disabled="guardando"
            >
              <span v-if="estudiante.guardando" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ estudiante.calificacionId ? 'Actualizar' : 'Guardar' }}
            </button>
            
            <div v-if="estudiante.mensaje" class="alert" :class="estudiante.exito ? 'alert-success' : 'alert-danger'" role="alert">
              {{ estudiante.mensaje }}
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="estudiantes.length === 0" class="alert alert-info">
        No hay estudiantes para calificar en esta tarea o ya han sido calificados todos.
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import calificacionService from '@/services/calificacionService';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'CalificarTarea',
  
  setup() {
    const route = useRoute();
    const authStore = useAuthStore();
    
    const tareaId = parseInt(route.params.tareaId);
    const tarea = ref({ titulo: 'Cargando...' });
    const estudiantes = ref([]);
    const loading = ref(true);
    const guardando = ref(false);
    const maxPuntos = ref(2.5); // Valor por defecto, se actualizará según el tipo de tarea
    
    // Cargar datos iniciales
    const cargarDatos = async () => {
      try {
        loading.value = true;
        
        // En una implementación real, aquí cargaríamos los detalles de la tarea
        // y los estudiantes sin calificar
        const [tareaData, estudiantesData] = await Promise.all([
          // Aquí iría la llamada para obtener los detalles de la tarea
          Promise.resolve({ id: tareaId, titulo: 'Título de la tarea', tipo: 'ACD' }), // Mock
          calificacionService.getEstudiantesSinCalificar(tareaId)
        ]);
        
        tarea.value = tareaData;
        
        // Configurar el máximo de puntos según el tipo de tarea
        if (tareaData.tipo === 'ACD') maxPuntos.value = 2.5;
        else if (tareaData.tipo === 'AA') maxPuntos.value = 1.5;
        else if (tareaData.tipo === 'APE') maxPuntos.value = 1.0;
        
        // Procesar estudiantes
        estudiantes.value = estudiantesData.estudiantes_sin_calificar.map(est => ({
          ...est,
          calificacion: null,
          retroalimentacion: '',
          calificacionId: null,
          guardando: false,
          error: '',
          mensaje: '',
          exito: false
        }));
        
      } catch (error) {
        console.error('Error al cargar datos:', error);
      } finally {
        loading.value = false;
      }
    };
    
    // Guardar calificación de un estudiante
    const guardarCalificacion = async (estudiante) => {
      // Validar calificación
      if (estudiante.calificacion === null || estudiante.calificacion === '') {
        estudiante.error = 'La calificación es requerida';
        return;
      }
      
      const calificacion = parseFloat(estudiante.calificacion);
      if (isNaN(calificacion) || calificacion < 0 || calificacion > maxPuntos.value) {
        estudiante.error = `La calificación debe estar entre 0 y ${maxPuntos.value}`;
        return;
      }
      
      estudiante.error = '';
      estudiante.guardando = true;
      
      try {
        const calificacionData = {
          tarea: tareaId,
          estudiante: estudiante.id,
          calificacion: calificacion,
          retroalimentacion: estudiante.retroalimentacion || '',
          id: estudiante.calificacionId || null
        };
        
        const resultado = await calificacionService.guardarCalificacion(calificacionData);
        
        // Actualizar el estado local
        estudiante.calificacionId = resultado.id;
        estudiante.mensaje = 'Calificación guardada correctamente';
        estudiante.exito = true;
        
        // Opcional: Eliminar el mensaje después de unos segundos
        setTimeout(() => {
          estudiante.mensaje = '';
        }, 3000);
        
      } catch (error) {
        console.error('Error al guardar la calificación:', error);
        estudiante.mensaje = 'Error al guardar la calificación';
        estudiante.exito = false;
      } finally {
        estudiante.guardando = false;
      }
    };
    
    // Cargar datos al montar el componente
    onMounted(() => {
      cargarDatos();
    });
    
    return {
      tarea,
      estudiantes,
      loading,
      guardando,
      maxPuntos,
      guardarCalificacion
    };
  }
};
</script>

<style scoped>
.calificar-tarea {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.estudiantes-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.estudiante-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.2s;
}

.estudiante-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.estudiante-header {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.estudiante-header h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.email {
  color: #666;
  font-size: 0.9em;
}

.calificacion-form {
  margin-top: 15px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}

textarea.form-control {
  min-height: 80px;
  resize: vertical;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95em;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.alert {
  padding: 10px 15px;
  border-radius: 4px;
  margin-top: 10px;
  font-size: 0.9em;
}

.alert-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.alert-info {
  background-color: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.invalid-feedback {
  color: #dc3545;
  font-size: 0.85em;
  margin-top: 5px;
}

.is-invalid {
  border-color: #dc3545;
}

.loading {
  text-align: center;
  padding: 20px;
  font-style: italic;
  color: #666;
}
</style>
