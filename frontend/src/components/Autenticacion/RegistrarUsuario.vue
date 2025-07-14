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
  height: 100vh;
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.form-card {
  background-color: #ffffff;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.15);
  width: 80%;
  height: 90%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.form-title {
  text-align: center;
  font-size: 2rem;
  color: #1f2937;
  margin-bottom: 2rem;
}

.form-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

input,
select {
  padding: 1rem;
  font-size: 1.1rem;
  border: 1px solid #ccc;
  border-radius: 10px;
  outline: none;
}

button {
  padding: 1rem;
  font-size: 1.1rem;
  background-color: #2563eb;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: #1e40af;
}

.mensaje {
  margin-top: 2rem;
  text-align: center;
  color: green;
  font-size: 1.1rem;
}

.error-msg {
  color: red;
  font-size: 0.9rem;
  margin-top: -1rem;
  margin-bottom: 1rem;
  display: block;
}


</style>