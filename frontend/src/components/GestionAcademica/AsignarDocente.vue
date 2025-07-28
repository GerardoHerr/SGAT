<template>
  <div class="container">
    <h2>Asignar Docente Responsable</h2>
    
    <div class="card">
      <div class="card-body">
        <!-- Selector de Asignatura -->
        <div class="form-group">
          <label>Seleccionar Asignatura:</label>
          <select v-model="asignaturaSeleccionada" @change="cargarDocenteActual" class="form-control">
            <option value="">Seleccione una asignatura</option>
            <option v-for="asignatura in asignaturas" :key="asignatura.id" :value="asignatura.id">
              {{ asignatura.codigo }} - {{ asignatura.nombre }}
            </option>
          </select>
        </div>

        <!-- Docente Actual -->
        <div v-if="docenteActual" class="docente-actual mb-4">
          <h3 class="h5">Docente Actual:</h3>
          <div class="alert alert-info p-3">
            <p class="mb-0">
              <i class="fas fa-chalkboard-teacher me-2"></i>
              {{ docenteActual.nombre }} {{ docenteActual.apellido }}
              <span v-if="docenteActual.email" class="d-block text-muted small mt-1">{{ docenteActual.email }}</span>
            </p>
          </div>
        </div>

        <!-- Selector de Nuevo Docente -->
        <div class="form-group" v-if="asignaturaSeleccionada">
          <label>Asignar Nuevo Docente:</label>
          <select v-model="docenteSeleccionado" class="form-control">
            <option value="">Seleccione un docente</option>
            <option v-for="docente in docentes" :key="docente.id" :value="docente.id">
              {{ docente.nombre }} {{ docente.apellido }} - {{ docente.email }}
            </option>
          </select>
        </div>

        <!-- Botón de Asignar -->
        <div class="form-actions mt-4">
          <button 
            v-if="asignaturaSeleccionada && docenteSeleccionado" 
            @click="asignarDocente"
            class="btn btn-primary"
            :disabled="loading"
          >
            <i class="fas fa-user-plus me-2"></i>
            <span v-if="loading">Asignando...</span>
            <span v-else>Asignar Docente</span>
          </button>
        </div>

        <!-- Mensaje de resultado -->
        <div v-if="mensaje" :class="['message', `message-${tipoMensaje}`, 'mt-4']">
          <i :class="tipoMensaje === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
          {{ mensaje }}
        </div>
      </div>
    </div>

    <!-- Tabla -->
    <div class="tabla-section">
      <div class="card-tabla">
        <h3>Asignaturas y Docentes Responsables</h3>
        <div class="tabla-container">
          <table class="tabla-asignaturas">
            <thead>
              <tr>
                <th>Código</th>
                <th>Asignatura</th>
                <th>Docente Responsable</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="asignatura in asignaturas" :key="asignatura.id">
                <td>{{ asignatura.codigo }}</td>
                <td>{{ asignatura.nombre }}</td>
                <td>
                  <span v-if="asignatura.docente_responsable_nombre">
                    {{ asignatura.docente_responsable_nombre }} {{ asignatura.docente_responsable_apellido }}
                  </span>
                  <span v-else class="sin-docente">Sin asignar</span>
                </td>
                <td>
                  <span :class="asignatura.activa ? 'estado-activo' : 'estado-inactivo'">
                    {{ asignatura.activa ? 'Activa' : 'Inactiva' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
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
          this.cargarAsignaturas();
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

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';

.docente-actual {
  .alert {
    background-color: $bg-light;
    border: 1px solid $border-color;
    border-left: 4px solid $color-primary;
    color: $text-primary;
    margin-bottom: 0;
    
    i {
      color: $color-primary;
    }
  }
}

.alert-info {
  background-color: #e7f5ff;
  border-color: #74c0fc;
  color: #1864ab;
  
  i {
    color: #1864ab;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid $border-color;
}

.btn {
  i {
    margin-right: 0.5rem;
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

/* Ajustes responsivos */
@media (max-width: 768px) {
  .card {
    padding: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
    
    .btn {
      width: 100%;
    }
  }
}
</style>
