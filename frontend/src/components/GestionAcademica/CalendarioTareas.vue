<template>
  <div class="calendario-tareas">
    <h2 class="titulo-calendario"><i class="fas fa-calendar-alt"></i> Calendario de Tareas</h2>
    <div v-if="loading" class="loading-msg">
      <i class="fas fa-spinner fa-spin"></i> Cargando tareas...
    </div>
    <div v-else>
      <div v-if="Object.keys(tareasPorFecha).length === 0" class="no-tareas">
        <i class="fas fa-info-circle"></i> No hay tareas registradas.
      </div>
      <div v-else>
        <div v-for="(tareas, fecha) in tareasPorFecha" :key="fecha" class="fecha-bloque">
          <div class="fecha-header">
            <i class="fas fa-calendar-day"></i>
            <span>{{ formatFecha(fecha) }}</span>
          </div>
          <ul>
            <li v-for="tarea in tareas" :key="tarea.id" class="tarea-item">
              <div class="tarea-info">
                <span class="tarea-titulo">
                  <i class="fas fa-tasks"></i>
                  {{ tarea.tarea_titulo || tarea.titulo || 'Sin título' }}
                </span>
                <span class="tarea-calificacion" v-if="tarea.calificacion !== undefined">
                  <i class="fas fa-star"></i>
                  {{ tarea.calificacion ?? 'Sin calificación' }}
                </span>
                <span v-if="tarea.archivo" class="tarea-pdf">
                  <i class="fas fa-file-pdf"></i>
                  <a :href="tarea.archivo" target="_blank">Ver PDF</a>
                </span>
              </div>
              <button class="btn-revisar-tarea" @click="irASubirTarea(tarea.id)">
                <i class="fas fa-eye"></i> Revisar
              </button>
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

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.calendario-tareas {
  max-width: 5400px; /* Aumenta el ancho máximo */
  margin: 40px auto;
  background: #fff;
  border-radius: 16px; /* Más redondeado */
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 40px 80px; /* Más espacio interno */
}

.titulo-calendario {
  color: #1e874b;
  margin-bottom: 24px;
  font-size: 2em;
  display: flex;
  align-items: center;
  gap: 10px;
}

.loading-msg {
  color: #1e874b;
  font-size: 1.2em;
  text-align: center;
  margin: 30px 0;
}

.no-tareas {
  color: #b94a48;
  font-weight: 500;
  text-align: center;
  margin: 30px 0;
  font-size: 1.1em;
}

.fecha-bloque {
  margin-bottom: 40px;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 32px;
  background: #f8f8f8;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(30,135,75,0.08);
}

.fecha-header {
  color: #1e874b;
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

ul {
  list-style: none;
  padding-left: 0;
}

.tarea-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border-radius: 14px;
  margin-bottom: 20px;
  padding: 24px 40px;
  box-shadow: 0 4px 16px rgba(30,135,75,0.06);
  transition: box-shadow 0.2s;
  font-size: 1.15em;
}

.tarea-item:hover {
  box-shadow: 0 4px 16px rgba(30,135,75,0.08);
}

.tarea-info {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
}

.tarea-titulo {
  color: #1e874b;
  font-weight: 600;
  font-size: 1.05em;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tarea-calificacion {
  color: #f39c12;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tarea-pdf {
  color: #b94a48;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tarea-pdf a {
  color: #b94a48;
  text-decoration: underline;
}

.btn-revisar-tarea {
  background-color: #1e874b;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 16px;
  cursor: pointer;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s;
}

.btn-revisar-tarea:hover {
  background-color: #155d3b;
}
</style>