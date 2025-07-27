
<template>
  <div class="subir-tarea">
    <div v-if="loading" class="cargando-info"><i class="fas fa-spinner fa-spin"></i> Cargando información de la tarea...</div>
    <div v-else-if="!tareaEntrega">
      <div class="no-tarea"><i class="fas fa-exclamation-circle"></i> No se encontró la información de la entrega.</div>
    </div>
    <div v-else>
      <div class="card-tarea">
        <h2 class="titulo-tarea"><i class="fas fa-tasks"></i> {{ asignacion?.titulo || 'Sin título' }}</h2>
        <div class="bloques-tarea">
          <div v-if="tareaEntrega?.archivo" class="bloque-info">
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
              <strong>PDF:</strong>
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
          <div>
            <label for="archivo"><i class="fas fa-paperclip"></i> Selecciona tu archivo:</label>
            <input type="file" id="archivo" ref="archivoInput" required />
          </div>
          <button type="submit" class="btn-agregar-entrega"><i class="fas fa-upload"></i> Subir archivo</button>
          <button type="button" @click="cancelarEntrega" class="btn-cancelar">Cancelar</button>
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
      // Puedes agregar más campos si tu backend lo requiere
      // formData.append('fecha_entregada', new Date().toISOString());
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

<style scoped>
.subir-tarea {
  max-width: 650px;
  margin: 40px auto;
  background: #f8f8f8;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.10);
  padding: 36px 30px;
}
.cargando-info {
  color: #1e874b;
  font-size: 1.1em;
  text-align: center;
  margin: 30px 0;
}
.no-tarea {
  color: #b94a48;
  font-weight: 500;
  text-align: center;
  margin: 30px 0;
  font-size: 1.1em;
}
.card-tarea {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 4px 16px rgba(30,135,75,0.10);
  padding: 28px 24px 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.titulo-tarea {
  color: #3498db;
  margin-bottom: 12px;
  font-size: 1.5em;
  display: flex;
  align-items: center;
  gap: 10px;
}
.bloques-tarea {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.bloque-info {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: #f6f6f6;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 1.01em;
}
.bloque-estado {
  background: #eafbe7;
  border-left: 4px solid #27ae60;
}
.entrega-atrasada {
  background: #ffeaea;
  border-radius: 6px;
  padding: 6px 10px;
  margin-bottom: 4px;
}
.entrega-tiempo {
  background: #eafbe7;
  border-radius: 6px;
  padding: 6px 10px;
  margin-bottom: 4px;
}
.info-grupal {
  background: #eaf6fb;
  border-left: 4px solid #3498db;
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 14px;
  color: #1e874b;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}
.acciones-entrega {
  display: flex;
  gap: 16px;
  margin-top: 10px;
}
.btn-agregar-entrega {
  background: #27ae60;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 18px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}
.btn-agregar-entrega:hover {
  background: #1e874b;
}
.btn-cancelar {
  background: #b94a48;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 18px;
  cursor: pointer;
  font-size: 16px;
  margin-left: 10px;
  transition: background 0.2s;
}
.btn-cancelar:hover {
  background: #a93226;
}
</style>
