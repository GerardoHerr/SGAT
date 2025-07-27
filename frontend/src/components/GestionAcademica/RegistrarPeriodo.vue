<template>
  <div class="registrar-periodo">
    <div class="main-content">
      <div class="form-card">
        <h2>Registro de Periodo Academico</h2>
        
        <form @submit.prevent="registrarPeriodo">
          <div class="form-group">
            <label for="fechaInicio">Fecha de Inicio</label>
            <input 
              id="fechaInicio"
              v-model="form.fechaInicio" 
              type="date" 
              required 
              :disabled="loading"
              @change="generarNombre"
            >
          </div>

          <div class="form-group">
            <label for="fechaFin">Fecha de Fin</label>
            <input 
              id="fechaFin"
              v-model="form.fechaFin" 
              type="date" 
              required 
              :disabled="loading"
              :min="form.fechaInicio"
              @change="generarNombre"
            >
          </div>

          <div class="form-group">
            <label for="nombre">Nombre del Periodo</label>
            <input 
              id="nombre"
              v-model="form.nombre" 
              type="text" 
              placeholder="Se generara automaticamente"
              readonly
              :disabled="loading"
              class="readonly-field"
            >
          </div>

          <button type="submit" class="register-btn" :disabled="loading || !form.nombre">
            <span v-if="loading">Registrando...</span>
            <span v-else>Registrar Periodo</span>
          </button>
        </form>

        <!-- Mensaje de resultado -->
        <div v-if="mensaje" :class="['mensaje', tipoMensaje]">
          {{ mensaje }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegistrarPeriodo',
  data() {
    return {
      form: {
        fechaInicio: '',
        fechaFin: '',
        nombre: ''
      },
      loading: false,
      mensaje: '',
      tipoMensaje: ''
    }
  },
  methods: {
    generarNombre() {
      if (this.form.fechaInicio && this.form.fechaFin) {
        const fechaInicio = new Date(this.form.fechaInicio);
        const fechaFin = new Date(this.form.fechaFin);
        
        // Validar que la fecha de fin sea posterior a la de inicio
        if (fechaFin <= fechaInicio) {
          this.mensaje = 'La fecha de fin debe ser posterior a la fecha de inicio';
          this.tipoMensaje = 'error';
          this.form.nombre = '';
          return;
        } else {
          this.mensaje = '';
        }
        
        const meses = [
          'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ];
        
        const mesInicio = meses[fechaInicio.getMonth()];
        const añoInicio = fechaInicio.getFullYear();
        const mesFin = meses[fechaFin.getMonth()];
        const añoFin = fechaFin.getFullYear();
        
        // Generar nombre en formato: Marzo2025-Agosto2025
        this.form.nombre = `${mesInicio}${añoInicio}-${mesFin}${añoFin}`;
      } else {
        this.form.nombre = '';
      }
    },

    async registrarPeriodo() {
      this.loading = true;
      this.mensaje = '';

      try {
        const response = await fetch('http://localhost:8000/api/periodos/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            admin_id: 1,
            nombre: this.form.nombre,
            fecha_inicio: this.form.fechaInicio,
            fecha_fin: this.form.fechaFin
          })
        });

        const result = await response.json();

        if (result.success) {
          //this.mensaje = result.message;
          this.mensaje = result.message || 'Periodo registrado con éxito';
          this.tipoMensaje = 'success';
          this.limpiarFormulario();
        } else {
          this.mensaje = result.error;
          this.tipoMensaje = 'error';
        }
      } catch (error) {
        this.mensaje = 'Error de conexión con el servidor';
        this.tipoMensaje = 'error';
      }
      /*
      try {
        const response = await axios.post('http://localhost:8000/api/periodos/', this.periodo)
        this.mensaje = response.data.mensaje || 'Periodo registrado con éxito'
        this.periodo = { fechaInicio: '', fechaFin: '', nombre: '' }
        this.errors = {}
      } catch (error) {
        this.mensaje = 'Error al registrar el periodo'
        console.error(error.response?.data || error)
      }*/

      this.loading = false;
    },

    limpiarFormulario() {
      this.form = {
        fechaInicio: '',
        fechaFin: '',
        nombre: ''
      };
    }
  }
}
</script>

<style scoped>
/* IMPORTAR FUENTE TAHOMA */
@import url('https://fonts.googleapis.com/css2?family=Tahoma:wght@400;700;900&display=swap');

.registrar-periodo {
  width: 100%;
  min-height: 100vh;
  background: #f8fafc; /* FONDO GRIS CLARO EN LUGAR DEL AZUL FEO */
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 1rem 2rem 2rem 2rem;
  box-sizing: border-box;
  font-family: 'Tahoma', Arial, sans-serif;
}

.main-content {
  width: 100%;
  max-width: 1600px; /* MÁS ANCHO - ERA 1400px */
  background: transparent;
  margin-top: 1rem; /* REDUCIDO - ERA 2rem */
  font-family: 'Tahoma', Arial, sans-serif;
}

.form-card {
  background: white;
  padding: 1.5rem 12rem; /* MÁS PADDING HORIZONTAL - ERA 10rem Y ALTURA REDUCIDA - ERA 2rem */
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3);
  border: 2px solid #dbeafe;
  width: 100%;
  box-sizing: border-box;
  position: relative;
  transition: none;
  font-family: 'Tahoma', Arial, sans-serif;
}

.form-card:hover {
  transform: none;
  box-shadow: 0 12px 48px rgba(30, 58, 138, 0.4);
}

.form-card h2 {
  text-align: center;
  margin-bottom: 0.8rem; /* REDUCIDO - ERA 1rem */
  background: linear-gradient(135deg, #1e3a8a, #3b82f6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.8rem;
  font-weight: 900;
  font-family: 'Tahoma', Arial, sans-serif;
  text-transform: uppercase;
  letter-spacing: 2px;
  position: relative;
}

.form-card h2::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, #1e3a8a, #3b82f6);
  border-radius: 2px;
}

.form-group {
  margin-bottom: 0.8rem; /* REDUCIDO - ERA 1rem */
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 0.3rem; /* REDUCIDO - ERA 0.5rem */
  color: #1e3a8a;
  font-weight: 700;
  font-size: 1rem;
  font-family: 'Tahoma', Arial, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input {
  width: 100%;
  padding: 0.8rem 2rem; /* ALTURA REDUCIDA - ERA 1rem */
  border: 3px solid #dbeafe;
  border-radius: 16px;
  font-size: 1rem;
  color: #1e3a8a;
  background: white;
  transition: none;
  box-sizing: border-box;
  font-weight: 400;
  font-family: 'Tahoma', Arial, sans-serif;
  min-height: 44px; /* ALTURA REDUCIDA - ERA 48px */
}

.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  background: white;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  transform: none;
}

.form-group input:hover:not(:focus) {
  border-color: #93c5fd;
  transform: none;
  box-shadow: none;
}

.readonly-field {
  background: linear-gradient(135deg, #f0f9ff, #dbeafe) !important;
  color: #1e40af !important;
  cursor: not-allowed;
  border-color: #93c5fd !important;
  font-style: italic;
  font-family: 'Tahoma', Arial, sans-serif !important;
  font-size: 0.95rem !important;
}

.readonly-field:focus {
  border-color: #93c5fd !important;
  box-shadow: none !important;
  transform: none !important;
}

.register-btn {
  width: 100%;
  padding: 1rem; /* ALTURA REDUCIDA - ERA 1.2rem */
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: white;
  border: none;
  border-radius: 16px;
  font-size: 1.1rem;
  font-weight: 700;
  font-family: 'Tahoma', Arial, sans-serif;
  cursor: pointer;
  transition: none;
  margin-top: 1rem; /* REDUCIDO - ERA 1.5rem */
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
  position: relative;
  overflow: hidden;
}

.register-btn::before {
  display: none;
}

.register-btn:hover {
  background: linear-gradient(135deg, #1e40af, #2563eb);
  transform: none;
  box-shadow: 0 4px 15px rgba(59, 130, 246, 0.5);
}

.register-btn:active {
  transform: none;
}

.register-btn:disabled {
  background: linear-gradient(135deg, #9ca3af, #6b7280);
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* QUITAR TODAS LAS ANIMACIONES */
.form-card {
  animation: none;
}

.form-group {
  animation: none;
}

.register-btn {
  animation: none;
}

.mensaje {
  margin-top: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 16px;
  text-align: center;
  font-weight: 700;
  font-size: 0.9rem;
  font-family: 'Tahoma', Arial, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: none;
  backdrop-filter: blur(10px);
}

.mensaje.success {
  background: linear-gradient(135deg, rgba(219, 234, 254, 0.9), rgba(147, 197, 253, 0.9));
  color: #1e40af;
  border: 3px solid #3b82f6;
}

.mensaje.error {
  background: linear-gradient(135deg, rgba(254, 226, 226, 0.9), rgba(252, 165, 165, 0.9));
  color: #dc2626;
  border: 3px solid #f87171;
}

/* Efectos para date inputs */
.form-group input[type="date"]::-webkit-calendar-picker-indicator {
  color: #3b82f6;
  font-size: 1.2em;
  cursor: pointer;
  padding: 0.3rem;
  border-radius: 8px;
  transition: none;
}

.form-group input[type="date"]::-webkit-calendar-picker-indicator:hover {
  background: rgba(59, 130, 246, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .form-card {
    padding: 1.5rem 2rem;
  }
  
  .main-content {
    margin-top: 1rem;
    max-width: 95%;
  }
}
</style>