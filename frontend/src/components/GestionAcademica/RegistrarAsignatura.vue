<!-- filepath: c:\Users\Usuario iTC\Desktop\Procesos_Project\SGAT\frontend\src\components\RegistrarAsignatura.vue -->
<template>
  <div class="registrar-asignatura">
    <div class="main-content">
      <div class="form-card">
        <h2>Registro de Asignatura</h2>
        
        <form @submit.prevent="registrarAsignatura">
          <div class="form-group">
            <input 
              v-model="form.codigo" 
              type="text" 
              placeholder="Código de Asignatura"
              required 
              maxlength="10"
              :disabled="loading"
            >
          </div>

          <div class="form-group">
            <input 
              v-model="form.nombre" 
              type="text" 
              placeholder="Nombre de Asignatura"
              required 
              maxlength="200"
              :disabled="loading"
            >
          </div>

          <div class="form-group">
            <textarea 
              v-model="form.descripcion"
              placeholder="Descripción de la asignatura"
              rows="3"
              :disabled="loading"
            ></textarea>
          </div>

          <div class="form-group">
            <select v-model="form.activa" :disabled="loading">
              <option value="" disabled>Seleccione estado</option>
              <option :value="true">Activa</option>
              <option :value="false">Inactiva</option>
            </select>
          </div>

          <button type="submit" class="register-btn" :disabled="loading">
            <span v-if="loading">Registrando...</span>
            <span v-else>Registrar</span>
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
import { authService } from '@/services/authService.js'

export default {
  name: 'RegistrarAsignatura',
  data() {
    return {
      form: {
        codigo: '',
        nombre: '',
        descripcion: '',
        activa: true
      },
      loading: false,
      mensaje: '',
      tipoMensaje: '',
      usuarioEmail: null
    }
  },
  mounted() {
    this.obtenerUsuarioActual();
  },
  methods: {
    obtenerUsuarioActual() {
      const currentUser = authService.getCurrentUser();
      if (currentUser && currentUser.email) {
        this.usuarioEmail = currentUser.email;
      } else {
        this.mensaje = 'Error: No se pudo obtener el usuario autenticado';
        this.tipoMensaje = 'error';
        this.$router.push('/login');
      }
    },

    async registrarAsignatura() {
      this.loading = true;
      this.mensaje = '';

      // Verificar que tenemos el email del usuario
      if (!this.usuarioEmail) {
        this.mensaje = 'Error: Usuario no autenticado';
        this.tipoMensaje = 'error';
        this.loading = false;
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/api/asignaturas/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            codigo: this.form.codigo,
            nombre: this.form.nombre,
            descripcion: this.form.descripcion,
            activa: this.form.activa,
            registrada_por: this.usuarioEmail
          })
        });

    const result = await response.json();
    console.log(result); // ✅ te ayudará a depurar

        if (response.ok) {
          this.mensaje = 'Asignatura registrada exitosamente';
          this.tipoMensaje = 'success';
          this.limpiarFormulario();
        } else {
          // Manejar errores de validación de Django REST Framework
          if (result.codigo && Array.isArray(result.codigo)) {
            this.mensaje = `Error en código: ${result.codigo[0]}`;
          } else if (result.nombre && Array.isArray(result.nombre)) {
            this.mensaje = `Error en nombre: ${result.nombre[0]}`;
          } else if (result.registrada_por && Array.isArray(result.registrada_por)) {
            this.mensaje = `Error en usuario: ${result.registrada_por[0]}`;
          } else if (result.detail) {
            this.mensaje = result.detail;
          } else {
            this.mensaje = 'Error al registrar la asignatura';
          }
          this.tipoMensaje = 'error';
        }
      } catch (error) {
        console.error('Error:', error);
        this.mensaje = 'Error de conexión con el servidor';
        this.tipoMensaje = 'error';
      }

  this.loading = false;
  },

    limpiarFormulario() {
      this.form = {
        codigo: '',
        nombre: '',
        descripcion: '',
        activa: true
      };
    }
  }
}
</script>

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';
.registrar-asignatura {
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
  
  input, select, textarea {
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
  
  textarea {
    min-height: 120px;
    resize: vertical;
  }
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
  .registrar-asignatura {
    padding: 1rem;
  }
  
  .main-content {
    padding: 1.5rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: $breakpoint-sm) {
  .form-card {
    padding: 0;
  }
  
  .form-group {
    input, select, textarea {
      padding: 0.6rem 0.8rem;
    }
  }
  
  .register-btn {
    padding: 0.7rem 1rem;
  }
}
</style>