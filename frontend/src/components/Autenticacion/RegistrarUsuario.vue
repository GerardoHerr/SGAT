<template>
  <div class="registro-container">
    <div class="form-card">
      <h2 class="form-title">Registro de Usuario</h2>
      <form @submit.prevent="registrarUsuario" class="form-content">
        <input v-model="usuario.nombre" placeholder="Nombre" />
        <span v-if="errors.nombre" class="error-msg">{{ errors.nombre }}</span>

        <input v-model="usuario.apellido" placeholder="Apellido" />
        <span v-if="errors.apellido" class="error-msg">{{ errors.apellido }}</span>

        <input v-model="usuario.email" type="email" placeholder="Correo" />
        <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>

        <input v-model="usuario.contrasenia" type="password" placeholder="Contraseña" />
        <span v-if="errors.contrasenia" class="error-msg">{{ errors.contrasenia }}</span>

        <select v-model="usuario.rol">
          <option disabled value="">Seleccione rol</option>
          <option value="ADMIN">Administrador</option>
          <option value="DOC">Docente</option>
          <option value="EST">Estudiante</option>
        </select>
        <span v-if="errors.rol" class="error-msg">{{ errors.rol }}</span>

        <button type="submit">Registrar</button>
      </form>
      <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>
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
      errors: {},  // <-- aquí guardamos errores
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
.registro-container {
  width: 100vw;
  min-height: 100vw;
  background: transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin: 0;
  padding: 0;
  position: static;
  overflow: visible;
}

.form-card {
  background: #fff;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  width: 100%;
  max-width: 700px;
  margin: 0 auto;
  box-sizing: border-box;
}

.form-title {
  text-align: center;
  font-size: 1.6rem;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input,
select {
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s ease;
}

input:focus,
select:focus {
  border-color: #2563eb;
}

button {
  padding: 0.8rem;
  font-size: 1rem;
  background-color: #2563eb;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease;
  margin-top: 0.5rem;
}

button:hover {
  background-color: #1e40af;
}

.mensaje {
  margin-top: 1rem;
  text-align: center;
  color: green;
  font-size: 1rem;
}

.error-msg {
  color: red;
  font-size: 0.85rem;
  margin-top: -0.5rem;
  margin-bottom: 0.5rem;
  display: block;
}





</style>