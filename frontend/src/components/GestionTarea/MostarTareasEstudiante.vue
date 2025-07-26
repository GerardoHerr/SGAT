<template>
  <div class="mostrar-tareas-estudiante">
    <h2>Tareas del Curso</h2>
    <div v-if="loading">Cargando tareas...</div>
    <div v-else>
      <div v-if="tareas.length === 0" class="no-tareas">No hay tareas registradas para este curso.</div>
      <ul v-else>
        <li v-for="tarea in tareas" :key="tarea.id">
          <strong>{{ tarea.titulo || tarea.tarea_titulo || (tarea.tarea && tarea.tarea.titulo) || 'Sin título' }}</strong>
          <span v-if="tarea.calificacion !== undefined"> | Calificación: {{ tarea.calificacion }}</span>
          <button class="btn-revisar-tarea" @click="revisarTarea(tarea)">Revisar</button>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  name: 'MostarTareasEstudiante',
  data() {
    return {
      tareas: [],
      loading: true,
      cursoId: null,
      estudianteEmail: ''
    }
  },
  async mounted() {
    // Obtener cursoId de la query y email del estudiante logeado
    const cursoId = this.$route.query.curso;
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    this.estudianteEmail = currentUser?.email || '';
    this.cursoId = cursoId;
    await this.cargarTareas();
  },
  methods: {
    async cargarTareas() {
      this.loading = true
      try {
        // Obtener todas las tareas del curso y filtrar por estudiante
        const response = await axios.get(`http://localhost:8000/api/entregas/?curso_id=${this.cursoId}`)
        // Filtrar solo las tareas del estudiante logeado
        this.tareas = response.data.filter(t => t.estudiante_email === this.estudianteEmail);
        console.log('Tareas cargadas:', this.tareas)
      } catch (error) {
        this.tareas = []
      }
      this.loading = false
    },
    async revisarTarea(tarea) {
      // Redirigir a la vista de subir tarea con el id de la tarea usando params
      this.$router.push({
        name: 'SubirTareaEstudiante',
        params: { id: tarea.id }
      });
    }
  },
  filters: {
    fecha(val) {
      if (!val) return ''
      return new Date(val).toLocaleString()
    }
  }
}
</script>

<style scoped>
.mostrar-tareas-estudiante {
  max-width: 800px;
  margin: 40px auto;
  background: #f8f8f8;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 30px 24px;
}
.no-tareas {
  text-align: center;
  color: #b94a48;
  font-weight: 500;
  margin-bottom: 24px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 8px;
}
.btn-revisar-tarea {
  margin-left: 12px;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 4px 12px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-revisar-tarea:hover {
  background: #217dbb;
}
</style>
