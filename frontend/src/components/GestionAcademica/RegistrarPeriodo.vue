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

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';
.registrar-periodo {
  width: 100%;
  padding: 2rem;
  margin: 0 auto;
  max-width: 1200px;
}

.main-content {
  background: $bg-white;
  border-radius: $border-radius;
  box-shadow: $shadow-sm;
  padding: 2rem;
  margin-bottom: 2rem;
}

.form-card {
  max-width: 800px;
  margin: 0 auto;
}

h2 {
  color: $text-primary;
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 3px;
    background: $color-primary;
  }
}

.form-group {
  margin-bottom: 1.5rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: $text-primary;
    font-weight: 500;
  }
  
  input, select {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid $border-color;
    border-radius: $border-radius;
    font-size: 1rem;
    transition: $transition-base;
    
    &:focus {
      outline: none;
      border-color: $color-primary;
      box-shadow: 0 0 0 2px rgba($color-primary, 0.2);
    }
    
    &[disabled] {
      background-color: $bg-lighter;
      cursor: not-allowed;
    }
  }
  
  /* Date picker styles */
  input[type="date"] {
    &::-webkit-calendar-picker-indicator {
      color: $color-primary;
      cursor: pointer;
      padding: 0.2rem;
      border-radius: 4px;
      
      &:hover {
        background: rgba($color-primary, 0.1);
      }
    }
  }
}

.readonly-field {
  background-color: $bg-lighter !important;
  color: $text-secondary !important;
  cursor: not-allowed;
  font-style: italic;
}

.register-btn {
  @extend .btn;
  @extend .btn-primary;
  width: 100%;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
}

.mensaje {
  padding: 1rem;
  border-radius: $border-radius;
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  
  &-success {
    background-color: $color-primary-bg;
    color: $color-primary-dark;
    border-left: 4px solid $color-primary;
  }
  
  &-error {
    background-color: #ffebee;
    color: #c62828;
    border-left: 4px solid #f44336;
  }
}

/* Responsive */
@media (max-width: $breakpoint-md) {
  .registrar-periodo {
    padding: 1rem;
  }
  
  .main-content {
    padding: 1.5rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  .form-card {
    padding: 0 1rem;
  }
}

@media (max-width: $breakpoint-sm) {
  .form-group {
    input, select {
      padding: 0.6rem 0.8rem;
    }
  }
  
  .register-btn {
    padding: 0.7rem 1rem;
    font-size: 0.9rem;
  }
}
</style>