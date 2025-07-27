<template>
  <div class="registro-container">
    <div class="form-card">
      <div class="header">
        <div class="icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="user-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
          </svg>
        </div>
        <h2 class="form-title">Registro de Usuario</h2>
        <p class="form-subtitle">Completa tus datos para crear una cuenta</p>
      </div>
      
      <form @submit.prevent="registrarUsuario" class="form-content">
        <div class="input-group">
          <div class="input-wrapper">
            <input 
              v-model="usuario.nombre" 
              placeholder="Nombre" 
              :class="{ 'error': errors.nombre }"
            />
            <span v-if="errors.nombre" class="error-msg">{{ errors.nombre }}</span>
          </div>
          
          <div class="input-wrapper">
            <input 
              v-model="usuario.apellido" 
              placeholder="Apellido" 
              :class="{ 'error': errors.apellido }"
            />
            <span v-if="errors.apellido" class="error-msg">{{ errors.apellido }}</span>
          </div>
        </div>

        <div class="input-wrapper">
          <input 
            v-model="usuario.email" 
            type="email" 
            placeholder="Correo electrónico" 
            :class="{ 'error': errors.email }"
          />
          <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
        </div>

        <div class="input-wrapper">
          <input 
            v-model="usuario.contrasenia" 
            type="password" 
            placeholder="Contraseña" 
            :class="{ 'error': errors.contrasenia }"
          />
          <span v-if="errors.contrasenia" class="error-msg">{{ errors.contrasenia }}</span>
        </div>

        <div class="input-wrapper">
          <select v-model="usuario.rol" :class="{ 'error': errors.rol }">
            <option disabled value="">Seleccione su rol</option>
            <option value="ADM">👑 Administrador</option>
            <option value="DOC">👨‍🏫 Docente</option>
            <option value="EST">🎓 Estudiante</option>
          </select>
          <span v-if="errors.rol" class="error-msg">{{ errors.rol }}</span>
        </div>

        <button type="submit" class="submit-btn">
          <span>Crear Cuenta</span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="arrow-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
          </svg>
        </button>
      </form>
      
      <div v-if="mensaje" class="mensaje-wrapper">
        <div class="mensaje success">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="check-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
          {{ mensaje }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegistroUsuario',
  data() {
    return {
      usuario: {
        nombre: '',
        apellido: '',
        email: '',
        contrasenia: '',
        rol: ''
      },
      errors: {},
      mensaje: ''
    }
  },
  methods: {
    validar() {
      this.errors = {}

      if (!this.usuario.nombre) {
        this.errors.nombre = 'El nombre es obligatorio'
      }

      if (!this.usuario.apellido) {
        this.errors.apellido = 'El apellido es obligatorio'
      }

      if (!this.usuario.email) {
        this.errors.email = 'El correo es obligatorio'
      } else if (!this.validarEmail(this.usuario.email)) {
        this.errors.email = 'El correo no es válido'
      }

      if (!this.usuario.contrasenia) {
        this.errors.contrasenia = 'La contraseña es obligatoria'
      } else if (this.usuario.contrasenia.length < 6) {
        this.errors.contrasenia = 'La contraseña debe tener al menos 6 caracteres'
      }

      if (!this.usuario.rol) {
        this.errors.rol = 'Debes seleccionar un rol'
      }

      return Object.keys(this.errors).length === 0
    },
    validarEmail(email) {
      const re = /\S+@\S+\.\S+/
      return re.test(email)
    },
    async registrarUsuario() {
      if (!this.validar()) {
        this.mensaje = ''
        return
      }

      try {
        const response = await axios.post('http://localhost:8000/api/usuarios/', this.usuario)
        this.mensaje = response.data.mensaje || 'Usuario registrado con éxito'
        this.usuario = { nombre: '', apellido: '', email: '', contrasenia: '', rol: '' }
        this.errors = {}
      } catch (error) {
        this.mensaje = 'Error al registrar el usuario'
        console.error(error.response?.data || error)
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.registro-container {
  width: 100vw;
  height: 100vh;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  padding: 1rem;
}

.form-card {
  background: #ffffff;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
  border: 1px solid #e0e0e0;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: #2563eb;
  border-radius: 12px;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.user-icon {
  width: 28px !important;
  height: 28px !important;
  min-width: 28px;
  min-height: 28px;
  max-width: 28px;
  max-height: 28px;
  color: #ffffff;
}

.form-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #000000;
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.form-subtitle {
  color: #666666;
  font-size: 0.95rem;
  margin: 0;
  font-weight: 500;
  line-height: 1.4;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.input-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

input,
select {
  padding: 0.875rem 1rem;
  font-size: 0.95rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s ease;
  background: #ffffff;
  font-weight: 500;
  width: 100%;
  box-sizing: border-box;
  color: #333333;
}

input:focus,
select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

input.error,
select.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

input::placeholder {
  color: #999999;
  font-weight: 400;
}

select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%232563eb' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.2em 1.2em;
  padding-right: 2.5rem;
}

.submit-btn {
  padding: 0.875rem 1.5rem;
  font-size: 1rem;
  background: #2563eb;
  color: #ffffff;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
  width: 100%;
}

.submit-btn:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
}

.submit-btn:active {
  transform: translateY(0);
}

.arrow-icon {
  width: 16px !important;
  height: 16px !important;
  min-width: 16px;
  min-height: 16px;
  max-width: 16px;
  max-height: 16px;
  transition: transform 0.3s ease;
}

.submit-btn:hover .arrow-icon {
  transform: translateX(3px);
}

.mensaje-wrapper {
  margin-top: 1rem;
}

.mensaje {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
}

.mensaje.success {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.check-icon {
  width: 16px !important;
  height: 16px !important;
  min-width: 16px;
  min-height: 16px;
  max-width: 16px;
  max-height: 16px;
  flex-shrink: 0;
}

.error-msg {
  color: #ef4444;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error-msg::before {
  content: "⚠️";
  font-size: 0.7rem;
}

/* Responsive */
@media (max-width: 640px) {
  .registro-container {
    padding: 0.75rem;
  }
  
  .form-card {
    padding: 1.5rem;
    max-width: 100%;
  }
  
  .input-group {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .form-title {
    font-size: 1.6rem;
  }
  
  .form-subtitle {
    font-size: 0.9rem;
  }
  
  input, select {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
  
  .submit-btn {
    padding: 0.8rem;
    font-size: 0.95rem;
  }

  .icon-wrapper {
    width: 36px !important;
    height: 36px !important;
  }
  .user-icon {
    width: 18px !important;
    height: 18px !important;
  }
}

@media (min-width: 768px) {
  .form-card {
    padding: 3rem;
    max-width: 600px;
  }
  
  .form-title {
    font-size: 2rem;
  }
  
  .form-subtitle {
    font-size: 1.1rem;
  }
  
  .icon-wrapper {
    width: 70px;
    height: 70px;
  }
  
  .user-icon {
    width: 35px;
    height: 35px;
  }
  
  input, select {
    padding: 1rem 1.25rem;
    font-size: 1rem;
  }
  
  .submit-btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
  }
  
  .input-group {
    gap: 1.5rem;
  }
  
  .form-content {
    gap: 1.5rem;
  }
}
</style>