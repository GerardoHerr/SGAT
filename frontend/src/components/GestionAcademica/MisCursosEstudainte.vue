<template>
  <div class="mis-cursos-container">
    <h2 class="titulo">Mis Cursos</h2>
    <div class="tabla-wrapper">
      <table class="table table-hover table-bordered">
        <thead class="thead-dark">
          <tr>
            <th>#</th>
            <th>Asignatura</th>
            <th>Docente</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(curso, idx) in cursos" :key="curso.id">
            <td class="text-center">{{ idx + 1 }}</td>
            <td class="asignatura">
              <span class="asignatura-nombre">{{ curso.asignatura_nombre || curso.asignatura?.nombre }}</span>
              <div v-if="curso.asignatura?.codigo" class="asignatura-codigo">Código: {{ curso.asignatura.codigo }}</div>
            </td>
            <td class="docente">
              <span class="docente-nombre">{{ curso.docente_nombre || curso.docente?.nombre }} {{ curso.docente_apellido || curso.docente?.apellido }}</span>
              <div v-if="curso.docente?.email" class="docente-email">{{ curso.docente.email }}</div>
            </td>
            <td class="acciones text-center">
              <button class="btn btn-primary btn-sm" @click="revisarCurso(curso)">
                <i class="fas fa-eye"></i> Revisar
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="cursos.length === 0" class="alert alert-info mt-3 text-center">
        No tienes cursos asignados aún.
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'MisCursosEstudainte',
  data() {
    return {
      cursos: [],
      todosCursos: [],
      currentUser: null
    };
  },
  methods: {
    async cargarCursos() {
      try {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
        if (this.currentUser && this.currentUser.email) {
          const response = await axios.get(`http://localhost:8000/api/cursos/por-estudiante/?email=${encodeURIComponent(this.currentUser.email)}`);
          this.cursos = response.data;
        } else {
          this.cursos = [];
        }
      } catch (error) {
        this.cursos = [];
      }
    },
    revisarCurso(curso) {
      // Redirige a la vista mostrarTareasEstudiante con el id del curso seleccionado
      this.$router.push({ name: 'ListarTareasEstudiante', params: { id: curso.id } });
    }
  },
  mounted() {
    this.cargarCursos();
  }
};
</script>

<style scoped lang="scss">

@import '@/assets/styles/variables';
@import '@/assets/styles/base';

// Fallback para variables SCSS si no están definidas
$primary: #28a745 !default; // verde
$secondary: #6c757d !default;

.mis-cursos-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.titulo {
  text-align: center;
  font-weight: 700;
  margin-bottom: 2rem;
  color: $primary;
  letter-spacing: 1px;
}

.tabla-wrapper {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  padding: 1.5rem;
}

.table {
  margin-top: 0;
  background: #f9f9f9;
  th, td {
    vertical-align: middle;
    font-size: 1rem;
  }
  th {
    background: $primary;
    color: #fff;
    font-weight: 600;
    text-align: center;
  }
  td.asignatura {
    font-weight: 500;
    .asignatura-nombre {
      font-size: 1.1rem;
      color: $secondary;
    }
    .asignatura-codigo {
      font-size: 0.9rem;
      color: #888;
    }
  }
  td.docente {
    .docente-nombre {
      font-size: 1.05rem;
      font-weight: 500;
    }
    .docente-email {
      font-size: 0.9rem;
      color: #888;
    }
  }
  td.acciones {
    .btn {
      min-width: 90px;
    }
    i {
      margin-right: 4px;
    }
  }
}

.alert-info {
  font-size: 1.1rem;
  margin-top: 2rem;
}
</style>
