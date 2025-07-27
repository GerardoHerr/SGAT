<template>
  <div class="asignar-docente">
    <!-- Formulario -->
    <div class="formulario-section">
      <div class="card-formulario">
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

<style scoped>
.asignar-docente {
  background: #f8fafc;
  min-height: 100vh;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin: 0;
  box-sizing: border-box;
}

/* FORMULARIO */
.formulario-section {
  display: flex;
  justify-content: center;
  width: 100%;
}

.card-formulario {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
  border: 2px solid #3b82f6;
}

.card-formulario h2 {
  color: #1e40af;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 700;
}

.form-group {
  margin-bottom: 1.8rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.8rem;
  color: #1e40af;
  font-weight: 600;
  font-size: 1.1rem;
}

.form-group select {
  width: 100%;
  padding: 1.2rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  background: white;
  color: #1e40af;
  font-size: 1.1rem;
  font-weight: 500;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%233b82f6' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 1rem center;
  background-repeat: no-repeat;
  background-size: 1.2em 1.2em;
  padding-right: 3rem;
  transition: all 0.3s ease;
}

.form-group select:focus {
  border-color: #3b82f6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.docente-actual {
  background: #eff6ff;
  padding: 1.8rem;
  border-radius: 8px;
  margin: 1.5rem 0;
  border-left: 4px solid #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.docente-actual h3 {
  margin: 0 0 0.8rem 0;
  color: #1e40af;
  font-size: 1.2rem;
  font-weight: 600;
}

.docente-actual p {
  margin: 0;
  color: #1e40af;
  font-weight: 600;
  font-size: 1.1rem;
}

.btn-asignar {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 1.2rem 2.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: block;
  margin: 2rem auto;
  font-size: 1.1rem;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
  min-width: 220px;
}

.btn-asignar:hover:not(:disabled) {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

.btn-asignar:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.mensaje {
  margin-top: 1.5rem;
  padding: 1.2rem;
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
  font-size: 1.1rem;
}

.mensaje.success {
  background: #dcfce7;
  color: #15803d;
  border: 2px solid #4ade80;
}

.mensaje.error {
  background: #fee2e2;
  color: #dc2626;
  border: 2px solid #f87171;
}

/* TABLA */
.tabla-section {
  flex: 1;
  width: 100%;
}

.card-tabla {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 2px solid #3b82f6;
  width: 100%;
}

.card-tabla h3 {
  color: #1e40af;
  text-align: center;
  margin-bottom: 1.8rem;
  font-size: 1.7rem;
  font-weight: 700;
}

.tabla-container {
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.tabla-asignaturas {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  font-size: 1rem;
}

.tabla-asignaturas th {
  background: #3b82f6;
  color: white;
  padding: 1.4rem 1.2rem;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
}

.tabla-asignaturas td {
  padding: 1.4rem 1.2rem;
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
  color: #1e40af;
  font-weight: 500;
  text-align: center;
  font-size: 1rem;
  vertical-align: middle;
}

.tabla-asignaturas tr:hover {
  background: #f8fafc;
  transition: background 0.2s ease;
}

.tabla-asignaturas tr:last-child td {
  border-bottom: none;
}

.sin-docente {
  color: #ef4444;
  font-style: italic;
  font-weight: 600;
}

.estado-activo {
  background: #dcfce7;
  color: #16a34a;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  border: 1px solid #4ade80;
}

.estado-inactivo {
  background: #fee2e2;
  color: #dc2626;
  padding: 0.6rem 1.2rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  border: 1px solid #f87171;
}

/* Borde superior azul */
.card-formulario::before,
.card-tabla::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: #3b82f6;
  border-radius: 12px 12px 0 0;
}

.card-formulario,
.card-tabla {
  position: relative;
}

/* RESPONSIVE */
@media (max-width: 1200px) {
  .asignar-docente {
    padding: 1.2rem;
  }
  
  .card-formulario {
    max-width: 100%;
    padding: 2rem;
  }
  
  .card-formulario h2 {
    font-size: 1.7rem;
  }
}

@media (max-width: 768px) {
  .asignar-docente {
    padding: 1rem;
  }
  
  .card-formulario,
  .card-tabla {
    padding: 1.5rem;
  }
  
  .card-formulario h2,
  .card-tabla h3 {
    font-size: 1.4rem;
  }
  
  .tabla-asignaturas th,
  .tabla-asignaturas td {
    padding: 1rem 0.8rem;
    font-size: 0.9rem;
  }
  
  .form-group select {
    font-size: 1rem;
    padding: 1rem;
  }
  
  .btn-asignar {
    font-size: 1rem;
    padding: 1rem 2rem;
  }
}

/* Animación suave */
.card-formulario,
.card-tabla {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
