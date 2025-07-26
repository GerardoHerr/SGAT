
<template>
  <div class="subir-tarea">
    <div v-if="loading">Cargando información de la tarea...</div>
    <div v-else-if="!tareaEntrega">
      <div class="no-tarea">No se encontró la información de la entrega.</div>
    </div>
    <div v-else>
      <h2>{{ asignacion?.titulo || 'Sin título' }}</h2>

      <div :class="colorEntrega">
        <strong>Fecha entregada:</strong>
        {{ tareaEntrega?.fecha_entregada ? formatFecha(tareaEntrega.fecha_entregada) : 'No disponible' }}
        <span v-if="tareaEntrega?.fecha_entregada && asignacion?.fecha_entrega">
          <span v-if="esEntregaAtrasada" style="color:#b94a48;font-weight:600"> (Atrasada)</span>
          <span v-else style="color:#27ae60;font-weight:600"> (A tiempo)</span>
        </span>
      </div>
      <div>
        <strong>Descripción:</strong>
        {{ asignacion?.descripcion || 'No disponible' }}
      </div>
      <div>
        <strong>Tipo de tarea:</strong>
        {{ asignacion?.tipo_tarea || 'No disponible' }}
      </div>
      <div>
        <strong>¿Es grupal?:</strong>
        {{ asignacion?.es_grupal === true ? 'Sí' : asignacion?.es_grupal === false ? 'No' : 'No disponible' }}
      </div>
      <div>
        <strong>Fecha de creación:</strong>
        {{ asignacion?.fecha_creacion ? formatFecha(asignacion.fecha_creacion) : 'No disponible' }}
      </div>
      <div>
        <strong>Fecha de entrega:</strong>
        {{ asignacion?.fecha_entrega ? formatFecha(asignacion.fecha_entrega) : 'No disponible' }}
      </div>
      <div>
        <strong>PDF:</strong>
        <span v-if="asignacion?.archivo_explicacion">
          <a :href="asignacion.archivo_explicacion" target="_blank">Ver PDF</a>
        </span>
        <span v-else>No disponible</span>
      </div>
      <div>
        <strong>Calificación:</strong> {{ tareaEntrega?.calificacion !== undefined && tareaEntrega?.calificacion !== null ? tareaEntrega.calificacion : 'No disponible' }}
      </div>
      <div v-if="asignacion?.es_grupal" class="info-grupal" style="margin-bottom:12px;color:#1e874b;font-weight:500">
        Esta tarea es grupal. Al subir tu archivo, la entrega será válida para todos los integrantes del grupo.
      </div>
      <button v-if="!tareaEntrega?.archivo && !mostrarForm" class="btn-agregar-entrega" @click="mostrarFormularioEntrega">
        Agregar entrega
      </button>
      <button v-if="tareaEntrega?.archivo && !mostrarForm" class="btn-agregar-entrega" @click="mostrarFormularioEntrega">
        Modificar entrega
      </button>
      <form v-if="mostrarForm" @submit.prevent="enviarEntrega" class="form-entrega">
        <div>
          <label for="archivo">Selecciona tu archivo:</label>
          <input type="file" id="archivo" ref="archivoInput" required />
        </div>
        <button type="submit" class="btn-agregar-entrega">Subir archivo</button>
        <button type="button" @click="cancelarEntrega" style="margin-left:10px">Cancelar</button>
      </form>
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
      if (!this.tareaEntrega?.fecha_entregada || !this.asignacion?.fecha_entrega) return false;
      return new Date(this.tareaEntrega.fecha_entregada) > new Date(this.asignacion.fecha_entrega);
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
  max-width: 600px;
  margin: 40px auto;
  background: #f8f8f8;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 30px 24px;
}
.btn-agregar-entrega {
  margin-top: 20px;
  background: #27ae60;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 8px 18px;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s;
}
.btn-agregar-entrega:hover {
  background: #1e874b;
}
.entrega-atrasada {
  background: #ffeaea;
  border-radius: 6px;
  padding: 6px 10px;
  margin-bottom: 8px;
}
.entrega-tiempo {
  background: #eafbe7;
  border-radius: 6px;
  padding: 6px 10px;
  margin-bottom: 8px;
}
</style>
