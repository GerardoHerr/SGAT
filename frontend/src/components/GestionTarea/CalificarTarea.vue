<template>
  <div class="calificar-tarea">
    <h2>Entregas de la Tarea</h2>
    <div v-if="loading">Cargando entregas...</div>
    <div v-else>
      <div v-if="entregas.length === 0" class="no-entregas">No hay entregas registradas para esta tarea.</div>
      <ul v-else>
        <li v-for="entrega in entregasFiltradas" :key="entrega.id">
          <template v-if="entrega.grupo">
            <strong>Grupo: {{ entrega.grupo_nombre || 'ID ' + entrega.grupo }}</strong><br>
            <span v-if="entrega.estudiantesGrupo && entrega.estudiantesGrupo.length">
              <span>Integrantes: </span>
              <span v-for="(est, idx) in entrega.estudiantesGrupo" :key="est.email">
                {{ est.nombre }} {{ est.apellido }}<span v-if="idx < entrega.estudiantesGrupo.length - 1">, </span>
              </span>
            </span>
            <span v-else>Cargando integrantes...</span>
            <br>
            Fecha entrega: {{ entrega.fecha_entrega | fecha }}
            <span v-if="entrega.calificacion !== undefined"> | Calificación: {{ entrega.calificacion }}</span>
          </template>
          <template v-else>
            <strong>{{ entrega.estudiante_nombre || entrega.estudiante_email }}</strong> - {{ entrega.fecha_entrega | fecha }}
            <span v-if="entrega.calificacion !== undefined"> | Calificación: {{ entrega.calificacion }}</span>
          </template>
        </li>
      </ul>
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
  max-width: 700px;
  margin: 40px auto;
  background: #f8f8f8;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  padding: 30px 24px;
}
.no-entregas {
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
  margin-bottom: 10px;
}
</style>
