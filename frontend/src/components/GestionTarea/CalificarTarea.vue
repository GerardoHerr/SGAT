<template>
  <div class="calificar-tarea">
    <div class="header-actions">
      <router-link to="/docente/cursos" class="back-button">
        <i class="fas fa-arrow-left"></i> Volver a Cursos
      </router-link>
      <div class="page-header">
        <h2>Entregas de la Tarea</h2>
        <div v-if="tarea" class="tarea-info">
          <span class="tarea-tipo">
            <i class="fas fa-tag"></i>
            {{ tarea.tipo }} - Calificación máxima: {{ maxCalificacion }}
          </span>
        </div>
        <div class="entregas-stats" v-if="!loading && entregas.length > 0">
          <span class="stat-item">
            <i class="fas fa-clipboard-list"></i>
            {{ entregasFiltradas.length }} entregas
          </span>
          <span class="stat-item">
            <i class="fas fa-check-circle"></i>
            {{ entregasCalificadas }} calificadas
          </span>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i>
        <span>Cargando entregas...</span>
      </div>
    </div>

    <div v-else>
      <div v-if="entregas.length === 0" class="no-entregas">
        <i class="fas fa-inbox"></i>
        <h3>No hay entregas registradas</h3>
        <p>Aún no se han registrado entregas para esta tarea.</p>
      </div>

      <div v-else class="entregas-grid">
        <div v-for="entrega in entregasFiltradas" :key="entrega.id" class="entrega-card">
          <!-- Header de la entrega -->
          <div class="entrega-header">
            <div class="estudiante-info">
              <template v-if="entrega.grupo">
                <div class="grupo-badge">
                  <i class="fas fa-users"></i>
                  <span>{{ entrega.grupo_nombre || 'Grupo ID ' + entrega.grupo }}</span>
                </div>
                <div class="integrantes-list" v-if="entrega.estudiantesGrupo && entrega.estudiantesGrupo.length">
                  <div class="integrantes-header">
                    <i class="fas fa-user-friends"></i>
                    <span>Integrantes:</span>
                  </div>
                  <div class="integrantes-tags">
                    <span v-for="est in entrega.estudiantesGrupo" :key="est.email" class="integrante-tag">
                      {{ est.nombre }} {{ est.apellido }}
                    </span>
                  </div>
                </div>
                <div v-else class="loading-integrantes">
                  <i class="fas fa-spinner fa-spin"></i>
                  <span>Cargando integrantes...</span>
                </div>
              </template>
              <template v-else>
                <div class="estudiante-individual">
                  <i class="fas fa-user"></i>
                  <span>{{ entrega.estudiante_nombre || entrega.estudiante_email }}</span>
                </div>
              </template>
            </div>
            
            <div class="entrega-status">
              <div class="status-badge" :class="{ 'calificada': entrega.calificacion !== null && entrega.calificacion !== undefined }">
                <i :class="entrega.calificacion !== null && entrega.calificacion !== undefined ? 'fas fa-check-circle' : 'fas fa-clock'"></i>
                <span>{{ entrega.calificacion !== null && entrega.calificacion !== undefined ? 'Calificada' : 'Pendiente' }}</span>
              </div>
            </div>
          </div>

          <!-- Información del archivo entregado -->
          <div class="archivo-entregado">
            <div class="archivo-info">
              <div class="archivo-item">
                <i class="fas fa-file-pdf"></i>
                <div class="archivo-details">
                  <span class="archivo-label">Archivo entregado:</span>
                  <div class="archivo-actions">
                    <a v-if="entrega.archivo" :href="entrega.archivo" target="_blank" class="archivo-link">
                      <i class="fas fa-external-link-alt"></i>
                      Ver archivo
                    </a>
                    <span v-else class="no-archivo">Sin archivo</span>
                    <span class="fecha-entrega" v-if="entrega.fecha_entregada">
                      {{ new Date(entrega.fecha_entregada).toLocaleString() }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sección de calificación -->
          <div class="calificacion-section">
            <div v-if="!entrega.editando" class="calificacion-display">
              <div class="calificacion-info-grid">
                <div class="calificacion-item">
                  <label>Calificación:</label>
                  <div class="calificacion-value">
                    <span v-if="entrega.calificacion !== null && entrega.calificacion !== undefined" class="calificacion-numero">
                      {{ entrega.calificacion }}
                    </span>
                    <span v-else class="sin-calificacion">Sin calificar</span>
                  </div>
                </div>

                <div class="calificacion-item" v-if="entrega.observaciones">
                  <label>Observaciones:</label>
                  <div class="observaciones-content">
                    {{ entrega.observaciones }}
                  </div>
                </div>

                <div class="calificacion-item" v-if="entrega.retroalimentacion_archivo_url">
                  <label>Retroalimentación:</label>
                  <div class="retroalimentacion-content">
                    <a :href="entrega.retroalimentacion_archivo_url" target="_blank" class="retroalimentacion-link">
                      <i class="fas fa-file-pdf"></i>
                      Ver retroalimentación
                    </a>
                    <span v-if="entrega.fecha_retroalimentacion" class="fecha-retro">
                      {{ new Date(entrega.fecha_retroalimentacion).toLocaleString() }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="calificacion-actions">
                <button @click="habilitarEdicion(entrega)" class="btn-editar">
                  <i class="fas fa-edit"></i>
                  {{ entrega.calificacion !== null && entrega.calificacion !== undefined ? 'Editar' : 'Calificar' }}
                </button>
              </div>
            </div>

            <!-- Formulario de calificación -->
            <div v-else class="calificacion-form">
              <div class="form-header">
                <h4>
                  <i class="fas fa-clipboard-check"></i>
                  {{ entrega.calificacion !== null && entrega.calificacion !== undefined ? 'Editar Calificación' : 'Nueva Calificación' }}
                </h4>
              </div>

              <div class="form-grid">
                <div class="form-group">
                  <label for="calificacion">
                    <i class="fas fa-star"></i>
                    Calificación
                  </label>
                  <div class="input-wrapper">
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
                    <span class="input-suffix">
                      / {{ Number(maxCalificacion).toFixed(1) }}
                    </span>
                  </div>
                </div>
                
                <div class="form-group full-width">
                  <label for="observaciones">
                    <i class="fas fa-comment-alt"></i>
                    Observaciones
                  </label>
                  <textarea
                    id="observaciones"
                    v-model="entrega.observacionesInput" 
                    placeholder="Escribe aquí tus comentarios y retroalimentación..." 
                    class="input-obs"
                    rows="4"
                  ></textarea>
                </div>
                
                <div class="form-group full-width">
                  <label>
                    <i class="fas fa-upload"></i>
                    Archivo de Retroalimentación
                  </label>
                  <div class="file-upload-area">
                    <label for="retroalimentacion-archivo" class="file-upload-label">
                      <div class="upload-content">
                        <i class="fas fa-cloud-upload-alt"></i>
                        <span class="upload-text">
                          {{ entrega.archivoRetroalimentacion ? entrega.archivoRetroalimentacion.name : 'Subir archivo PDF' }}
                        </span>
                        <span class="upload-hint">Máximo 5MB</span>
                      </div>
                      <input 
                        id="retroalimentacion-archivo"
                        type="file" 
                        accept=".pdf"
                        @change="onFileChange($event, entrega)"
                        style="display: none;"
                      />
                    </label>
                    
                    <div v-if="entrega.archivoRetroalimentacion" class="file-selected">
                      <div class="file-info">
                        <i class="fas fa-file-pdf"></i>
                        <div class="file-details">
                          <span class="file-name">{{ entrega.archivoRetroalimentacion.name }}</span>
                          <span class="file-size">{{ (entrega.archivoRetroalimentacion.size / 1024).toFixed(2) }} KB</span>
                        </div>
                        <button 
                          type="button" 
                          @click.stop="entrega.archivoRetroalimentacion = null"
                          class="btn-remove-file"
                          title="Eliminar archivo"
                        >
                          <i class="fas fa-times"></i>
                        </button>
                      </div>
                    </div>

                    <div v-if="entrega.retroalimentacion_archivo_url && !entrega.archivoRetroalimentacion" class="file-current">
                      <div class="current-file-info">
                        <i class="fas fa-file-pdf"></i>
                        <div class="current-file-details">
                          <span class="current-file-label">Archivo actual:</span>
                          <a :href="entrega.retroalimentacion_archivo_url" target="_blank" class="current-file-link">
                            Ver archivo actual
                          </a>
                        </div>
                        <button 
                          type="button" 
                          @click.stop="eliminarArchivoRetroalimentacion(entrega)"
                          class="btn-remove-current"
                          title="Eliminar archivo actual"
                        >
                          <i class="fas fa-trash"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="form-actions">
                <button 
                  @click="calificarEntrega(entrega)" 
                  :disabled="entrega.guardando || (!entrega.calificacionInput && !entrega.observacionesInput && !entrega.archivoRetroalimentacion)"
                  class="btn-guardar"
                >
                  <i v-if="entrega.guardando" class="fas fa-spinner fa-spin"></i>
                  <i v-else class="fas fa-save"></i>
                  {{ entrega.guardando ? 'Guardando...' : 'Guardar Calificación' }}
                </button>
                <button 
                  @click="cancelarEdicion(entrega)" 
                  class="btn-cancelar"
                  :disabled="entrega.guardando"
                >
                  <i class="fas fa-times"></i>
                  Cancelar
                </button>
              </div>
              
              <div v-if="entrega.error" class="message error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <span>{{ entrega.error }}</span>
              </div>
              <div v-if="entrega.exito" class="message success-message">
                <i class="fas fa-check-circle"></i>
                <span>¡Calificación guardada correctamente!</span>
              </div>
            </div>
          </div>
        </div>
      </div>
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
    },
    tipo_tarea: {
      type: String,
      required: false
    }
  },
  data() {
    return {
      entregas: [],
      loading: true,
      tareaIdLocal: null,
      tarea: null,
      tipoTareaLocal: null
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
    },
    entregasCalificadas() {
      return this.entregasFiltradas.filter(e => e.calificacion !== null && e.calificacion !== undefined).length;
    },
    maxCalificacion() {
      // Si la tarea está cargada, usar su tipo
      let tipo = this.tarea?.tipo || this.tipoTareaLocal;
      if (!tipo) return 2.5;
      switch (tipo) {
        case 'AA':
        case 'ACD':
          return 2.0;
        case 'APE':
          return 2.5;
        default:
          return 2.5;
      }
    }
  },
  async mounted() {
    let tareaId = this.id || this.$route?.params?.id;
    let tipoTarea = this.tipo_tarea || this.$route?.params?.tipo_tarea;
    console.log('ID de tarea:', tareaId, 'Tipo de tarea:', tipoTarea ? tipoTarea : '(vacío)');
    this.tareaIdLocal = tareaId;
    this.tipoTareaLocal = tipoTarea;
    try {
      await this.cargarTarea();
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
    async cargarTarea() {
      try {
        const response = await api.get(`tareas/${this.tareaIdLocal}/`);
        this.tarea = response.data;
        console.log('Tarea cargada:', this.tarea);
      } catch (error) {
        console.error('Error al cargar tarea:', error);
        this.tarea = null;
      }
    },
    
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
        console.log('Entregas cargadas:', this.entregas);
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
      if (!entrega.calificacionInput && entrega.calificacionInput !== 0 && !entrega.observacionesInput && !entrega.archivoRetroalimentacion) {
        entrega.error = 'Debes proporcionar al menos una calificación, observaciones o un archivo de retroalimentación.';
        return;
      }

      if (entrega.calificacionInput !== null && entrega.calificacionInput !== undefined) {
        const max = Number(this.maxCalificacion).toFixed(1);
        if (entrega.calificacionInput < 0 || entrega.calificacionInput > this.maxCalificacion) {
          entrega.error = `La calificación debe estar entre 0 y ${max}`;
          return;
        }
      }

      entrega.error = '';
      entrega.exito = false;
      entrega.guardando = true;

      try {
        const formData = new FormData();
        if (entrega.calificacionInput !== null && entrega.calificacionInput !== undefined) {
          formData.append('calificacion', parseFloat(entrega.calificacionInput));
        }
        if (entrega.observacionesInput) {
          formData.append('observaciones', entrega.observacionesInput);
        }
        if (entrega.archivoRetroalimentacion) {
          formData.append('retroalimentacion_archivo', entrega.archivoRetroalimentacion);
        }
        const config = {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        };
        const response = await api.post(`entregas/${entrega.id}/calificar/`, formData, config);
        if (response.data && response.data.data) {
          const d = response.data.data;
          // Buscar el objeto entrega en el array original y actualizar sus propiedades
          const entregaOriginal = this.entregas.find(e => e.id === entrega.id);
          if (entregaOriginal) {
            entregaOriginal.calificacion = d.calificacion;
            entregaOriginal.calificacionInput = d.calificacion;
            entregaOriginal.observaciones = d.observaciones;
            entregaOriginal.observacionesInput = d.observaciones;
            entregaOriginal.retroalimentacion_archivo_url = d.retroalimentacion_archivo || null;
            entregaOriginal.fecha_retroalimentacion = d.fecha_retroalimentacion || null;
            entregaOriginal.archivoRetroalimentacion = null;
            entregaOriginal.editando = false;
            entregaOriginal.exito = true;
            entregaOriginal.guardando = false;
            entregaOriginal.error = '';
            setTimeout(() => {
              entregaOriginal.exito = false;
            }, 3000);
          }
        }
      } catch (error) {
        console.error('Error al guardar calificación:', error);
        let errorMessage = 'Error al guardar la calificación';
        if (error.response) {
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
      if (entrega.calificacion !== null && entrega.calificacion !== undefined) {
        entrega.calificacionInput = entrega.calificacion;
        entrega.observacionesInput = entrega.observaciones || '';
        entrega.editando = false;
      } else {
        entrega.calificacionInput = null;
        entrega.observacionesInput = '';
      }
      
      entrega.archivoRetroalimentacion = null;
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

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.calificar-tarea {
  background-color: #f8f9fa;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  color: #333333;
  padding: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  box-sizing: border-box;
}

.header-actions {
  margin-bottom: 2rem;
  
  .back-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #ffffff;
    color: #2e7d32;
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    margin-bottom: 1.5rem;
    transition: all 0.2s ease;
    border: 1px solid #e0e0e0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    
    &:hover {
      background: #e8f0fe;
      border-color: #4a6cf7;
      transform: translateY(-1px);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    i {
      font-size: 0.9em;
    }
  }
}

.page-header {
  background: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e0e0e0;
  
  h2 {
    color: #1a365d;
    margin: 0 0 1rem 0;
    font-size: 2rem;
    font-weight: 600;
    text-align: center;
  }
  
  .tarea-info {
    text-align: center;
    margin-bottom: 1rem;
    
    .tarea-tipo {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: #e3f2fd;
      color: #1976d2;
      padding: 0.5rem 1rem;
      border-radius: 20px;
      font-weight: 500;
      border: 1px solid #bbdefb;
      font-size: 0.95rem;
      
      i {
        font-size: 0.9em;
      }
    }
  }
  
  .entregas-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
    
    .stat-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #4a5568;
      font-weight: 500;
      
      i {
        color: #4a6cf7;
        font-size: 1.1em;
      }
    }
  }
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
    color: #4a6cf7;
    
    i {
      font-size: 2rem;
    }
    
    span {
      font-size: 1.1rem;
      font-weight: 500;
    }
  }
}

.no-entregas {
  text-align: center;
  color: #2e7d32;
  padding: 3rem;
  background-color: #ffffff;
  border-radius: 12px;
  margin: 2rem 0;
  border: 2px dashed #a5d6a7;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  
  i {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #4caf50;
  }
  
  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    color: #1a365d;
  }
  
  p {
    margin: 0;
    color: #666666;
    font-size: 1.1rem;
  }
}

.entregas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.entrega-card {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background-color: #4caf50;
  }
  
  &:hover {
    box-shadow: 0 8px 25px rgba(76, 175, 80, 0.15);
    transform: translateY(-2px);
    border-color: #a5d6a7;
  }
}

.entrega-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.estudiante-info {
  flex: 1;
  
  .grupo-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-weight: 500;
    margin-bottom: 0.75rem;
    border: 1px solid #bbdefb;
    
    i {
      font-size: 0.9em;
    }
  }
  
  .estudiante-individual {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #323232;
    font-weight: 500;
    font-size: 1.1rem;
    
    i {
      color: #4a6cf7;
      font-size: 1em;
    }
  }
  
  .integrantes-list {
    .integrantes-header {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #666666;
      font-size: 0.9rem;
      margin-bottom: 0.5rem;
      
      i {
        color: #4a6cf7;
      }
    }
    
    .integrantes-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    
    .integrante-tag {
      background: #f5f5f5;
      color: #333333;
      padding: 0.25rem 0.75rem;
      border-radius: 12px;
      font-size: 0.85rem;
      border: 1px solid #e0e0e0;
    }
  }
  
  .loading-integrantes {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #666666;
    font-size: 0.9rem;
    
    i {
      color: #4a6cf7;
    }
  }
}

.entrega-status {
  .status-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
    background: #fff3e0;
    color: #f57c00;
    border: 1px solid #ffcc02;
    
    &.calificada {
      background: #e8f5e9;
      color: #2e7d32;
      border-color: #4caf50;
    }
    
    i {
      font-size: 0.85em;
    }
  }
}

.archivo-entregado {
  background: #f8f9fa;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  
  .archivo-info {
    .archivo-item {
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      
      > i {
        color: #e53e3e;
        font-size: 1.2em;
        margin-top: 0.1rem;
      }
      
      .archivo-details {
        flex: 1;
        
        .archivo-label {
          display: block;
          font-weight: 500;
          color: #2d3748;
          margin-bottom: 0.5rem;
        }
        
        .archivo-actions {
          display: flex;
          align-items: center;
          gap: 1rem;
          flex-wrap: wrap;
          
          .archivo-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #4a6cf7;
            text-decoration: none;
            font-weight: 500;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            transition: all 0.2s ease;
            border: 1px solid #4a6cf7;
            background: #ffffff;
            
            &:hover {
              background: #4a6cf7;
              color: #ffffff;
              transform: translateY(-1px);
            }
            
            i {
              font-size: 0.8em;
            }
          }
          
          .no-archivo {
            color: #718096;
            font-style: italic;
          }
          
          .fecha-entrega {
            color: #718096;
            font-size: 0.85rem;
            background: #ffffff;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
          }
        }
      }
    }
  }
}

.calificacion-section {
  border-top: 1px solid #e2e8f0;
  padding-top: 1.5rem;
}

.calificacion-display {
  .calificacion-info-grid {
    display: grid;
    gap: 1rem;
    margin-bottom: 1.5rem;
    
    .calificacion-item {
      label {
        display: block;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
      }
      
      .calificacion-value {
        .calificacion-numero {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          background: #e8f5e9;
          color: #2e7d32;
          padding: 0.5rem 1rem;
          border-radius: 8px;
          font-weight: 600;
          font-size: 1.1rem;
          border: 2px solid #4caf50;
          min-width: 60px;
        }
        
        .sin-calificacion {
          color: #718096;
          font-style: italic;
          background: #f7fafc;
          padding: 0.5rem 1rem;
          border-radius: 8px;
          border: 1px dashed #cbd5e0;
        }
      }
      
      .observaciones-content {
        background: #f8f9fa;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        color: #2d3748;
        line-height: 1.6;
        font-size: 0.95rem;
      }
      
      .retroalimentacion-content {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
        
        .retroalimentacion-link {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          color: #4a6cf7;
          text-decoration: none;
          font-weight: 500;
          padding: 0.5rem 1rem;
          border-radius: 8px;
          border: 1px solid #4a6cf7;
          background: #ffffff;
          transition: all 0.2s ease;
          
          &:hover {
            background: #4a6cf7;
            color: #ffffff;
            transform: translateY(-1px);
          }
          
          i {
            color: #e53e3e;
            font-size: 1em;
          }
        }
        
        .fecha-retro {
          color: #718096;
          font-size: 0.85rem;
          background: #f7fafc;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          border: 1px solid #e2e8f0;
        }
      }
    }
  }
  
  .calificacion-actions {
    display: flex;
    justify-content: flex-end;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
  }
}

.calificacion-form {
  background: #f8f9fa;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #4a6cf7;
  border-radius: 0 12px 12px 0;
  padding: 1.5rem;
  margin-top: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  animation: slideDown 0.3s ease-out;
  
  .form-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
    
    h4 {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: #1a365d;
      margin: 0;
      font-size: 1.2rem;
      font-weight: 600;
      
      i {
        color: #4a6cf7;
        font-size: 1.1em;
      }
    }
  }
  
  .form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    align-items: start;
    
    .full-width {
      grid-column: 1 / -1;
    }
  }
  
  .form-group {
    label {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 600;
      color: #2d3748;
      margin-bottom: 0.75rem;
      font-size: 0.95rem;
      
      i {
        color: #4a6cf7;
        font-size: 0.9em;
      }
    }
    
    .input-wrapper {
      position: relative;
      display: inline-flex;
      align-items: center;
      
      .input-calif {
        width: 120px;
        padding: 0.75rem 1rem;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        text-align: center;
        background: #ffffff;
        transition: all 0.2s ease;
        
        &:focus {
          outline: none;
          border-color: #4a6cf7;
          box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
          transform: translateY(-1px);
        }
      }
      
      .input-suffix {
        margin-left: 0.75rem;
        color: #718096;
        font-weight: 500;
      }
    }
    
    .input-obs {
      width: 100%;
      padding: 1rem;
      border: 2px solid #e2e8f0;
      border-radius: 8px;
      font-size: 0.95rem;
      line-height: 1.6;
      background: #ffffff;
      transition: all 0.2s ease;
      resize: vertical;
      min-height: 120px;
      
      &:focus {
        outline: none;
        border-color: #4a6cf7;
        box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
      }
      
      &::placeholder {
        color: #a0aec0;
      }
    }
  }
}

.file-upload-area {
  .file-upload-label {
    display: block;
    cursor: pointer;
    
    .upload-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      border: 2px dashed #cbd5e0;
      border-radius: 8px;
      background: #ffffff;
      transition: all 0.2s ease;
      
      &:hover {
        border-color: #4a6cf7;
        background: #f7fafc;
      }
      
      i {
        font-size: 2rem;
        color: #4a6cf7;
        margin-bottom: 0.75rem;
      }
      
      .upload-text {
        color: #2d3748;
        font-weight: 500;
        margin-bottom: 0.25rem;
      }
      
      .upload-hint {
        color: #718096;
        font-size: 0.85rem;
      }
    }
  }
  
  .file-selected,
  .file-current {
    margin-top: 1rem;
    
    .file-info,
    .current-file-info {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 1rem;
      background: #e8f5e9;
      border: 1px solid #4caf50;
      border-radius: 8px;
      
      > i {
        color: #e53e3e;
        font-size: 1.2em;
      }
      
      .file-details,
      .current-file-details {
        flex: 1;
        
        .file-name,
        .current-file-label {
          display: block;
          font-weight: 500;
          color: #2d3748;
        }
        
        .file-size {
          color: #718096;
          font-size: 0.85rem;
        }
        
        .current-file-link {
          color: #4a6cf7;
          text-decoration: none;
          font-weight: 500;
          
          &:hover {
            text-decoration: underline;
          }
        }
      }
      
      .btn-remove-file,
      .btn-remove-current {
        background: #fed7d7;
        color: #c53030;
        border: 1px solid #fc8181;
        padding: 0.5rem;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease;
        
        &:hover {
          background: #c53030;
          color: #ffffff;
        }
        
        i {
          font-size: 0.9em;
        }
      }
    }
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-weight: 500;
  
  &.error-message {
    background: #fed7d7;
    color: #c53030;
    border: 1px solid #fc8181;
    border-left: 4px solid #e53e3e;
  }
  
  &.success-message {
    background: #e8f5e9;
    color: #2e7d32;
    border: 1px solid #4caf50;
    border-left: 4px solid #4caf50;
  }
  
  i {
    font-size: 1.1em;
  }
}

// Botones
%btn-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  text-decoration: none;
  
  i {
    font-size: 0.9em;
  }
  
  &:disabled {
    cursor: not-allowed;
    opacity: 0.6;
    transform: none !important;
    box-shadow: none !important;
  }
}

.btn-guardar {
  @extend %btn-base;
  background: #4a6cf7;
  color: #ffffff;
  border-color: #4a6cf7;
  box-shadow: 0 2px 4px rgba(74, 108, 247, 0.2);
  
  &:hover:not(:disabled) {
    background: #3a5bd9;
    border-color: #3a5bd9;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(74, 108, 247, 0.3);
  }
  
  &:active:not(:disabled) {
    transform: translateY(0);
  }
}

.btn-cancelar {
  @extend %btn-base;
  background: #f7fafc;
  color: #4a5568;
  border-color: #e2e8f0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  
  &:hover:not(:disabled) {
    background: #edf2f7;
    border-color: #cbd5e0;
    transform: translateY(-2px);
  }
}

.btn-editar {
  @extend %btn-base;
  background: #4a6cf7;
  color: #ffffff;
  border-color: #4a6cf7;
  padding: 0.6rem 1.25rem;
  box-shadow: 0 2px 4px rgba(74, 108, 247, 0.2);
  
  &:hover:not(:disabled) {
    background: #3a5bd9;
    border-color: #3a5bd9;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(74, 108, 247, 0.3);
  }
}

// Animaciones
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// Responsive
@media (max-width: 1200px) {
  .entregas-grid {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  }
}

@media (max-width: 768px) {
  .calificar-tarea {
    padding: 1rem;
  }
  
  .entregas-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .entrega-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .entregas-stats {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .archivo-actions {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .retroalimentacion-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .page-header h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .entregas-grid {
    grid-template-columns: 1fr;
  }
  
  .entrega-card {
    padding: 1rem;
  }
  
  .form-actions {
    .btn-guardar,
    .btn-cancelar {
      width: 100%;
    }
  }
}
</style>