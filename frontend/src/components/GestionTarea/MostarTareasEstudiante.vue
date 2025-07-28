<template>
  <div class="mostrar-tareas-estudiante">
    <h2>Tareas del Curso</h2>
    <div v-if="loading" class="loading-tareas">Cargando tareas...</div>
    <div v-else>
      <div v-if="tareas.length === 0" class="no-tareas">No hay tareas registradas para este curso.</div>
      <div v-else class="tareas-grid">
        <div v-for="tarea in tareas" :key="tarea.id" class="tarea-card">
          <div class="tarea-header">
            <div class="tarea-titulo">
              <i class="fas fa-tasks"></i>
              {{ tarea.titulo || tarea.tarea_titulo || (tarea.tarea && tarea.tarea.titulo) || 'Sin título' }}
            </div>
            <div class="tarea-calificacion" v-if="tarea.calificacion !== undefined">
              <span :class="{'calif-aprobada': tarea.calificacion > 0, 'calif-pendiente': tarea.calificacion === null || tarea.calificacion === undefined}">
                Calificación: {{ tarea.calificacion !== null && tarea.calificacion !== undefined ? tarea.calificacion : 'Pendiente' }}
              </span>
            </div>
          </div>
          <div class="tarea-actions">
            <button class="btn-revisar-tarea" @click="revisarTarea(tarea)">
              <i class="fas fa-eye"></i> Revisar / Subir Entrega
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
    console.log('Curso ID:', cursoId);
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

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.mostrar-tareas-estudiante {
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 16px rgba(67, 233, 123, 0.10);
  padding: 36px 28px;
  min-height: 60vh;
}
h2 {
  color: #2e7d32;
  margin-bottom: 2rem;
  font-size: 1.7em;
  text-align: center;
  font-weight: 600;
  position: relative;
  padding-bottom: 1rem;
}
h2:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: #4caf50;
}
.loading-tareas {
  text-align: center;
  color: #666;
  padding: 20px;
}
.no-tareas {
  text-align: center;
  color: #c62828;
  font-weight: 500;
  margin-bottom: 24px;
  background: #ffebee;
  border-radius: 8px;
  padding: 18px 0;
  border-left: 4px solid #f44336;
}
.tareas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
  gap: 40px;
}
.tarea-card {
  background: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(67, 233, 123, 0.08);
  border: 1px solid #e0e0e0;
  padding: 22px 18px 18px 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 120px;
  transition: box-shadow 0.2s, border-color 0.2s;
}
.tarea-card:hover {
  box-shadow: 0 5px 20px rgba(76, 175, 80, 0.13);
  border-color: #a5d6a7;
}
.tarea-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 10px;
}
.tarea-titulo {
  color: #323232;
  font-size: 1.1em;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}
.tarea-calificacion {
  font-size: 1em;
  font-weight: 500;
}
.calif-aprobada {
  color: #2e7d32;
}
.calif-pendiente {
  color: #bdbdbd;
}
.tarea-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
.btn-revisar-tarea {
  background: linear-gradient(90deg, #43e97b 0%, #38f9d7 100%);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 8px 22px;
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
.btn-revisar-tarea:hover,
.btn-revisar-tarea:focus {
  background: linear-gradient(90deg, #38f9d7 0%, #43e97b 100%);
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.18);
  transform: translateY(-2px) scale(1.03);
}
@media (max-width: 1024px) {
  .tareas-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }
}
@media (max-width: 768px) {
  .mostrar-tareas-estudiante {
    padding: 12px 2px;
  }
  .tarea-card {
    padding: 12px 6px;
  }
}
</style>
