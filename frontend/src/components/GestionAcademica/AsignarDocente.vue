<template>
  <div class="asignar-docente">
    <div class="main-content">
      <div class="card">
        <h2>Asignar Docente Responsable</h2>
        
        <!-- Selector de Asignatura -->
        <div class="form-group">
          <label>Seleccionar Asignatura:</label>
          <select v-model="asignaturaSeleccionada" @change="cargarDocenteActual">
            <option value="">Seleccione una asignatura</option>
            <option v-for="asignatura in asignaturas" :key="asignatura.id" :value="asignatura.id">
              {{ asignatura.codigo }} - {{ asignatura.nombre }}
            </option>
          </select>
        </div>

        <!-- Docente Actual -->
        <div v-if="docenteActual" class="docente-actual">
          <h3>Docente Actual:</h3>
          <p>{{ docenteActual.nombre }} {{ docenteActual.apellido }}</p>
        </div>

        <!-- Selector de Nuevo Docente -->
        <div class="form-group" v-if="asignaturaSeleccionada">
          <label>Asignar Nuevo Docente:</label>
          <select v-model="docenteSeleccionado">
            <option value="">Seleccione un docente</option>
            <option v-for="docente in docentes" :key="docente.id" :value="docente.id">
              {{ docente.nombre }} {{ docente.apellido }} - {{ docente.email }}
            </option>
          </select>
        </div>

        <!-- Botón de Asignar -->
        <button 
          v-if="asignaturaSeleccionada && docenteSeleccionado" 
          @click="asignarDocente"
          class="btn-asignar"
          :disabled="loading"
        >
          <span v-if="loading">Asignando...</span>
          <span v-else>Asignar Docente</span>
        </button>

        <!-- Mensaje de resultado -->
        <div v-if="mensaje" :class="['mensaje', tipoMensaje]">
          {{ mensaje }}
        </div>
      </div>

      <!-- Lista de Asignaturas con Docentes -->
      <div class="card">
        <h3>Asignaturas y Docentes Responsables</h3>
        <div class="tabla-asignaturas">
          <div class="tabla-header">
            <span>Código</span>
            <span>Asignatura</span>
            <span>Docente Responsable</span>
            <span>Estado</span>
          </div>
          <div v-for="asignatura in asignaturas" :key="asignatura.id" class="tabla-row">
            <span>{{ asignatura.codigo }}</span>
            <span>{{ asignatura.nombre }}</span>
            <span>
              <span v-if="asignatura.docente_responsable_nombre">
                {{ asignatura.docente_responsable_nombre }} {{ asignatura.docente_responsable_apellido }}
              </span>
              <span v-else class="sin-docente">Sin asignar</span>
            </span>
            <span :class="asignatura.activa ? 'activa' : 'inactiva'">
              {{ asignatura.activa ? 'Activa' : 'Inactiva' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AsignarDocente',
  data() {
    return {
      asignaturas: [],
      docentes: [],
      asignaturaSeleccionada: '',
      docenteSeleccionado: '',
      docenteActual: null,
      loading: false,
      mensaje: '',
      tipoMensaje: ''
    }
  },
  mounted() {
    this.cargarAsignaturas();
    this.cargarDocentes();
  },
  methods: {
    async cargarAsignaturas() {
      try {
        const response = await fetch('http://localhost:8000/api/asignaturas/');
        if (response.ok) {
          this.asignaturas = await response.json();
        }
      } catch (error) {
        console.error('Error al cargar asignaturas:', error);
      }
    },

    async cargarDocentes() {
      try {
        const response = await fetch('http://localhost:8000/api/asignaturas/docentes_disponibles/');
        if (response.ok) {
          this.docentes = await response.json();
        }
      } catch (error) {
        console.error('Error al cargar docentes:', error);
      }
    },

    cargarDocenteActual() {
      if (this.asignaturaSeleccionada) {
        const asignatura = this.asignaturas.find(a => a.id == this.asignaturaSeleccionada);
        if (asignatura && asignatura.docente_responsable_nombre) {
          this.docenteActual = {
            nombre: asignatura.docente_responsable_nombre,
            apellido: asignatura.docente_responsable_apellido
          };
        } else {
          this.docenteActual = null;
        }
      }
    },

    async asignarDocente() {
      this.loading = true;
      this.mensaje = '';

      try {
        const response = await fetch('http://localhost:8000/api/asignaturas/asignar_docente/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            asignatura_id: this.asignaturaSeleccionada,
            docente_id: this.docenteSeleccionado
          })
        });

        const result = await response.json();

        if (response.ok) {
          this.mensaje = result.mensaje;
          this.tipoMensaje = 'success';
          this.cargarAsignaturas(); // Recargar para mostrar los cambios
          this.asignaturaSeleccionada = '';
          this.docenteSeleccionado = '';
          this.docenteActual = null;
        } else {
          this.mensaje = result.error || 'Error al asignar docente';
          this.tipoMensaje = 'error';
        }
      } catch (error) {
        console.error('Error:', error);
        this.mensaje = 'Error de conexión con el servidor';
        this.tipoMensaje = 'error';
      }

      this.loading = false;
    }
  }
}
</script>

<style scoped>
.asignar-docente {
  padding: 2rem;
  background: #323232;
  min-height: 100vh;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  background: #DDD0C8;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card h2, .card h3 {
  color: #323232;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #323232;
  font-weight: 500;
}

.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #323232;
  border-radius: 0.5rem;
  background: white;
  color: #323232;
  font-size: 1rem;
}

.docente-actual {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 0.5rem;
  margin: 1rem 0;
  border-left: 4px solid #3498db;
}

.docente-actual h3 {
  margin: 0 0 0.5rem 0;
  color: #3498db;
  font-size: 1rem;
}

.docente-actual p {
  margin: 0;
  color: #323232;
  font-weight: 500;
}

.btn-asignar {
  background: #3498db;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: block;
  margin: 1.5rem auto;
}

.btn-asignar:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-2px);
}

.btn-asignar:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
}

.mensaje {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 0.5rem;
  text-align: center;
  font-weight: 500;
}

.mensaje.success {
  background-color: #d4edda;
  color: #155724;
  border: 2px solid #c3e6cb;
}

.mensaje.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 2px solid #f5c6cb;
}

.tabla-asignaturas {
  margin-top: 1rem;
}

.tabla-header, .tabla-row {
  display: grid;
  grid-template-columns: 1fr 2fr 2fr 1fr;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #323232;
}

.tabla-header {
  background: #323232;
  color: #DDD0C8;
  font-weight: 600;
  border-radius: 0.5rem 0.5rem 0 0;
}

.tabla-row {
  background: white;
  color: #323232;
}

.tabla-row:last-child {
  border-radius: 0 0 0.5rem 0.5rem;
}

.sin-docente {
  color: #e74c3c;
  font-style: italic;
}

.activa {
  color: #27ae60;
  font-weight: 500;
}

.inactiva {
  color: #e74c3c;
  font-weight: 500;
}

@media (max-width: 768px) {
  .tabla-header, .tabla-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .tabla-header span, .tabla-row span {
    padding: 0.25rem 0;
  }
}
</style>
