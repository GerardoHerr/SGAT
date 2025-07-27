<template>
  <div class="usuarios-container">
    <!-- Header Bar -->
    <div class="header-bar">
      <h1 class="page-title">Gestión de Usuarios</h1>
      <button class="add-btn" @click="mostrarModal = true">
        Agregar Usuario
      </button>
    </div>
    

    <!-- Buscador -->
    <div class="search-section">
      <div class="search-wrapper">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </div>
        <input v-model="busqueda" type="text" placeholder="Buscar por nombre, apellido o email..."
          class="search-input" />
        <select v-model="filtroTipo" class="search-filter">
          <option value="todos">Todos</option>
          <option value="nombre">Nombre</option>
          <option value="apellido">Apellido</option>
          <option value="email">Email</option>
        </select>
      </div>
    </div>

    <!-- Tabla de Usuarios -->
    <div class="table-container">
      <table class="usuarios-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Email</th>
            <th>Nombres</th>
            <th>Apellidos</th>
            <th>Rol</th>
            <th>Estado</th>
            <th>Opciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(usuario, index) in usuariosFiltrados" :key="usuario.email"
            :class="{ 'row-even': index % 2 === 0 }">
            <td>{{ index + 1 }}</td>
            <td>{{ usuario.email }}</td>
            <td>{{ usuario.nombre }}</td>
            <td>{{ usuario.apellido }}</td>
            <td>
              <span class="rol-badge" :class="getRolClass(usuario.rol)">
                {{ getRolText(usuario.rol) }}
              </span>
            </td>
            <td>
              <span class="status-badge" :class="usuario.activo ? 'active' : 'inactive'">
                {{ usuario.activo ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="actions-cell">
              <button class="action-btn edit-btn" @click="editarUsuario(usuario)" title="Editar">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                </svg>
              </button>
              <button class="action-btn delete-btn" @click="confirmarEliminar(usuario)" title="Eliminar">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916C15.75 3.42 14.58 2.25 13.11 2.25h-2.22c-1.47 0-2.64 1.17-2.64 2.64v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="usuariosFiltrados.length === 0" class="empty-state">
        <p>No se encontraron usuarios</p>
      </div>
    </div>

    <!-- Modal para Agregar/Editar Usuario -->
    <div v-if="mostrarModal" class="modal-overlay" @click="cerrarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editando ? 'Editar Usuario' : 'Registro de Usuario' }}</h2>
          <button class="close-btn" @click="cerrarModal">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="guardarUsuario" class="form-content">
          <div class="input-group">
            <div class="input-wrapper">
              <input v-model="usuarioForm.nombre" placeholder="Nombre" :class="{ 'error': errors.nombre }" />
              <span v-if="errors.nombre" class="error-msg">{{ errors.nombre }}</span>
            </div>

            <div class="input-wrapper">
              <input v-model="usuarioForm.apellido" placeholder="Apellido" :class="{ 'error': errors.apellido }" />
              <span v-if="errors.apellido" class="error-msg">{{ errors.apellido }}</span>
            </div>
          </div>

          <div class="input-wrapper">
            <input v-model="usuarioForm.email" type="email" placeholder="Correo electrónico"
              :class="{ 'error': errors.email }" :disabled="editando" />
            <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
          </div>

          <div class="input-wrapper">
            <input v-model="usuarioForm.contrasenia" type="password"
              :placeholder="editando ? 'Nueva contraseña (opcional)' : 'Contraseña'"
              :class="{ 'error': errors.contrasenia }" />
            <span v-if="errors.contrasenia" class="error-msg">{{ errors.contrasenia }}</span>
          </div>

          <div class="input-wrapper">
            <select v-model="usuarioForm.rol" :class="{ 'error': errors.rol }">
              <option disabled value="">Seleccione su rol</option>
              <option value="ADM">👑 Administrador</option>
              <option value="DOC">👨‍🏫 Docente</option>
              <option value="EST">🎓 Estudiante</option>
            </select>
            <span v-if="errors.rol" class="error-msg">{{ errors.rol }}</span>
          </div>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="loading">{{ editando ? 'Actualizando...' : 'Registrando...' }}</span>
            <span v-else>{{ editando ? 'Actualizar Usuario' : 'Crear Cuenta' }}</span>
          </button>
        </form>

        <div v-if="mensaje" class="mensaje-wrapper">
          <div class="mensaje" :class="tipoMensaje">
            {{ mensaje }}
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Confirmación para Eliminar -->
    <div v-if="mostrarConfirmacion" class="modal-overlay" @click="cancelarEliminar">
      <div class="confirmation-modal" @click.stop>
        <div class="confirmation-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
          </svg>
        </div>
        <h3>¿Eliminar Usuario?</h3>
        <p>¿Estás seguro de que deseas eliminar a <strong>{{ usuarioAEliminar?.nombre }} {{ usuarioAEliminar?.apellido
            }}</strong>?</p>
        <p>Esta acción no se puede deshacer.</p>
        <div class="confirmation-actions">
          <button class="cancel-btn" @click="cancelarEliminar">Cancelar</button>
          <button class="confirm-btn" @click="eliminarUsuario" :disabled="loading">
            {{ loading ? 'Eliminando...' : 'Eliminar' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="mostrarModalExito" class="modal-overlay" @click="cerrarModalExito">
      <div class="confirmation-modal" @click.stop>
        <h2 class="modal-exito-titulo">{{ mensajeExito }}</h2>
        <button class="cancel-btn" @click="cerrarModalExito">Aceptar</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GestionUsuarios',
  data() {
    return {
      usuarios: [],
      usuarioForm: {
        nombre: '',
        apellido: '',
        email: '',
        contrasenia: '',
        rol: ''
      },
      usuarioAEliminar: null,
      errors: {},
      mensaje: '',
      tipoMensaje: '',
      loading: false,
      editando: false,
      mostrarModal: false,
      mostrarConfirmacion: false,
      busqueda: '',
      filtroTipo: 'todos',
      mostrarModalExito: false,
    mensajeExito: '',
    }
  },
  computed: {
    usuariosFiltrados() {
      if (!this.busqueda.trim()) return this.usuarios
      
      const texto = this.busqueda.toLowerCase().trim()
      
      return this.usuarios.filter(usuario => {
        switch (this.filtroTipo) {
          case 'nombre':
            return usuario.nombre.toLowerCase().includes(texto)
          case 'apellido':
            return usuario.apellido.toLowerCase().includes(texto)
          case 'email':
            return usuario.email.toLowerCase().includes(texto)
          default:
            return usuario.nombre.toLowerCase().includes(texto) ||
                   usuario.apellido.toLowerCase().includes(texto) ||
                   usuario.email.toLowerCase().includes(texto)
        }
      })
    }
  },
  async mounted() {
    await this.cargarUsuarios()
  },
  methods: {
    mostrarModalGuardado(tipo) {
      if (tipo === 'guardar') {
        this.mensajeExito = this.editando ? 'Usuario guardado correctamente.' : 'Usuario creado correctamente.';
      } else if (tipo === 'eliminar') {
        this.mensajeExito = 'Usuario eliminado correctamente.';
      }
      this.mostrarModalExito = true;
    },
    cerrarModalExito() {
      this.mostrarModalExito = false;
    },

    async cargarUsuarios() {
      try {
        const response = await axios.get('http://localhost:8000/api/usuarios/')
        this.usuarios = response.data.results || response.data || []
      } catch (error) {
        console.error('Error al cargar usuarios:', error)
        this.mostrarMensaje('Error al cargar usuarios', 'error')
      }
    },

    editarUsuario(usuario) {
      this.editando = true
      this.usuarioForm = {
        nombre: usuario.nombre,
        apellido: usuario.apellido,
        email: usuario.email,
        rol: usuario.rol,
        contrasenia: ''
      }
      this.mostrarModal = true
      this.limpiarErrores()
    },

    confirmarEliminar(usuario) {
      this.usuarioAEliminar = usuario
      this.mostrarConfirmacion = true
    },

    async eliminarUsuario() {
      if (!this.usuarioAEliminar) return
      
      this.loading = true
      try {
        //const emailEncoded = encodeURIComponent(this.usuarioAEliminar.email)
        await axios.delete(`http://localhost:8000/api/usuarios/by-email/?email=${this.usuarioAEliminar.email}`)

        // Remover de la lista local
        this.usuarios = this.usuarios.filter(u => u.email !== this.usuarioAEliminar.email)
        
        this.mostrarMensaje('Usuario eliminado con éxito', 'success')
        this.mostrarModalGuardado('eliminar')
        this.cancelarEliminar()
      } catch (error) {
        console.error('Error al eliminar usuario:', error)
        this.mostrarMensaje('Error al eliminar usuario', 'error')
      } finally {
        this.loading = false
      }
    },

    cancelarEliminar() {
      this.mostrarConfirmacion = false
      this.usuarioAEliminar = null
    },

    validar() {
      this.errors = {}

      if (!this.usuarioForm.nombre.trim()) {
        this.errors.nombre = 'El nombre es obligatorio'
      }

      if (!this.usuarioForm.apellido.trim()) {
        this.errors.apellido = 'El apellido es obligatorio'
      }

      if (!this.usuarioForm.email.trim()) {
        this.errors.email = 'El correo es obligatorio'
      } else if (!this.validarEmail(this.usuarioForm.email)) {
        this.errors.email = 'El correo no es válido'
      }

      if (!this.editando) {
        if (!this.usuarioForm.contrasenia) {
          this.errors.contrasenia = 'La contraseña es obligatoria'
        } else if (this.usuarioForm.contrasenia.length < 6) {
          this.errors.contrasenia = 'La contraseña debe tener al menos 6 caracteres'
        }
      } else {
        // Al editar, la contraseña es opcional pero si se proporciona debe ser válida
        if (this.usuarioForm.contrasenia && this.usuarioForm.contrasenia.length < 6) {
          this.errors.contrasenia = 'La contraseña debe tener al menos 6 caracteres'
        }
      }

      if (!this.usuarioForm.rol) {
        this.errors.rol = 'Debes seleccionar un rol'
      }

      return Object.keys(this.errors).length === 0
    },

    validarEmail(email) {
      const re = /\S+@\S+\.\S+/
      return re.test(email)
    },

    async guardarUsuario() {
      if (!this.validar()) {
        this.mensaje = ''
        return
      }

      this.loading = true
      try {
        if (this.editando) {
          // Actualizar usuario
          const updateData = {
            nombre: this.usuarioForm.nombre,
            apellido: this.usuarioForm.apellido,
            rol: this.usuarioForm.rol
          }

          // Solo incluir contraseña si se proporcionó una nueva
          if (this.usuarioForm.contrasenia) {
            updateData.contrasenia = this.usuarioForm.contrasenia
          }
          //const emailEncoded = encodeURIComponent(this.usuarioForm.email)
          //const response = await axios.put(`http://localhost:8000/api/usuarios/${emailEncoded}/`, updateData)
          const response =await axios.put(`http://localhost:8000/api/usuarios/by-email/?email=${this.usuarioForm.email}`, updateData)

          // Actualizar en la lista local
          const index = this.usuarios.findIndex(u => u.email === this.usuarioForm.email)
          if (index !== -1) {
            this.usuarios[index] = { ...this.usuarios[index], ...response.data }
          }
          
          this.mostrarModalGuardado('guardar')
        } else {
          // Crear nuevo usuario
          const response = await axios.post('http://localhost:8000/api/usuarios/', this.usuarioForm)
          
          // Agregar a la lista local
          this.usuarios.push(response.data)
          
          this.mostrarModalGuardado('guardar')
        }
        
        this.cerrarModal()
      } catch (error) {
        console.error('Error al guardar usuario:', error)
        this.mostrarMensaje(
          this.editando ? 'Error al actualizar usuario' : 'Error al registrar usuario', 
          'error'
        )
      } finally {
        this.loading = false
      }
    },

    cerrarModal() {
      this.mostrarModal = false
      this.editando = false
      this.limpiarFormulario()
      this.limpiarErrores()
    },

    limpiarFormulario() {
      this.usuarioForm = {
        nombre: '',
        apellido: '',
        email: '',
        contrasenia: '',
        rol: ''
      }
    },

    limpiarErrores() {
      this.errors = {}
      this.mensaje = ''
    },

    mostrarMensaje(texto, tipo) {
      this.mensaje = texto
      this.tipoMensaje = tipo
      setTimeout(() => {
        this.mensaje = ''
      }, 5000)
    },

    getRolClass(rol) {
      const classes = {
        'ADM': 'admin',
        'DOC': 'docente',
        'EST': 'estudiante'
      }
      return classes[rol] || 'default'
    },

    getRolText(rol) {
      const textos = {
        'ADM': 'Administrador',
        'DOC': 'Docente',
        'EST': 'Estudiante'
      }
      return textos[rol] || rol
    }
  }
}
</script>

<style scoped>
/* Contenedor principal con borde */
.usuarios-container {
  padding: 2rem;
  background: #323232;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #DDD0C8;
  border: 3px solid #9A8F84;
  border-radius: 12px;
  margin: 1rem;
}

/* Header Bar */
.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.add-btn {
  background: #C4B8AD;
  color: #323232;
  border: 2px solid #9A8F84;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover {
  background: #9A8F84;
  color: #DDD0C8;
  transform: translateY(-1px);
}

/* Título */
.page-title {
  flex: 1;
  font-size: 2rem;
  font-weight: 700;
  color: #9A8F84;
  margin-bottom: 1.5rem;
  margin: 0;
  text-align: center;
}

/* Sección de búsqueda */
.search-section {
  margin-bottom: 1.5rem;
}

.search-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  max-width: 600px;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #9A8F84;
  z-index: 1;
}

.search-icon svg {
  width: 20px;
  height: 20px;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid #7A6F66;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #7A6F66;
  color: #DDD0C8;
}

.search-input:focus {
  outline: none;
  border-color: #C4B8AD;
  box-shadow: 0 0 0 3px rgba(196, 184, 173, 0.2);
}

.search-input::placeholder {
  color: #9A8F84;
}

.search-filter {
  padding: 0.75rem 1rem;
  border: 2px solid #7A6F66;
  border-radius: 8px;
  background: #7A6F66;
  color: #DDD0C8;
  cursor: pointer;
  min-width: 120px;
}

.search-filter:focus {
  outline: none;
  border-color: #C4B8AD;
}

/* Tabla */
.table-container {
  background: #7A6F66;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
  border: 2px solid #9A8F84;
}

.usuarios-table {
  width: 100%;
  border-collapse: collapse;
}

.usuarios-table th {
  background: #9A8F84;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #323232;
  border-bottom: 2px solid #C4B8AD;
  font-size: 0.9rem;
}

.usuarios-table td {
  padding: 1rem;
  border-bottom: 1px solid #9A8F84;
  font-size: 0.9rem;
  color: #DDD0C8;
}

.row-even {
  background: rgba(154, 143, 132, 0.1);
}

.actions-cell {
  text-align: center;
}

.action-btn {
  background: none;
  border: 2px solid transparent;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  margin: 0 0.25rem;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.edit-btn {
  color: #C4B8AD;
  background: rgba(196, 184, 173, 0.1);
  border-color: #C4B8AD;
}

.edit-btn:hover {
  background: #C4B8AD;
  color: #323232;
}

.delete-btn {
  color: #DDD0C8;
  background: rgba(221, 208, 200, 0.1);
  border-color: #DDD0C8;
}

.delete-btn:hover {
  background: #DDD0C8;
  color: #323232;
}

/* Badges */
.rol-badge, .status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  background: #C4B8AD;
  color: #323232;
  border: 1px solid #9A8F84;
}

/* Estado vacío */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #9A8F84;
}

/* Modal overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(50, 50, 50, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

/* Modal content */
.modal-content {
  background: #7A6F66;
  border: 2px solid #9A8F84;
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  color: #DDD0C8;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid #9A8F84;
}

.modal-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #9A8F84;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  color: #9A8F84;
  border-radius: 4px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(196, 184, 173, 0.2);
  color: #C4B8AD;
}

.close-btn svg {
  width: 20px;
  height: 20px;
}

/* Estilos del formulario en modal */
.form-content {
  padding: 1.5rem;
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

.form-content input,
.form-content select {
  padding: 0.875rem 1rem;
  font-size: 0.95rem;
  border: 2px solid #9A8F84;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s ease;
  background: #7A6F66;
  font-weight: 500;
  width: 100%;
  box-sizing: border-box;
  color: #DDD0C8;
}

.form-content input::placeholder {
  color: #9A8F84;
}

.form-content input:focus,
.form-content select:focus {
  border-color: #C4B8AD;
  box-shadow: 0 0 0 3px rgba(196, 184, 173, 0.2);
}

.form-content input.error,
.form-content select.error {
  border-color: #DDD0C8;
  box-shadow: 0 0 0 3px rgba(221, 208, 200, 0.2);
}

.form-content input:disabled {
  background: #323232;
  color: #7A6F66;
  cursor: not-allowed;
  border-color: #7A6F66;
}

.form-content select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23C4B8AD' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.2em 1.2em;
  padding-right: 2.5rem;
}

.submit-btn {
  padding: 0.875rem 1.5rem;
  font-size: 1rem;
  background: #C4B8AD;
  color: #323232;
  font-weight: 600;
  border: 2px solid #9A8F84;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background: #9A8F84;
  color: #DDD0C8;
  transform: translateY(-2px);
}

.submit-btn:disabled {
  background: #7A6F66;
  color: #9A8F84;
  cursor: not-allowed;
  transform: none;
  border-color: #7A6F66;
}

.error-msg {
  color: #DDD0C8;
  font-size: 0.8rem;
  font-weight: 600;
}

.mensaje-wrapper {
  padding: 0 1.5rem 1.5rem;
}

.mensaje {
  padding: 0.875rem 1rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  border: 2px solid;
}

.mensaje.success {
  background: rgba(196, 184, 173, 0.2);
  color: #C4B8AD;
  border-color: #C4B8AD;
}

.mensaje.error {
  background: rgba(221, 208, 200, 0.2);
  color: #DDD0C8;
  border-color: #DDD0C8;
}

/* Modal de confirmación */
.confirmation-modal {
  background: #7A6F66;
  border: 2px solid #9A8F84;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  max-width: 400px;
  width: 100%;
  color: #DDD0C8;
}

.confirmation-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  background: rgba(221, 208, 200, 0.2);
  border: 2px solid #DDD0C8;
  border-radius: 50%;
  color: #DDD0C8;
  margin-bottom: 1rem;
}

.confirmation-icon svg {
  width: 24px;
  height: 24px;
}

.confirmation-modal h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #9A8F84;
  margin-bottom: 0.5rem;
}

.confirmation-modal p {
  color: #DDD0C8;
  margin-bottom: 1rem;
}

.confirmation-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.cancel-btn, .confirm-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid;
}

.cancel-btn {
  background: #7A6F66;
  color: #9A8F84;
  border-color: #9A8F84;
}

.cancel-btn:hover {
  background: #9A8F84;
  color: #323232;
}

.confirm-btn {
  background: #C4B8AD;
  color: #323232;
  border-color: #9A8F84;
}

.confirm-btn:hover:not(:disabled) {
  background: #9A8F84;
  color: #DDD0C8;
}

.confirm-btn:disabled {
  background: #7A6F66;
  color: #9A8F84;
  cursor: not-allowed;
  border-color: #7A6F66;
}

.modal-exito-titulo {
  color: #9A8F84;
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .usuarios-container {
    padding: 1rem;
    margin: 0.5rem;
  }
  
  .input-group {
    grid-template-columns: 1fr;
  }
  
  .search-wrapper {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .usuarios-table {
    font-size: 0.8rem;
  }
  
  .usuarios-table th,
  .usuarios-table td {
    padding: 0.75rem 0.5rem;
  }
  
  .page-title {
    font-size: 1.5rem;
  }
}
</style>