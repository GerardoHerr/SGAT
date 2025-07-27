<template>
  <div class="mostrar-tareas">
    <h2>Tareas del Curso</h2>
    <div v-if="cursoSeleccionado">
      <div v-if="tareas.length === 0" class="no-tareas">No hay tareas registradas para este curso.</div>
      <div v-else>
        <div v-for="tipo in tiposTarea" :key="tipo" class="tipo-tarea">
          <h3>{{ tipoLabels[tipo] }}</h3>
          <ul>
            <li v-for="tarea in tareasPorTipo(tipo)" :key="tarea.id" class="tarea-item">
              <div class="tarea-info">
                <strong class="tarea-titulo">{{ tarea.titulo }}</strong>
                <span class="tarea-fecha">Entregas: {{ tarea.cantidad_entregas }}</span>
                <span class="tarea-tipo">
                  <i :class="tarea.es_grupal ? 'fas fa-users' : 'fas fa-user'" style="margin-right:4px"></i>
                  {{ tarea.es_grupal ? 'Grupal' : 'Individual' }}
                </span>
              </div>
              <button class="btn-calificar" @click="irACalificarTarea(tarea.id)">Calificar</button>
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
  name: 'MostrarTareas',
  data() {
    return {
      cursoSeleccionado: '',
      tareas: [],
      docenteEmail: '',
      tiposTarea: ['AA', 'ACD', 'APE'],
      tipoLabels: {
        AA: 'AA - Actividades de Aplicación',
        ACD: 'ACD - Construcción del Conocimiento',
        APE: 'APE - Prácticas de Experimentación'
      },
    }
  },
  async mounted() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'))
    if (!currentUser || currentUser.rol !== 'DOC') {
      this.$router.push('/login')
      return
    }
    this.docenteEmail = currentUser.email
    // Obtener el curso desde la query
    const cursoId = this.$route.query.curso
    if (cursoId) {
      this.cursoSeleccionado = String(cursoId)
      await this.cargarTareas()
    }
  },
  methods: {
    async cargarTareas() {
      if (!this.cursoSeleccionado) return
      try {
        const response = await axios.get(`http://localhost:8000/api/asignaciones/?curso=${this.cursoSeleccionado}&docente_email=${this.docenteEmail}`)
        this.tareas = response.data
      } catch (error) {
        this.tareas = []
      }
    },
    tareasPorTipo(tipo) {
      return this.tareas.filter(t => t.tipo_tarea === tipo)
    },
    irACalificarTarea(tareaId) {
      this.$router.push({ name: 'CalificarTarea', params: { id: tareaId } })
    },
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
.btn-calificar {
  margin-left: 12px;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 4px 12px;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-calificar:hover {
  background: #217dbb;
}
.mostrar-tareas {
  max-width: 800px;
  margin: 40px auto;
  background: #f8f8f8;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 30px 24px;
}
.tipo-tarea {
  margin-bottom: 32px;
}
.tareas-grupo {
  display: flex;
  gap: 40px;
}
.tareas-col {
  flex: 1;
  background: #fff;
  border-radius: 8px;
  padding: 16px 20px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
}
h3 {
  color: #3498db;
  margin-bottom: 10px;
}
h4 {
  color: #323232;
  margin-bottom: 8px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 8px;
}
.no-tareas {
  text-align: center;
  color: #b94a48;
  font-weight: 500;
  margin-bottom: 24px;
}

/* Mejor presentación de la tarea */
.tarea-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border-radius: 8px;
  margin-bottom: 12px;
  padding: 12px 18px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
}

.tarea-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.tarea-titulo {
  color: #3498db;
  font-weight: 600;
  font-size: 1.08em;
}
.tarea-fecha {
  color: #555;
  font-size: 0.98em;
}
.tarea-tipo {
  color: #1e874b;
  font-size: 0.98em;
  font-weight: 500;
  display: flex;
  align-items: center;
}
</style>
