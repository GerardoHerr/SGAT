<template>
  <div class="crear-curso">
    <h2>Crear Curso</h2>
    <form @submit.prevent="crearCurso">
      <div class="form-group">
        <label for="asignatura">Asignatura:</label>
        <select id="asignatura" v-model="curso.asignatura" required @change="asignarDocente">
          <option value="" disabled>Seleccione una asignatura</option>
          <option v-for="asig in asignaturas" :key="asig.id" :value="asig.id">
            {{ asig.nombre }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="periodo">Periodo:</label>
        <input type="text" id="periodo" v-model="curso.periodo" required />
      </div>
      <button type="submit" class="btn-crear">Crear Curso</button>
    </form>
    <div v-if="mensaje" class="mensaje">{{ mensaje }}</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CrearCurso',
  data() {
    return {
      curso: {
        asignatura: '',
        docente: '',
        periodo: ''
      },
      asignaturas: [],
      mensaje: ''
    }
  },
  async mounted() {
    await this.cargarAsignaturas();
  },
  methods: {
    async cargarAsignaturas() {
      try {
        const res = await axios.get('http://localhost:8000/api/asignaturas/');
        this.asignaturas = res.data;
      } catch (e) {
        this.asignaturas = [];
      }
    },
    asignarDocente() {
      // Busca la asignatura seleccionada y asigna el docente responsable
      const asig = this.asignaturas.find(a => a.id === this.curso.asignatura);
      this.curso.docente = asig ? asig.docente_responsable : '';
    },
    async crearCurso() {
      try {
        await axios.post('http://localhost:8000/api/cursos/', this.curso)
        this.mensaje = 'Curso creado exitosamente.'
        this.curso = { asignatura: '', docente: '', periodo: '' }
      } catch (error) {
        this.mensaje = 'Error al crear el curso.'
      }
    }
  }
}
</script>

<style scoped>
.crear-curso {
  max-width: 400px;
  margin: 40px auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 30px 24px;
}
.form-group {
  margin-bottom: 18px;
}
label {
  display: block;
  font-weight: 500;
  margin-bottom: 6px;
}
input, select {
  width: 100%;
  padding: 8px 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1em;
}
.btn-crear {
  background: #1e874b;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 10px 22px;
  cursor: pointer;
  font-size: 1em;
  transition: background 0.2s;
}
.btn-crear:hover {
  background: #155d3b;
}
.mensaje {
  margin-top: 18px;
  font-weight: 500;
  color: #1e874b;
}
</style>