<template>
  <div class="calificar-tarea">
    <h2>Entregas de la Tarea</h2>
    <div v-if="loading">Cargando entregas...</div>
    <div v-else>
      <div v-if="entregas.length === 0" class="no-entregas">No hay entregas registradas para esta tarea.</div>
      <div v-else class="entregas-lista">
        <div v-for="entrega in entregasFiltradas" :key="entrega.id" class="entrega-card">
          <div class="entrega-header">
            <template v-if="entrega.grupo">
              <span class="entrega-grupo"><i class="fas fa-users"></i> Grupo: <b>{{ entrega.grupo_nombre || ('ID ' + entrega.grupo) }}</b></span>
              <div class="entrega-integrantes">
                <span v-if="entrega.estudiantesGrupo && entrega.estudiantesGrupo.length">
                  <span>Integrantes: </span>
                  <span v-for="(est, idx) in entrega.estudiantesGrupo" :key="est.email">
                    {{ est.nombre }} {{ est.apellido }}<span v-if="idx < entrega.estudiantesGrupo.length - 1">, </span>
                  </span>
                </span>
                <span v-else>Cargando integrantes...</span>
              </div>
            </template>
            <template v-else>
              <span class="entrega-estudiante"><i class="fas fa-user"></i> <b>{{ entrega.estudiante_nombre || entrega.estudiante_email }}</b></span>
            </template>
          </div>
          <div class="entrega-info">
            <span><i class="fas fa-calendar-alt"></i> Fecha entrega: <b>{{ entrega.fecha_entregada | fecha }}</b></span>
            <span v-if="entrega.calificacion !== undefined"><i class="fas fa-star"></i> Calificación: <b>{{ entrega.calificacion }}</b></span>
            <span v-if="entrega.archivo" class="entrega-archivo">
              <a :href="entrega.archivo" target="_blank" class="btn-descargar"><i class="fas fa-file-pdf"></i> Ver archivo</a>
            </span>
          </div>
          <div v-if="entrega.observaciones" class="entrega-observaciones">
            <i class="fas fa-comment"></i> <b>Observaciones:</b> {{ entrega.observaciones }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CalificarTarea',
  props: {
    id: {
      type: [String, Number],
      required: false
    }
  },
  data() {
    return {
      entregas: [],
      loading: true,
      tareaIdLocal: null
    }
  },
  computed: {
    entregasFiltradas() {
      // Si hay entregas con grupo_id, mostrar solo una por grupo (la primera encontrada)
      const entregasPorGrupo = {};
      const entregasSinGrupo = [];
      for (const entrega of this.entregas) {
        if (entrega.grupo) {
          if (!entregasPorGrupo[entrega.grupo]) {
            entregasPorGrupo[entrega.grupo] = entrega;
          }
        } else {
          entregasSinGrupo.push(entrega);
        }
      }
      return [...Object.values(entregasPorGrupo), ...entregasSinGrupo];
    }
  },
  async mounted() {
    // Permitir recibir el id por props o por $route.params
    let tareaId = this.id
    if (!tareaId && this.$route && this.$route.params && this.$route.params.id) {
      tareaId = this.$route.params.id
    }
    this.tareaIdLocal = tareaId
    await this.cargarEntregas()
    // Si hay entregas con grupo, cargar estudiantes de cada grupo
    await this.cargarEstudiantesDeGrupos();
  },
  methods: {
    async cargarEntregas() {
      this.loading = true
      try {
        const response = await axios.get(`http://localhost:8000/api/entregas/?tarea_id=${this.tareaIdLocal}`)
        this.entregas = response.data
      } catch (error) {
        this.entregas = []
      }
      this.loading = false
    },
    async cargarEstudiantesDeGrupos() {
      // Buscar los grupos únicos de las entregas
      const gruposIds = [...new Set(this.entregas.filter(e => e.grupo).map(e => e.grupo))];
      for (const grupoId of gruposIds) {
        try {
          const resp = await axios.get(`http://localhost:8000/api/grupos/${grupoId}/`);
          const estudiantes = resp.data.estudiantes || [];
          const grupoNombre = resp.data.nombre || null;
          // Asignar la lista de estudiantes y nombre de grupo a cada entrega de ese grupo
          this.entregas.forEach(e => {
            if (e.grupo === grupoId) {
              e.estudiantesGrupo = estudiantes;
              e.grupo_nombre = grupoNombre;
            }
          });
        } catch (err) {
          // Si falla, dejar vacío
          this.entregas.forEach(e => {
            if (e.grupo === grupoId) {
              e.estudiantesGrupo = [];
              e.grupo_nombre = null;
            }
          });
        }
      }
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
.calificar-tarea {
  max-width: 800px;
  margin: 40px auto;
  background: #f8f8f8;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.10);
  padding: 32px 28px;
}
.no-entregas {
  text-align: center;
  color: #b94a48;
  font-weight: 500;
  margin-bottom: 24px;
}
.entregas-lista {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
}
.entrega-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.10);
  padding: 18px 22px 14px 22px;
  min-width: 320px;
  flex: 1 1 340px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-left: 5px solid #3498db;
}
.entrega-header {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: 4px;
}
.entrega-grupo, .entrega-estudiante {
  color: #217dbb;
  font-weight: 600;
  font-size: 1.08em;
  display: flex;
  align-items: center;
  gap: 6px;
}
.entrega-integrantes {
  color: #555;
  font-size: 0.97em;
  margin-left: 18px;
}
.entrega-info {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  color: #444;
  font-size: 0.99em;
}
.entrega-archivo .btn-descargar {
  color: #e74c3c;
  font-weight: 500;
  text-decoration: none;
  margin-left: 8px;
}
.entrega-archivo .btn-descargar:hover {
  text-decoration: underline;
}
.entrega-observaciones {
  background: #f6f6f6;
  border-left: 3px solid #f39c12;
  padding: 7px 12px;
  border-radius: 6px;
  color: #a67c00;
  font-size: 0.98em;
  margin-top: 6px;
}
.entrega-info i, .entrega-header i {
  margin-right: 4px;
}
</style>
