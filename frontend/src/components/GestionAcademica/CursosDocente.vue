<template>
  <div class="cursos-docente">
    <h2>Mis Cursos</h2>
    <div v-if="loading" class="loading">Cargando cursos...</div>
    <div v-else>
      <div v-if="cursos.length === 0" class="no-cursos">No tienes cursos asignados.</div>
      <ul v-else class="lista-cursos">
        <li v-for="curso in cursos" :key="curso.id" class="curso-item">
          <strong>{{ curso.asignatura_nombre }}</strong> - Periodo: {{ curso.periodo }}<br>
          Docente: {{ curso.docente_nombre }}<br>
          Estudiantes inscritos: {{ curso.cantidad_estudiantes }}
          <br>
          <button
            class="btn-agregar-tarea"
            :disabled="curso.cantidad_estudiantes === 0"
            @click="irAgregarTarea(curso.id)"
          >
            Agregar Tarea
          </button>
          <button
            class="btn-mostrar-tareas"
            :disabled="curso.cantidad_estudiantes === 0"
            @click="irMostrarTareas(curso.id)"
            style="margin-left: 10px;"
          >
            Mostrar Tareas
          </button>
        </li>

      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CursosDocente',
  data() {
    return {
      cursos: [],
      loading: true,
      docenteEmail: ''
    }
  },
  async mounted() {
    const currentUser = JSON.parse(localStorage.getItem('currentUser'))
    if (!currentUser || currentUser.rol !== 'DOC') {
      this.$router.push('/login')
      return
    }
    this.docenteEmail = currentUser.email
    await this.cargarCursos()
  },
  methods: {
    async cargarCursos() {
      try {
        const response = await axios.get(`http://localhost:8000/api/cursos/?docente_email=${this.docenteEmail}`)
        this.cursos = response.data
      } catch (error) {
        this.cursos = []
      } finally {
        this.loading = false
      }
    },
    irAgregarTarea(cursoId) {
      // Redirige a la vista de asignar tarea, pasando el id del curso
      this.$router.push({ path: '/docente/asignar-tareas', query: { curso: cursoId } })
    },
    irMostrarTareas(cursoId) {
      // Redirige a la vista de mostrar tareas, pasando el id del curso
      this.$router.push({ path: '/docente/mostrar-tareas', query: { curso: cursoId } })
    }
  }
}
</script>

<style scoped>
.cursos-docente {
  max-width: 700px;
  margin: 40px auto;
  background: #f8f8f8;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 30px 24px;
}
h2 {
  text-align: center;
  color: #323232;
  margin-bottom: 24px;
}
.loading {
  text-align: center;
  color: #888;
}
.no-cursos {
  text-align: center;
  color: #b94a48;
  font-weight: 500;
}
.lista-cursos {
  list-style: none;
  padding: 0;
}
.curso-item {
  background: #fff;
  border-radius: 8px;
  margin-bottom: 18px;
  padding: 18px 20px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
  font-size: 17px;
}
.curso-item {
  position: relative;
}
.btn-agregar-tarea {
  margin-top: 10px;
  padding: 8px 18px;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
}
.btn-agregar-tarea:disabled {
  background: #bfc9d1;
  color: #eee;
  cursor: not-allowed;
}
 .btn-mostrar-tareas {
   margin-top: 10px;
   padding: 8px 18px;
   background: #27ae60;
   color: #fff;
   border: none;
   border-radius: 6px;
   font-size: 15px;
   font-weight: 600;
   cursor: pointer;
   transition: background 0.2s, box-shadow 0.2s;
 }
 .btn-mostrar-tareas:disabled {
   background: #bfc9d1;
   color: #eee;
   cursor: not-allowed;
 }
</style>
