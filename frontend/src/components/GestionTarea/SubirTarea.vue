<template>
  <div class="subir-tarea">
    <button @click="$router.push('/estudiante/calendario-tareas')" class="back-button">
      <i class="fas fa-arrow-left"></i> Volver a Calendario
    </button>
    <div v-if="loading" class="cargando-info"><i class="fas fa-spinner fa-spin"></i> Cargando información de la tarea...</div>
    <div v-else-if="!tareaEntrega">
      <div class="no-tarea"><i class="fas fa-exclamation-circle"></i> No se encontró la información de la entrega.</div>
    </div>
    <div v-else>
      <div class="card-tarea">
        <h2 class="titulo-tarea"><i class="fas fa-tasks"></i> {{ asignacion?.titulo || 'Sin título' }}</h2>
        <div class="bloques-tarea">
          <div v-if="tareaEntrega?.archivo && tareaEntrega.archivo !== '' && tareaEntrega.archivo !== null" class="bloque-info">
            <i class="fas fa-file-pdf"></i>
            <div>
              <strong>Tu entrega (PDF):</strong>
              <span>
                <a :href="tareaEntrega.archivo" target="_blank">Ver PDF entregado</a>
              </span>
            </div>
          </div>
          <div class="bloque-info bloque-estado">
            <i class="fas fa-clipboard-check"></i>
            <div>
              <div v-if="tareaEntrega?.archivo" :class="colorEntrega">
                <strong>Fecha entregada:</strong>
                {{ tareaEntrega?.fecha_entregada ? formatFecha(tareaEntrega.fecha_entregada) : 'No disponible' }}
                <span v-if="tareaEntrega?.fecha_entregada && asignacion?.fecha_entrega">
                  <span v-if="esEntregaAtrasada" style="color:#b94a48;font-weight:600"> (Atrasada)</span>
                  <span v-else style="color:#27ae60;font-weight:600"> (A tiempo)</span>
                </span>
              </div>
              <div v-else-if="asignacion?.fecha_entrega">
                <strong>Estado:</strong>
                <span v-if="esEntregaAtrasada" style="color:#b94a48;font-weight:600"><i class="fas fa-clock"></i> Atrasada</span>
                <span v-else style="color:#27ae60;font-weight:600"><i class="fas fa-clock"></i> A tiempo</span>
              </div>
            </div>
          </div>
          <div class="bloque-info">
            <i class="fas fa-align-left"></i>
            <div>
              <strong>Descripción:</strong>
              <span>{{ asignacion?.descripcion || 'No disponible' }}</span>
            </div>
          </div>
          <div class="bloque-info">
            <i class="fas fa-list"></i>
            <div>
              <strong>Tipo de tarea:</strong>
              <span>{{ asignacion?.tipo_tarea || 'No disponible' }}</span>
            </div>
          </div>
          <div class="bloque-info">
            <i :class="asignacion?.es_grupal ? 'fas fa-users' : 'fas fa-user'" style="color:#1e874b"></i>
            <div>
              <strong>¿Es grupal?:</strong>
              <span>{{ asignacion?.es_grupal === true ? 'Sí' : asignacion?.es_grupal === false ? 'No' : 'No disponible' }}</span>
            </div>
          </div>
          <div class="bloque-info">
            <i class="fas fa-calendar-plus"></i>
            <div>
              <strong>Fecha de creación:</strong>
              <span>{{ asignacion?.fecha_creacion ? formatFecha(asignacion.fecha_creacion) : 'No disponible' }}</span>
            </div>
          </div>
          <div class="bloque-info">
            <i class="fas fa-calendar-day"></i>
            <div>
              <strong>Fecha de entrega:</strong>
              <span>{{ asignacion?.fecha_entrega ? formatFecha(asignacion.fecha_entrega) : 'No disponible' }}</span>
            </div>
          </div>
          <div class="bloque-info">
            <i class="fas fa-file-pdf"></i>
            <div>
              <strong>PDF con la actividad:</strong>
              <span v-if="asignacion?.archivo_explicacion">
                <a :href="asignacion.archivo_explicacion" target="_blank">Ver PDF</a>
              </span>
              <span v-else>No disponible</span>
            </div>
          </div>
          <div class="bloque-info">
            <i class="fas fa-star"></i>
            <div>
              <strong>Calificación:</strong>
              <span>{{ tareaEntrega?.calificacion !== undefined && tareaEntrega?.calificacion !== null ? tareaEntrega.calificacion : 'No disponible' }}</span>
              <div v-if="tareaEntrega?.observaciones" style="margin-top:8px; color:#1a365d; background:#f5f5f5; border-left:3px solid #4a6cf7; padding:8px 12px; border-radius:4px;">
                <strong>Observaciones del docente:</strong> {{ tareaEntrega.observaciones }}
              </div>
              <div v-if="tareaEntrega?.retroalimentacion_archivo" style="margin-top:8px;">
                <strong>PDF de retroalimentación:</strong>
                <a :href="tareaEntrega.retroalimentacion_archivo" target="_blank">Ver PDF de retroalimentación</a>
              </div>
            </div>
          </div>
        </div>
        <div v-if="asignacion?.es_grupal" class="info-grupal">
          <i class="fas fa-users"></i> Esta tarea es grupal. Al subir tu archivo, la entrega será válida para todos los integrantes del grupo.
        </div>
        <div class="acciones-entrega">
          <button v-if="!tareaEntrega?.archivo && !mostrarForm" class="btn-agregar-entrega" @click="mostrarFormularioEntrega">
            <i class="fas fa-upload"></i> Agregar entrega
          </button>
          <button v-if="tareaEntrega?.archivo && !mostrarForm" class="btn-agregar-entrega" @click="mostrarFormularioEntrega">
            <i class="fas fa-edit"></i> Modificar entrega
          </button>
        </div>
        <form v-if="mostrarForm" @submit.prevent="enviarEntrega" class="form-entrega">
          <div class="file-input-wrapper">
            <label for="archivo" class="file-label"><i class="fas fa-paperclip"></i> Selecciona tu archivo:</label>
            <input type="file" id="archivo" ref="archivoInput" required class="file-input" />
          </div>
          <div class="form-btns">
            <button type="submit" class="btn-agregar-entrega"><i class="fas fa-upload"></i> Subir archivo</button>
            <button type="button" @click="cancelarEntrega" class="btn-cancelar">Cancelar</button>
            <button v-if="tareaEntrega?.archivo" type="button" @click="borrarEntrega" class="btn-borrar"><i class="fas fa-trash"></i> Borrar entrega</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SubirTarea',
  data() {
    return {
      tareaEntrega: null,
      asignacion: null,
      loading: true,
      mostrarForm: false
    }
  },
  async mounted() {
    const id = this.$route.params.id;
    this.loading = true;
    try {
      // Obtener la entrega
      const response = await axios.get(`http://localhost:8000/api/entregas/${id}/`);
      this.tareaEntrega = response.data;
      // Si existe el id de la tarea/asignación, obtener sus datos completos
      if (this.tareaEntrega.tarea) {
        try {
          const tareaResp = await axios.get(`http://localhost:8000/api/asignaciones/${this.tareaEntrega.tarea}/`);
          this.asignacion = tareaResp.data;
        } catch (e) {
          this.asignacion = null;
        }
      }
      console.log('Tarea entrega cargada:', this.tareaEntrega);
      console.log('Asignación cargada:', this.asignacion);
    } catch (error) {
      this.tareaEntrega = null;
      this.asignacion = null;
    }
    this.loading = false;
  },
  computed: {
    esEntregaAtrasada() {
      if (!this.asignacion?.fecha_entrega) return false;
      // Si ya hay archivo y fecha_entregada, comparar con esa fecha
      if (this.tareaEntrega?.archivo && this.tareaEntrega?.fecha_entregada) {
        return new Date(this.tareaEntrega.fecha_entregada) > new Date(this.asignacion.fecha_entrega);
      }
      // Si no hay archivo, comparar la fecha actual con la fecha de entrega
      return new Date() > new Date(this.asignacion.fecha_entrega);
    },
    colorEntrega() {
      if (!this.tareaEntrega?.fecha_entregada || !this.asignacion?.fecha_entrega) return '';
      return this.esEntregaAtrasada ? 'entrega-atrasada' : 'entrega-tiempo';
    }
  },
  methods: {
    async borrarEntrega() {
      if (!confirm('¿Seguro que deseas borrar tu archivo PDF subido?')) return;
      try {
        const formData = new FormData();
        formData.append('archivo', '');
        await axios.patch(`http://localhost:8000/api/entregas/${this.tareaEntrega.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        alert('Archivo eliminado correctamente');
        this.mostrarForm = false;
        // Recargar datos de la entrega para mostrar el estado actualizado
        const response = await axios.get(`http://localhost:8000/api/entregas/${this.tareaEntrega.id}/`);
        this.tareaEntrega = response.data;
      } catch (e) {
        alert('Error al borrar el archivo');
      }
    },
    mostrarFormularioEntrega() {
      this.mostrarForm = true;
    },
    cancelarEntrega() {
      this.mostrarForm = false;
    },
    async enviarEntrega() {
      const input = this.$refs.archivoInput;
      if (!input || !input.files.length) {
        alert('Selecciona un archivo');
        return;
      }
      const archivo = input.files[0];
      const formData = new FormData();
      formData.append('archivo', archivo);
      formData.append('fecha_entregada', new Date().toISOString());
      try {
        await axios.patch(`http://localhost:8000/api/entregas/${this.tareaEntrega.id}/`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        alert('Entrega subida correctamente');
        this.mostrarForm = false;
        // Recargar datos de la entrega para mostrar la nueva fecha_entregada y archivo
        const response = await axios.get(`http://localhost:8000/api/entregas/${this.tareaEntrega.id}/`);
        this.tareaEntrega = response.data;
      } catch (e) {
        alert('Error al subir la entrega');
      }
    },
    formatFecha(val) {
      if (!val) return '';
      return new Date(val).toLocaleString();
    }
  }
}
</script>

<style scoped lang="scss">
.back-button {
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      background: #f5f5f5;
      color: #2e7d32;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      text-decoration: none;
      font-weight: 500;
      margin-bottom: 1.5rem;
      transition: all 0.2s ease;
      border: 1px solid #e0e0e0;
      
      &:hover {
        background: #e8f0fe;
        border-color: #4a6cf7;
      }
      
      i {
        font-size: 0.9em;
      }
  }

@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.subir-tarea {
  max-width: 900px;
  margin: 48px auto;
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 2px 16px rgba(67, 233, 123, 0.10);
  padding: 48px 40px;
  min-height: 60vh;
}
.cargando-info {
  color: #1e874b;
  font-size: 1.15em;
  text-align: center;
  margin: 36px 0;
}
.no-tarea {
  color: #b94a48;
  font-weight: 600;
  text-align: center;
  margin: 36px 0;
  font-size: 1.15em;
  background: #ffebee;
  border-radius: 10px;
  padding: 18px 0;
  border-left: 4px solid #f44336;
}
.card-tarea {
  background: #f8f9fa;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.08);
  padding: 48px 60px 32px 60px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  border: 1px solid #e0e0e0;
  max-width: 1100px;
  margin: 0 auto;
}
.titulo-tarea {
  color: #2e7d32;
  margin-bottom: 18px;
  font-size: 1.7em;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  position: relative;
  padding-bottom: 0.5rem;
}
.titulo-tarea:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: #4caf50;
}
.bloques-tarea {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.bloque-info {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  background: #fff;
  border-radius: 10px;
  padding: 14px 18px;
  font-size: 1.08em;
  border: 1px solid #e0e0e0;
}
.bloque-estado {
  background: #eafbe7;
  border-left: 4px solid #27ae60;
}
.entrega-atrasada {
  background: #ffeaea;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 4px;
}
.entrega-tiempo {
  background: #eafbe7;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 4px;
}
.info-grupal {
  background: #eaf6fb;
  border-left: 4px solid #3498db;
  border-radius: 10px;
  padding: 12px 18px;
  margin-bottom: 18px;
  color: #1e874b;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}
.acciones-entrega {
  display: flex;
  gap: 20px;
  margin-top: 16px;
}
.btn-agregar-entrega {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 28px;
  cursor: pointer;
  font-size: 1.08em;
  font-weight: 600;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.10);
  outline: none;
}
.btn-agregar-entrega:hover {
  background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%);
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.18);
  transform: translateY(-2px) scale(1.03);
}
.btn-cancelar {
  background: #b94a48;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 28px;
  cursor: pointer;
  font-size: 1.08em;
  margin-left: 10px;
  transition: background 0.2s;
  font-weight: 600;
}
.btn-cancelar:hover {
  background: #a93226;
}
@media (max-width: 1200px) {
  .card-tarea {
    padding: 24px 10px;
  }
}
@media (max-width: 900px) {
  .subir-tarea {
    padding: 18px 4px;
  }
  .card-tarea {
    padding: 12px 2px;
  }
}
// Estilo para el input de archivo y botón borrar
.file-input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}
.file-label {
  font-weight: 600;
  color: #1e874b;
  margin-right: 8px;
}
.file-input {
  border: 1px solid #27ae60;
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 1em;
  background: #f8f9fa;
  color: #222;
  outline: none;
  transition: border 0.2s;
}
.file-input:focus {
  border: 1.5px solid #1e874b;
}
.form-btns {
  display: flex;
  gap: 16px;
  margin-top: 10px;
}
.btn-borrar {
  background: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 22px;
  cursor: pointer;
  font-size: 1.08em;
  font-weight: 600;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.10);
  outline: none;
}
.btn-borrar:hover {
  background: #c0392b;
  box-shadow: 0 4px 16px rgba(231, 76, 60, 0.18);
  transform: translateY(-2px) scale(1.03);
}
</style>
