<template>
  <div class="visualizar-entregas">
    <div class="entregas-container">
      <h2 class="entregas-title"><i class="fas fa-clipboard-list"></i> Visualizar Entregas por Curso</h2>
      <div class="entregas-select-group">
        <label for="curso-select">Selecciona un curso:</label>
        <select id="curso-select" v-model="cursoSeleccionado" @change="cargarTareas" class="entregas-select">
          <option value="">-- Selecciona un curso --</option>
          <option v-for="curso in cursos" :key="curso.id" :value="curso.id">
            {{ curso.asignatura_nombre }} - {{ curso.periodo }}
          </option>
        </select>
        <label v-if="tareas.length > 0" for="tarea-select">Tarea:</label>
        <select v-if="tareas.length > 0" id="tarea-select" v-model="tareaSeleccionada" @change="cargarEntregas" class="entregas-select">
          <option value="">-- Selecciona una tarea --</option>
          <option v-for="tarea in tareas" :key="tarea.id" :value="tarea.id">
            {{ tarea.titulo }} ({{ tarea.tipo_tarea }})
          </option>
        </select>
      </div>
      <div v-if="loading" class="entregas-loading">
        <i class="fas fa-spinner fa-spin"></i> Cargando entregas...
      </div>
      <div v-else>
        <!-- Eliminado: Archivos entregados por estudiantes -->
        <div v-if="entregas.length === 0 && tareaSeleccionada" class="entregas-alert">
          No hay entregas registradas para esta tarea.
        </div>
        <div v-else-if="entregas.length > 0" class="entregas-list">
          <table class="entregas-table">
            <thead>
              <tr>
                <th>Estudiante</th>
                <th>Fecha Entregada</th>
                <th>Archivo</th>
                <th>Calificación</th>
                <th>Observaciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entrega in entregas" :key="entrega.id">
                <td>{{ entrega.estudiante_nombre }}</td>
                <td>{{ entrega.fecha_entregada ? entrega.fecha_entregada.replace('T', ' ').slice(0, 16) : '-' }}</td>
                <td>
                  <a v-if="entrega.archivo" :href="entrega.archivo" target="_blank" class="entregas-link">Ver archivo</a>
                  <span v-else>-</span>
                </td>
                <td>{{ entrega.calificacion || '-' }}</td>
                <td>{{ entrega.observaciones || '-' }}</td>
              </tr>
            </tbody>
          </table>

          <div v-if="entregaSeleccionada" class="entrega-info-card">
            <h4>Información de la Entrega</h4>
            <ul>
              <li><b>Estudiante:</b> {{ entregaSeleccionada.estudiante_nombre }} ({{ entregaSeleccionada.estudiante_email }})</li>
              <li><b>Tarea:</b> {{ entregaSeleccionada.tarea_titulo }}</li>
              <li><b>Fecha Entregada:</b> {{ entregaSeleccionada.fecha_entregada ? entregaSeleccionada.fecha_entregada.replace('T', ' ').slice(0, 16) : '-' }}</li>
              <li><b>Calificación:</b> {{ entregaSeleccionada.calificacion || '-' }}</li>
              <li><b>Observaciones:</b> {{ entregaSeleccionada.observaciones || '-' }}</li>
              <li v-if="entregaSeleccionada.archivo"><b>Archivo:</b> <a :href="entregaSeleccionada.archivo" target="_blank">Ver archivo</a></li>
            </ul>
            <button class="btn-calificar" @click="calificarEntrega(entregaSeleccionada)"><i class="fas fa-pen"></i> Calificar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  name: 'VisualizarEntregas',
  data() {
    return {
      cursos: [],
      cursoSeleccionado: '',
      tareas: [],
      tareaSeleccionada: '',
      entregas: [],
      loading: false,
      docenteEmail: '',
      entregaSeleccionada: null
    }
  },
  computed: {
    tareaActual() {
      return this.tareas.find(t => String(t.id) === String(this.tareaSeleccionada)) || null;
    }
  },
  async mounted() {
    this.obtenerUsuarioActual()
    await this.cargarCursos()
  },
  methods: {
    mostrarInfoEntrega(entrega) {
      this.entregaSeleccionada = entrega;
    },
    calificarEntrega(entrega) {
      // Aquí puedes abrir un modal o redirigir a una vista de calificación
      alert('Funcionalidad de calificación para la entrega de ' + entrega.estudiante_nombre);
    },
    obtenerUsuarioActual() {
      const currentUser = JSON.parse(localStorage.getItem('currentUser'))
      if (currentUser && currentUser.rol === 'DOC') {
        this.docenteEmail = currentUser.email
      } else {
        this.$router.push('/login')
      }
    },
    async cargarCursos() {
      try {
        const response = await axios.get(`http://localhost:8000/api/cursos/?docente_email=${this.docenteEmail}`)
        this.cursos = response.data
      } catch (error) {
        this.cursos = []
      }
    },
    async cargarTareas() {
      this.tareaSeleccionada = '';
      this.tareas = [];
      this.entregas = [];
      if (!this.cursoSeleccionado) return;
      try {
        // Obtener todas las tareas del docente y filtrar por curso_id
        const response = await axios.get(`http://localhost:8000/api/asignaciones/?docente_email=${this.docenteEmail}`);
        this.tareas = (response.data || []).filter(t => String(t.curso) === String(this.cursoSeleccionado) || String(t.curso_id) === String(this.cursoSeleccionado));
      } catch (error) {
        this.tareas = [];
      }
    },
    async cargarEntregas() {
      if (!this.cursoSeleccionado || !this.tareaSeleccionada) {
        this.entregas = [];
        return;
      }
      this.loading = true;
      try {
        const response = await axios.get(`http://localhost:8000/api/entregas/?tarea_id=${this.tareaSeleccionada}`)
        console.log('response.data:', response.data);
        this.entregas = response.data || [];
      } catch (error) {
        this.entregas = [];
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.visualizar-entregas {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 40px 0;
}
.entregas-container {
  max-width: 1100px;
  margin: 0 auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(52,152,219,0.08);
  padding: 36px 28px 28px 28px;
}
.entregas-title {
  text-align: center;
  color: $color-primary-dark;
  font-size: 2em;
  font-weight: 700;
  margin-bottom: 32px;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
}
.entregas-select-group {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}
.entregas-select-group label {
  font-weight: 500;
  color: $text-primary;
}
.entregas-select {
  padding: 10px 18px;
  border-radius: 8px;
  border: 1.5px solid $border-color;
  font-size: 1em;
  background: #f9f9f9;
  min-width: 260px;
}
.entregas-loading {
  text-align: center;
  color: #3498db;
  font-size: 1.2em;
  padding: 40px 0;
}
.entregas-alert {
  background: #f8d7da;
  color: #721c24;
  border-radius: 8px;
  padding: 18px;
  text-align: center;
  margin-bottom: 18px;
  font-weight: 500;
}
.entregas-list {
  margin-top: 18px;
}
.entregas-table {
  width: 100%;
  border-collapse: collapse;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(52,152,219,0.06);
}
.entregas-table th, .entregas-table td {
  padding: 12px 10px;
  border-bottom: 1px solid #e0e0e0;
  text-align: left;
}
.entregas-table th {
  background: #e3f2fd;
  color: #1976d2;
  font-weight: 600;
}
.estado {
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 0.98em;
  font-weight: 600;
  &.ENTREGADO { background: #e8f5e9; color: #388e3c; }
  &.PENDIENTE { background: #fffde7; color: #fbc02d; }
  &.ATRASADO { background: #ffebee; color: #c62828; }
}
.entregas-link {
  color: $color-primary;
  text-decoration: underline;
  font-weight: 500;
}
@media (max-width: 900px) {
  .entregas-container {
    padding: 12px 2px;
  }
  .entregas-title {
    font-size: 1.2em;
  }
  .entregas-select {
    min-width: 120px;
  }
  .entregas-table th, .entregas-table td {
    padding: 7px 4px;
    font-size: 0.95em;
  }
}
</style>
