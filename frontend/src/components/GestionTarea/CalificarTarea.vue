<template>
  <div class="calificar-tarea">
    <h2>Entregas de la Tarea</h2>
    <div v-if="loading">Cargando entregas...</div>
    <div v-else>
      <div v-if="entregas.length === 0" class="no-entregas">No hay entregas registradas para esta tarea.</div>
      <ul v-else>
        <li v-for="entrega in entregasFiltradas" :key="entrega.id" class="entrega-item">
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
          </template>
          <template v-else>
            <strong>{{ entrega.estudiante_nombre || entrega.estudiante_email }}</strong> - {{ entrega.fecha_entrega | fecha }}
          </template>

          <div class="calificacion-form">
            <template v-if="entrega.calificacion === null || entrega.calificacion === undefined">
              <input 
                v-model.number="entrega.calificacionInput" 
                type="number" 
                step="0.01" 
                min="0" 
                max="2.5" 
                placeholder="Calificación" 
                class="input-calif" 
                @keyup.enter="calificarEntrega(entrega)"
              />
              <input 
                v-model="entrega.observacionesInput" 
                type="text" 
                placeholder="Observaciones" 
                class="input-obs" 
                @keyup.enter="calificarEntrega(entrega)"
              />
              <button 
                @click="calificarEntrega(entrega)" 
                :disabled="entrega.guardando"
                class="btn-guardar"
              >
                {{ entrega.guardando ? 'Guardando...' : 'Guardar' }}
              </button>
              <span v-if="entrega.error" class="error">{{ entrega.error }}</span>
              <span v-if="entrega.exito" class="exito">Calificación guardada</span>
            </template>
            <template v-else>
              <span class="calif-guardada">Calificación: {{ entrega.calificacion }}</span>
              <span v-if="entrega.observaciones"> | Observaciones: {{ entrega.observaciones }}</span>
              <button @click="habilitarEdicion(entrega)" class="btn-editar">Editar</button>
            </template>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

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
    };
  },
  computed: {
    entregasFiltradas() {
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
    let tareaId = this.id;
    if (!tareaId && this.$route?.params?.id) {
      tareaId = this.$route.params.id;
    }
    this.tareaIdLocal = tareaId;
    
    try {
      await this.cargarEntregas();
      await this.cargarEstudiantesDeGrupos();
    } catch (error) {
      console.error('Error al cargar datos:', error);
    }
    
    // Inicializar inputs para edición
    this.entregas.forEach(e => {
      e.calificacionInput = e.calificacion;
      e.observacionesInput = e.observaciones;
      e.guardando = false;
      e.error = '';
      e.exito = false;
    });
  },
  methods: {
    async cargarEntregas() {
      this.loading = true;
      try {
        const response = await api.get(`entregas/?tarea_id=${this.tareaIdLocal}`);
        this.entregas = response.data.map(entrega => ({
          ...entrega,
          calificacionInput: entrega.calificacion,
          observacionesInput: entrega.observaciones || '',
          guardando: false,
          error: '',
          exito: false,
          estudiantesGrupo: entrega.estudiantesGrupo || []
        }));
      } catch (error) {
        console.error('Error al cargar entregas:', error);
        this.entregas = [];
      } finally {
        this.loading = false;
      }
    },
    
    async cargarEstudiantesDeGrupos() {
      const gruposIds = [...new Set(this.entregas.filter(e => e.grupo).map(e => e.grupo))];
      
      await Promise.all(gruposIds.map(async (grupoId) => {
        try {
          const resp = await api.get(`grupos/${grupoId}/`);
          const estudiantes = resp.data.estudiantes || [];
          const grupoNombre = resp.data.nombre || null;
          
          this.entregas = this.entregas.map(e => {
            if (e.grupo === grupoId) {
              return {
                ...e,
                estudiantesGrupo: estudiantes,
                grupo_nombre: grupoNombre
              };
            }
            return e;
          });
        } catch (err) {
          console.error(`Error cargando grupo ${grupoId}:`, err);
          this.entregas = this.entregas.map(e => {
            if (e.grupo === grupoId) {
              return {
                ...e,
                estudiantesGrupo: [],
                grupo_nombre: null
              };
            }
            return e;
          });
        }
      }));
    },
    
    async calificarEntrega(entrega) {
      if (!entrega.calificacionInput && entrega.calificacionInput !== 0) {
        entrega.error = 'Ingrese una calificación.';
        return;
      }
      
      const maxCalif = 2.5;
      if (entrega.calificacionInput < 0 || entrega.calificacionInput > maxCalif) {
        entrega.error = `La calificación debe estar entre 0 y ${maxCalif}`;
        return;
      }
      
      entrega.error = '';
      entrega.exito = false;
      entrega.guardando = true;
      
      try {
        await api.post(`entregas/${entrega.id}/calificar/`, {
          calificacion: parseFloat(entrega.calificacionInput),
          observaciones: entrega.observacionesInput || ''
        });
        
        entrega.calificacion = parseFloat(entrega.calificacionInput);
        entrega.observaciones = entrega.observacionesInput || '';
        entrega.exito = true;
        
        // Reset success message after 3 seconds
        setTimeout(() => {
          entrega.exito = false;
        }, 3000);
        
      } catch (err) {
        console.error('Error al guardar calificación:', err);
        entrega.error = err.response?.data?.error || 'Error al guardar la calificación';
      } finally {
        entrega.guardando = false;
      }
    },
    
    habilitarEdicion(entrega) {
      entrega.calificacionInput = entrega.calificacion;
      entrega.observacionesInput = entrega.observaciones || '';
      entrega.calificacion = null;
      entrega.error = '';
      entrega.exito = false;
    }
  },
  filters: {
    fecha(val) {
      if (!val) return '';
      return new Date(val).toLocaleString();
    }
  }
};
</script>

<style scoped>
.calificar-tarea {
  max-width: 800px;
  margin: 40px auto;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h2 {
  color: #2c3e50;
  margin-bottom: 24px;
  font-size: 1.8em;
  text-align: center;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.loading {
  text-align: center;
  color: #666;
  font-style: italic;
}

.no-entregas {
  text-align: center;
  color: #b94a48;
  font-weight: 500;
  padding: 20px;
  background-color: #f8d7da;
  border-radius: 6px;
  margin: 20px 0;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.entrega-item {
  background: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
  position: relative;
}

.entrega-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.calificacion-form {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px dashed #e0e0e0;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.input-calif,
.input-obs {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.input-calif:focus,
.input-obs:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.input-calif {
  width: 100px;
  text-align: center;
}

.input-obs {
  flex: 1;
  min-width: 200px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-guardar {
  background-color: #2ecc71;
  color: white;
}

.btn-guardar:not(:disabled):hover {
  background-color: #27ae60;
}

.btn-editar {
  background-color: #3498db;
  color: white;
  margin-left: 10px;
}

.btn-editar:hover {
  background-color: #2980b9;
}

.error {
  color: #e74c3c;
  font-size: 13px;
  margin-left: 10px;
  flex-basis: 100%;
  margin-top: 5px;
}

.exito {
  color: #27ae60;
  font-size: 13px;
  margin-left: 10px;
  font-weight: 500;
}

.calif-guardada {
  font-weight: 600;
  color: #2c3e50;
  margin-right: 10px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .calificar-tarea {
    margin: 20px 15px;
    padding: 20px 15px;
  }
  
  .calificacion-form {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .input-calif,
  .input-obs,
  button {
    width: 100%;
    margin: 5px 0;
  }
  
  .btn-editar {
    margin-left: 0;
    margin-top: 10px;
  }
}
</style>
