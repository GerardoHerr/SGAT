<template>
  <div class="cursos-docente">
    <h2 class="titulo-cursos"><i class="fas fa-chalkboard-teacher"></i> Mis Cursos</h2>
    <div v-if="loading" class="cursos-loading">
      <i class="fas fa-spinner fa-spin"></i> Cargando tus cursos...
    </div>
    <div v-else>
      <div v-if="cursos.length === 0" class="alerta-cursos">
        <i class="fas fa-info-circle"></i>
        <div>
          <h4>No tienes cursos asignados</h4>
          <p>Ponte en contacto con el administrador para que te asigne cursos.</p>
        </div>
      </div>
      <div v-else class="cursos-grid">
        <div v-for="curso in cursos" :key="curso.id" class="curso-card">
          <div class="curso-header">
            <div class="curso-titulo">
              <i class="fas fa-book"></i> {{ curso.asignatura_nombre }}
            </div>
            <span class="curso-periodo">{{ curso.periodo }}</span>
          </div>
          <div class="curso-info">
            <span class="curso-docente"><i class="fas fa-user-tie"></i> {{ curso.docente_nombre || 'Sin docente asignado' }}</span>
            <span class="curso-estudiantes"><i class="fas fa-users"></i> {{ curso.cantidad_estudiantes }} estudiante{{ curso.cantidad_estudiantes !== 1 ? 's' : '' }}</span>
          </div>
          <div class="curso-actions">
            <button class="btn-curso btn-tarea" @click="irAgregarTarea(curso.id)" :disabled="curso.cantidad_estudiantes === 0">
              <i class="fas fa-plus-circle"></i> Nueva Tarea
            </button>
            <button class="btn-curso btn-ver" @click="irMostrarTareas(curso.id)" :disabled="curso.cantidad_estudiantes === 0">
              <i class="fas fa-tasks"></i> Ver Tareas
            </button>
          </div>
        </div>
      </div>
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
      docenteEmail: '',
      currentUser: null
    };
  },
  async mounted() {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    if (!this.currentUser || this.currentUser.rol !== 'DOC') {
      this.$router.push('/login');
      return;
    }
    
    this.docenteEmail = this.currentUser.email;
    await this.cargarCursos();
  },
  methods: {
    async cargarCursos() {
      try {
        // Usar query param docente_email en vez de ruta /docente/<email>/
        const response = await fetch(`http://localhost:8000/api/cursos/?docente_email=${encodeURIComponent(this.currentUser.email)}`, {
          headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
          throw new Error('Error al cargar los cursos');
        }
        this.cursos = await response.json();
      } catch (error) {
        console.error('Error al cargar los cursos:', error);
        this.cursos = [];
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },
    irAgregarTarea(cursoId) {
      this.$router.push(`/docente/asignar-tareas/${cursoId}`);
    },
    irMostrarTareas(cursoId) {
      this.$router.push(`/docente/mostrar-tareas/${cursoId}`);
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.cursos-docente {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 16px;
}
.titulo-cursos {
  color: #2e7d32;
  font-size: 2em;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2.5rem;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
}
.cursos-loading {
  text-align: center;
  color: #3498db;
  font-size: 1.2em;
  padding: 40px 0;
}
.alerta-cursos {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  background: #f8f8f8;
  border-radius: 12px;
  padding: 32px 24px;
  color: #b94a48;
  font-size: 1.1em;
  margin-bottom: 32px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
}
.alerta-cursos h4 {
  margin: 0 0 6px 0;
  color: #b94a48;
  font-weight: 700;
}
.cursos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
  gap: 32px;
}
.curso-card {
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.08);
  border: 1px solid #e0e0e0;
  padding: 28px 24px 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.curso-card:hover {
  box-shadow: 0 5px 20px rgba(76, 175, 80, 0.13);
  border-color: #a5d6a7;
}
.curso-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.curso-titulo {
  color: #3498db;
  font-size: 1.18em;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}
.curso-periodo {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 14px;
  border-radius: 12px;
  font-size: 0.98em;
  font-weight: 500;
}
.curso-info {
  display: flex;
  gap: 18px;
  color: #616161;
  font-size: 1em;
  margin-bottom: 8px;
}
.curso-docente {
  display: flex;
  align-items: center;
  gap: 6px;
}
.curso-estudiantes {
  display: flex;
  align-items: center;
  gap: 6px;
}
.curso-actions {
  display: flex;
  gap: 14px;
  margin-top: 10px;
}
.btn-curso {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 10px 22px;
  font-size: 1em;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.10);
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  outline: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.btn-curso:disabled {
  background: #b2dfdb;
  color: #eee;
  cursor: not-allowed;
  box-shadow: none;
}
.btn-curso:hover:not(:disabled),
.btn-curso:focus:not(:disabled) {
  background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%);
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.18);
  transform: translateY(-2px) scale(1.03);
}
@media (max-width: 900px) {
  .cursos-docente {
    padding: 18px 4px;
  }
  .cursos-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .curso-card {
    padding: 16px 4px;
    min-width: unset;
  }
}
</style>
