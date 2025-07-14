<template>
  <div class="registrar-periodo">
    <div class="main-content">
      <div class="form-card">
        <h2>Registro de Período Académico</h2>
        
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
            <label for="nombre">Nombre del Período</label>
            <input 
              id="nombre"
              v-model="form.nombre" 
              type="text" 
              placeholder="Se generará automáticamente"
              readonly
              :disabled="loading"
              class="readonly-field"
            >
          </div>

          <button type="submit" class="register-btn" :disabled="loading || !form.nombre">
            <span v-if="loading">Registrando...</span>
            <span v-else>Registrar Período</span>
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
.registrar-periodo {
  width: 100vw;
  height: 100vh;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0;
  padding: 0;
  position: fixed;
  top: 0;
  left: 0;
  overflow: auto;
}

.main-content {
  width: 90%;
  max-width: 600px;
  margin: auto;
}

.form-card {
  background: white;
  padding: 4rem;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  width: 100%;
  box-sizing: border-box;
}

.form-card h2 {
  text-align: center;
  margin-bottom: 3rem;
  color: #2c3e50;
  font-size: 2.2rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 2rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 1.1rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 1.2rem;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.readonly-field {
  background-color: #f8f9fa !important;
  color: #6c757d;
  cursor: not-allowed;
}

.readonly-field:focus {
  border-color: #e9ecef !important;
  box-shadow: none !important;
}

.register-btn {
  width: 100%;
  padding: 1.3rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.register-btn:hover:not(:disabled) {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(52, 152, 219, 0.3);
}

.register-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.mensaje {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 10px;
  text-align: center;
  font-weight: 500;
  font-size: 1.1rem;
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

/* Responsive para pantallas pequeñas */
@media (max-width: 768px) {
  .main-content {
    width: 95%;
  }
  
  .form-card {
    padding: 2rem;
  }
  
  .form-card h2 {
    font-size: 1.8rem;
    margin-bottom: 2rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
}

/* Responsive para pantallas muy pequeñas */
@media (max-width: 480px) {
  .form-card {
    padding: 1.5rem;
  }
  
  .form-card h2 {
    font-size: 1.5rem;
  }
  
  .form-group input,
  .form-group select {
    padding: 1rem;
    font-size: 1rem;
  }
  
  .register-btn {
    padding: 1.1rem;
    font-size: 1.1rem;
  }
}
</style>