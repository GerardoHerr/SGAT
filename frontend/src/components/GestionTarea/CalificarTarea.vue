<template>
  <div class="calificar-tarea">
    <h2>Entregas de la Tarea</h2>
    <div v-if="loading">Cargando entregas...</div>
    <div v-else>
      <div v-if="entregas.length === 0" class="no-entregas">No hay entregas registradas para esta tarea.</div>
      <ul v-else>
        <li v-for="entrega in entregasFiltradas" :key="entrega.id" class="entrega-item">
          <div class="entrega-header">
            <template v-if="entrega.grupo">
              <strong>Grupo: {{ entrega.grupo_nombre || 'ID ' + entrega.grupo }}</strong><br>
              <span v-if="entrega.estudiantesGrupo && entrega.estudiantesGrupo.length">
                <span>Integrantes: </span>
                <span v-for="(est, idx) in entrega.estudiantesGrupo" :key="est.email">
                  {{ est.nombre }} {{ est.apellido }}<span v-if="idx < entrega.estudiantesGrupo.length - 1">, </span>
                </span>
              </span>
              <span v-else>Cargando integrantes...</span>
            </template>
            <template v-else>
              <strong>{{ entrega.estudiante_nombre || entrega.estudiante_email }}</strong>
            </template>
            <span class="fecha-entrega">
              {{ entrega.fecha_entrega | fecha }}
            </span>
          </div>

          <!-- Mostrar calificación y retroalimentación existente -->
          <div v-if="!entrega.editando" class="calificacion-info">
            <div class="calificacion-display">
              <div class="calificacion-header">
                <strong>Calificación: {{ entrega.calificacion || 'Sin calificar' }}</strong>
                <button @click="habilitarEdicion(entrega)" class="btn-editar">
                  <i class="fas fa-edit"></i> Editar
                </button>
              </div>
              
              <div v-if="entrega.observaciones" class="observaciones">
                <strong>Observaciones:</strong> {{ entrega.observaciones }}
              </div>
              
              <div v-if="entrega.retroalimentacion_archivo_url" class="retroalimentacion-archivo">
                <a :href="entrega.retroalimentacion_archivo_url" target="_blank" class="archivo-link">
                  <i class="fas fa-file-pdf"></i> Ver retroalimentación
                </a>
                <span v-if="entrega.fecha_retroalimentacion" class="fecha-retro">
                  ({{ new Date(entrega.fecha_retroalimentacion).toLocaleDateString() }})
                </span>
              </div>
            </div>
          </div>

          <!-- Formulario de calificación -->
          <div v-else class="calificacion-form">
            <div class="form-group">
              <label for="calificacion">Calificación</label>
              <input 
                id="calificacion"
                v-model.number="entrega.calificacionInput" 
                type="number" 
                step="0.01" 
                min="0" 
                max="2.5" 
                placeholder="0.00" 
                class="input-calif" 
                @keyup.enter="calificarEntrega(entrega)"
              />
            </div>
            
            <div class="form-group">
              <label for="observaciones">Observaciones</label>
              <textarea
                id="observaciones"
                v-model="entrega.observacionesInput" 
                placeholder="Escribe aquí tus comentarios..." 
                class="input-obs"
                rows="3"
              ></textarea>
            </div>
            
            <div class="form-group">
              <label>Retroalimentación</label>
              <div class="file-upload-container">
                <label for="retroalimentacion-archivo" class="file-upload">
                  <i class="fas fa-upload"></i>
                  {{ entrega.archivoRetroalimentacion ? entrega.archivoRetroalimentacion.name : 'Subir retroalimentación (PDF)' }}
                  <input 
                    id="retroalimentacion-archivo"
                    type="file" 
                    accept=".pdf"
                    @change="onFileChange($event, entrega)"
                    style="display: none;"
                  />
                </label>
                <small v-if="entrega.archivoRetroalimentacion" class="file-info">
                  {{ entrega.archivoRetroalimentacion.name }} ({{ (entrega.archivoRetroalimentacion.size / 1024).toFixed(2) }} KB)
                  <button 
                    type="button" 
                    @click.stop="entrega.archivoRetroalimentacion = null"
                    class="btn-remove-file"
                    title="Eliminar archivo"
                  >
                    <i class="fas fa-times"></i>
                  </button>
                </small>
                <small v-if="entrega.retroalimentacion_archivo_url && !entrega.archivoRetroalimentacion" class="file-info">
                  Archivo actual: 
                  <a :href="entrega.retroalimentacion_archivo_url" target="_blank" class="archivo-link">
                    Ver archivo actual
                  </a>
                  <button 
                    type="button" 
                    @click.stop="eliminarArchivoRetroalimentacion(entrega)"
                    class="btn-remove-file"
                    title="Eliminar archivo"
                  >
                    <i class="fas fa-trash"></i> Eliminar
                  </button>
                </small>
              </div>
            </div>
            
            <div class="form-actions">
              <button 
                @click="calificarEntrega(entrega)" 
                :disabled="entrega.guardando || (!entrega.calificacionInput && !entrega.observacionesInput && !entrega.archivoRetroalimentacion)"
                class="btn-guardar"
              >
                <i v-if="entrega.guardando" class="fas fa-spinner fa-spin"></i>
                {{ entrega.guardando ? 'Guardando...' : 'Guardar' }}
              </button>
              <button 
                @click="cancelarEdicion(entrega)" 
                class="btn-cancelar"
                :disabled="entrega.guardando"
              >
                Cancelar
              </button>
            </div>
            
            <div v-if="entrega.error" class="error-message">
              <i class="fas fa-exclamation-circle"></i> {{ entrega.error }}
            </div>
            <div v-if="entrega.exito" class="success-message">
              <i class="fas fa-check-circle"></i> ¡Calificación guardada correctamente!
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'CalificarTarea',
  props: {
    id: {
      type: [String, Number],
      required: false
    }
  },
  data() {
    return {
      entregas: [],
      loading: true,
      tareaIdLocal: null
    };
  },
  computed: {
    entregasFiltradas() {
      const entregasPorGrupo = {};
      const entregasSinGrupo = [];
      
      for (const entrega of this.entregas) {
        if (entrega.grupo) {
          if (!entregasPorGrupo[entrega.grupo]) {
            entregasPorGrupo[entrega.grupo] = entrega;
          }
        } else {
          entregasSinGrupo.push(entrega);
        }
      }
      
      return [...Object.values(entregasPorGrupo), ...entregasSinGrupo];
    }
  },
  async mounted() {
    let tareaId = this.id;
    if (!tareaId && this.$route?.params?.id) {
      tareaId = this.$route.params.id;
    }
    this.tareaIdLocal = tareaId;
    
    try {
      await this.cargarEntregas();
      await this.cargarEstudiantesDeGrupos();
    } catch (error) {
      console.error('Error al cargar datos:', error);
    }
    
    // Inicializar inputs para edición
    this.entregas.forEach(e => {
      e.calificacionInput = e.calificacion;
      e.observacionesInput = e.observaciones;
      e.guardando = false;
      e.error = '';
      e.exito = false;
    });
  },
  methods: {
    async cargarEntregas() {
      this.loading = true;
      try {
        const response = await api.get(`entregas/?tarea_id=${this.tareaIdLocal}`);
        this.entregas = response.data.map(entrega => ({
          ...entrega,
          calificacionInput: entrega.calificacion,
          observacionesInput: entrega.observaciones || '',
          archivoRetroalimentacion: null,
          guardando: false,
          error: '',
          exito: false,
          editando: false,
          estudiantesGrupo: entrega.estudiantesGrupo || []
        }));
      } catch (error) {
        console.error('Error al cargar entregas:', error);
        this.entregas = [];
      } finally {
        this.loading = false;
      }
    },
    
    async cargarEstudiantesDeGrupos() {
      const gruposIds = [...new Set(this.entregas
        .filter(e => e.grupo)
        .map(e => e.grupo)
      )];
      
      await Promise.all(gruposIds.map(async (grupoId) => {
        try {
          const { data } = await api.get(`grupos/${grupoId}/`);
          const estudiantes = data.estudiantes || [];
          
          this.entregas = this.entregas.map(e => 
            e.grupo === grupoId 
              ? { ...e, estudiantesGrupo: estudiantes, grupo_nombre: data.nombre || null }
              : e
          );
        } catch (err) {
          console.error(`Error cargando grupo ${grupoId}:`, err);
          this.entregas = this.entregas.map(e => 
            e.grupo === grupoId 
              ? { ...e, estudiantesGrupo: [], grupo_nombre: null }
              : e
          );
        }
      }));
    },
    
    onFileChange(event, entrega) {
      const file = event.target.files[0];
      if (!file) return;
      
      if (file.type !== 'application/pdf') {
        entrega.error = 'Por favor, sube un archivo en formato PDF.';
        return;
      }
      
      if (file.size > 5 * 1024 * 1024) { // 5MB
        entrega.error = 'El archivo es demasiado grande. El tamaño máximo permitido es de 5MB.';
        return;
      }
      
      entrega.archivoRetroalimentacion = file;
      entrega.error = '';
    },
    
    async eliminarArchivoRetroalimentacion(entrega) {
      if (!confirm('¿Estás seguro de que deseas eliminar el archivo de retroalimentación?')) {
        return;
      }
      
      try {
        entrega.guardando = true;
        entrega.error = '';
        
        await api.delete(`entregas/${entrega.id}/eliminar-retroalimentacion/`);
        
        // Actualizar la interfaz
        entrega.retroalimentacion_archivo_url = null;
        entrega.fecha_retroalimentacion = null;
        entrega.exito = 'Archivo de retroalimentación eliminado correctamente';
        
        setTimeout(() => {
          entrega.exito = '';
        }, 3000);
        
      } catch (error) {
        console.error('Error al eliminar archivo de retroalimentación:', error);
        entrega.error = error.response?.data?.error || 'Error al eliminar el archivo de retroalimentación';
      } finally {
        entrega.guardando = false;
      }
    },
    
    async calificarEntrega(entrega) {
      // Validaciones
      if (!entrega.calificacionInput && entrega.calificacionInput !== 0 && !entrega.observacionesInput && !entrega.archivoRetroalimentacion) {
        entrega.error = 'Debes proporcionar al menos una calificación, observaciones o un archivo de retroalimentación.';
        return;
      }
      
      if (entrega.calificacionInput !== null && entrega.calificacionInput !== undefined) {
        const maxCalif = 2.5;
        if (entrega.calificacionInput < 0 || entrega.calificacionInput > maxCalif) {
          entrega.error = `La calificación debe estar entre 0 y ${maxCalif}`;
          return;
        }
      }
      
      entrega.error = '';
      entrega.exito = false;
      entrega.guardando = true;
      
      try {
        const formData = new FormData();
        
        // Agregar datos al formData solo si están presentes
        if (entrega.calificacionInput !== null && entrega.calificacionInput !== undefined) {
          formData.append('calificacion', parseFloat(entrega.calificacionInput));
        }
        
        if (entrega.observacionesInput) {
          formData.append('observaciones', entrega.observacionesInput);
        }
        
        if (entrega.archivoRetroalimentacion) {
          formData.append('retroalimentacion_archivo', entrega.archivoRetroalimentacion);
        }
        
        // Configuración para enviar archivos
        const config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        
        // Realizar la petición
        const response = await api.patch(`entregas/${entrega.id}/`, formData, config);
        
        // Actualizar los datos de la entrega con la respuesta del servidor
        Object.assign(entrega, response.data);
        
        // Limpiar el archivo temporal
        entrega.archivoRetroalimentacion = null;
        
        // Salir del modo edición
        entrega.editando = false;
        
        // Mostrar mensaje de éxito
        entrega.exito = true;
        setTimeout(() => {
          entrega.exito = false;
        }, 3000);
        
      } catch (error) {
        console.error('Error al guardar calificación:', error);
        
        let errorMessage = 'Error al guardar la calificación';
        if (error.response) {
          // Si el servidor devuelve un mensaje de error, usarlo
          if (error.response.data) {
            if (typeof error.response.data === 'object') {
              errorMessage = Object.values(error.response.data).flat().join(' ');
            } else {
              errorMessage = error.response.data;
            }
          }
        }
        
        entrega.error = errorMessage;
      } finally {
        entrega.guardando = false;
      }
    },
    
    habilitarEdicion(entrega) {
      entrega.calificacionInput = entrega.calificacion;
      entrega.observacionesInput = entrega.observaciones || '';
      entrega.archivoRetroalimentacion = null;
      entrega.editando = true;
      entrega.error = '';
      entrega.exito = false;
    },
    
    cancelarEdicion(entrega) {
      // Restaurar los valores originales
      if (entrega.calificacion !== null && entrega.calificacion !== undefined) {
        entrega.calificacionInput = entrega.calificacion;
        entrega.observacionesInput = entrega.observaciones || '';
        entrega.editando = false;
      } else {
        // Si no tenía calificación previa, volver al estado inicial
        entrega.calificacionInput = null;
        entrega.observacionesInput = '';
      }
      
      // Limpiar archivo temporal
      entrega.archivoRetroalimentacion = null;
      
      // Limpiar mensajes
      entrega.error = '';
      entrega.exito = false;
    }
  },
  filters: {
    fecha(val) {
      if (!val) return '';
      return new Date(val).toLocaleString();
    }
  },
  
  created() {
    // Inicializar las propiedades necesarias al crear el componente
    this.entregas = this.entregas.map(entrega => ({
      ...entrega,
      calificacionInput: entrega.calificacion,
      observacionesInput: entrega.observaciones || '',
      archivoRetroalimentacion: null,
      guardando: false,
      editando: false,
      error: '',
      exito: false,
      estudiantesGrupo: entrega.estudiantesGrupo || []
    }));
  }
};
</script>

<style scoped>
.calificar-tarea {
  background-color: #ffffff;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  color: #333333;
  padding: 2.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 80vh;
  box-sizing: border-box;
}

.calificar-tarea > * {
  max-width: 100%;
  overflow-x: hidden;
}

h2 {
  color: #2e7d32;
  margin: 0 0 2rem 0;
  font-size: 1.8em;
  text-align: center;
  padding-bottom: 1rem;
  font-weight: 600;
  position: relative;
}

h2:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: #4caf50;
}

.loading {
  text-align: center;
  color: #666;
  padding: 20px;
}

.no-entregas {
  text-align: center;
  color: #2e7d32;
  padding: 24px;
  background-color: #f1f8e9;
  border-radius: 8px;
  margin: 24px 0;
  border: 2px dashed #a5d6a7;
  line-height: 1.6;
}

ul {
  list-style: none;
  padding: 0;
  margin: 2rem 0 0;
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
}

.entrega-item {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
}

.entrega-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background-color: #4caf50;
}

.entrega-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  flex-wrap: wrap;
  gap: 10px;
  color: #DDD0C8;
}

.entrega-header strong {
  color: #323232;
  font-size: 1.1em;
  margin-right: 10px;
}

.fecha-entrega {
  color: #616161;
  font-size: 0.85em;
  background: #f5f5f5;
  padding: 4px 12px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  font-weight: 500;
}

.entrega-item:hover {
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.2);
  transform: translateY(-2px);
  border-color: #a5d6a7;
  background: #ffffff;
}

.calificacion-info {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #323232;
  color: #323232;
}

.calificacion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  color: #323232;
}

.calificacion-display {
  line-height: 1.6;
}

.observaciones {
  display: block;
  margin: 16px 0;
  padding: 14px 16px;
  background-color: #f5f5f5;
  border-left: 4px solid #81c784;
  border-radius: 0 4px 4px 0;
  color: #424242;
  line-height: 1.6;
  font-size: 0.95em;
}

.retroalimentacion-archivo {
  margin-top: 12px;
  padding-top: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.error-message i,
.success-message i {
  font-size: 1.2em;
}

.error-message {
  color: #c62828;
  background-color: #ffebee;
  border: 1px solid #ef9a9a;
  padding: 12px 16px;
  border-radius: 4px;
  margin: 16px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95em;
  line-height: 1.5;
  border-left: 4px solid #f44336;
}

.success-message {
  color: #1b5e20;
  background-color: #e8f5e9;
  border: 1px solid #a5d6a7;
  padding: 12px 16px;
  border-radius: 4px;
  margin: 16px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95em;
  line-height: 1.5;
  border-left: 4px solid #4caf50;
}

.input-calif,
.input-obs,
.file-upload {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 0.95em;
  transition: all 0.2s ease;
  background-color: #fff;
  color: #333;
}

.input-calif {
  max-width: 100px;
  text-align: center;
  font-weight: 500;
}

.input-calif:focus,
.input-obs:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
}

.input-obs {
  min-height: 100px;
  resize: vertical;
  line-height: 1.5;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #424242;
  font-size: 0.95em;
}

.btn-editar {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-editar:hover {
  background-color: #388e3c;
  transform: translateY(-1px);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

.calificacion-form {
  animation: fadeIn 0.3s ease-out;
  background: #f8f9fa;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-left: 4px solid #4caf50;
}

@media (max-width: 768px) {
  .calificar-tarea {
    padding: 1rem;
  }
  
  .entrega-header {
    flex-direction: column;
    gap: 8px;
  }
  
  .fecha-entrega {
    align-self: flex-start;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 8px;
  }
  
  .btn-guardar,
  .btn-cancelar {
    width: 100%;
  }
  
  .input-calif {
    max-width: 100%;
  }
}
</style>
