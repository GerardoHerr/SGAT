<template>
  <div class="usuarios-container">
    <!-- Header Bar -->
    <div class="header-bar">
      <h2 class="page-title">Gestión de Usuarios</h2>
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
      <div>
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
      </div>
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
            <input v-model="usuarioForm.email" type="email" placeholder="usuario@unl.edu.ec"
              :class="{ 'error': errors.email }" :disabled="editando" />
            <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
          </div>

          <div class="input-wrapper">
            <input v-model="usuarioForm.contrasenia" type="password"
              :placeholder="editando ? 'Nueva contraseña (opcional)' : 'Contraseña'"
              :class="{ 'error': errors.contrasenia }"
              @input="validarContraseniaEnTiempoReal" />
            <!-- Barra de nivel de seguridad visual y texto -->
            <div v-if="usuarioForm.contrasenia">
              <div class="password-strength-bar">
                <div :class="['strength', strengthClass]" :style="{ width: strengthPercent + '%' }"></div>
              </div>
              <div class="password-strength-text" :class="strengthClass">
                {{ strengthText }}
              </div>
            </div>
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
    },
    strengthScore() {
      const c = this.usuarioForm.contrasenia || ''
      let score = 0
      if (c.length >= 6) score++
      if (/[A-Z]/.test(c)) score++
      if (/[a-z]/.test(c)) score++
      if (/[0-9]/.test(c)) score++
      if (/[^A-Za-z0-9]/.test(c)) score++
      return score
    },
    strengthPercent() {
      // 0-5 pasos
      return (this.strengthScore / 5) * 100
    },
    strengthClass() {
      if (this.strengthScore <= 1) return 'weak'
      if (this.strengthScore === 2) return 'medium'
      if (this.strengthScore >= 3) return 'strong'
      return ''
    },
    strengthText() {
      if (!this.usuarioForm.contrasenia) return ''
      if (this.strengthClass === 'weak') return 'Débil'
      if (this.strengthClass === 'medium') return 'Media'
      if (this.strengthClass === 'strong') return 'Fuerte'
      return ''
    }
  },
   watch: {
    'usuarioForm.email'(nuevo) {
      // Solo mostrar error si hay algo escrito y no es válido
      if (nuevo && !this.validarEmail(nuevo)) {
        this.errors.email = 'El correo debe ser institucional (@unl.edu.ec)';
      } else if (!nuevo) {
        this.errors.email = '';
      } else {
        this.errors.email = '';
      }
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

      // Validación nombre
      if (!this.usuarioForm.nombre.trim()) {
        this.errors.nombre = 'El nombre es obligatorio'
      } else if (/[0-9]/.test(this.usuarioForm.nombre)) {
        this.errors.nombre = 'El nombre no debe contener números'
      }

      // Validación apellido
      if (!this.usuarioForm.apellido.trim()) {
        this.errors.apellido = 'El apellido es obligatorio'
      } else if (/[0-9]/.test(this.usuarioForm.apellido)) {
        this.errors.apellido = 'El apellido no debe contener números'
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
      // Solo permite correos que terminen en @unl.edu.ec
      const re = /^[a-zA-Z0-9._%+-]+@unl\.edu\.ec$/
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
        await this.cargarUsuarios()
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

<style scoped lang="scss">
/* Texto de nivel de seguridad de contraseña */
.password-strength-text {
  font-size: 0.95em;
  margin-top: 0.2em;
  font-weight: 600;
  color: #888;
}
.password-strength-text.weak {
  color: #f44336;
}
.password-strength-text.medium {
  color: #ff9800;
}
.password-strength-text.strong {
  color: #4caf50;
}
/* Barra de nivel de seguridad de contraseña */
.password-strength-bar {
  width: 100%;
  height: 8px;
  background: #eee;
  border-radius: 4px;
  margin: 0.3em 0 0.5em 0;
  overflow: hidden;
}
.password-strength-bar .strength {
  height: 100%;
  transition: width 0.3s;
}
.password-strength-bar .strength.weak {
  background: #f44336;
}
.password-strength-bar .strength.medium {
  background: #ff9800;
}
.password-strength-bar .strength.strong {
  background: #4caf50;
}
@import '@/assets/styles/variables';
@import '@/assets/styles/base';
.usuarios-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  min-height: 80vh;
  box-sizing: border-box;
  background: #fff;

  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}



.header-bar {
  display: flex;
  justify-content: left;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid $border-color;
}

  .page-title {
    margin: 0;
    color: $text-primary;
    font-size: 1.8rem;
    font-weight: 600;
  }

.add-btn {
  @extend .btn;
  @extend .btn-primary;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  padding: 0.6rem 1.2rem;
  width: auto;
  min-width: 140px;
  max-width: 100%;
  box-sizing: border-box;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-left: 55%;
  svg {
    width: 1.2rem;
    height: 1.2rem;
  }
}

.search-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: $bg-lighter;
  border-radius: $border-radius;
  box-shadow: $shadow-sm;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 800px;
  margin: 0 auto;
  gap: 0.5rem;
}

.search-icon {
  position: absolute;
  left: 1rem;
  color: $text-secondary;
  pointer-events: none;
  
  svg {
    width: 1.25rem;
    height: 1.25rem;
  }
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 1px solid $border-color;
  border-radius: $border-radius 0 0 $border-radius;
  background: $bg-white;
  color: $text-primary;
  font-size: 0.95rem;
  transition: $transition-base;
  
  &::placeholder {
    color: $text-secondary;
  }
  
  &:focus {
    outline: none;
    border-color: $color-primary;
    box-shadow: 0 0 0 2px rgba($color-primary, 0.2);
  }
}

.search-filter {
  padding: 0 1rem;
  height: 3rem;
  background: $bg-white;
  color: $text-primary;
  border: 1px solid $border-color;
  border-left: none;
  border-radius: 0 $border-radius $border-radius 0;
  cursor: pointer;
  transition: $transition-base;
  font-size: 0.95rem;
  
  &:hover {
    background: $bg-lighter;
  }
  
  &:focus {
    outline: none;
    border-color: $color-primary;
  }
}

/* Tabla */
.table-container {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  background: #fff;
  max-height: calc(100vh - 300px);
  min-height: 300px;
  position: relative;
  overflow: hidden;
  
  > div {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    overflow: auto;
    padding-right: 8px; /* Space for scrollbar */
    
    &::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 4px;
      margin: 4px 0;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #c1c1c1;
      border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb:hover {
      background: #a8a8a8;
    }
  }
}

.usuarios-table {
  width: 100%;
  background: white;
  font-size: 0.9rem;
  table-layout: fixed;
  min-width: 100%;
  margin: 0;
  
  thead {
    position: sticky;
    top: 0;
    z-index: 10;
    background: #fff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  th, td {
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid #e0e0e0;
    vertical-align: middle;
  }
  
  /* Specific column widths */
  th:nth-child(1), td:nth-child(1) { width: 50px; }  /* # */
  th:nth-child(2), td:nth-child(2) { width: 250px; } /* Email */
  th:nth-child(3), td:nth-child(3) { width: 150px; } /* Nombres */
  th:nth-child(4), td:nth-child(4) { width: 150px; } /* Apellidos */
  th:nth-child(5), td:nth-child(5) { width: 120px; } /* Rol */
  th:nth-child(6), td:nth-child(6) { width: 100px; } /* Estado */
  th:nth-child(7), td:nth-child(7) { width: 120px; } /* Opciones */
  
  /* Handle long text */
  td {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 0;
    
    /* Show full text on hover */
    &:hover {
      overflow: visible;
      position: relative;
      z-index: 1;
      background: white;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      white-space: normal;
      word-break: break-word;
    }
  }
  
  th {
    background: $bg-lighter;
    color: $text-secondary;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
  }
  
  td {
    color: $text-primary;
    vertical-align: middle;
  }
  
  tr:last-child td {
    border-bottom: none;
  }
  
  tr:hover {
    background: rgba($color-primary, 0.03);
  }
  
  .row-even {
    background: $bg-lighter;
  }
}

.actions-cell {
  text-align: center;
}

.action-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  background: none;
  border: 1px solid transparent;
  cursor: pointer;
  
  svg {
    width: 1.25rem;
    height: 1.25rem;
  }
  
  &.edit-btn {
    color: #4a6cf7;
    border-color: #4a6cf7;
    
    &:hover {
      background: rgba(74, 108, 247, 0.1);
    }
  }
  
  &.delete-btn {
    color: #f44336;
    border-color: #f44336;
    
    &:hover {
      background: rgba(244, 67, 54, 0.1);
    }
  }
}

/* Badges */
.rol-badge, .status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
  text-align: center;
  min-width: 80px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Rol badges */
.rol-badge {
  &.estudiante {
    background: rgba($color-primary, 0.1);
    color: $color-primary;
    border: 1px solid rgba($color-primary, 0.2);
  }

  &.docente {
    background: rgba($color-primary-dark, 0.1);
    color: $color-primary-dark;
    border: 1px solid rgba($color-primary-dark, 0.2);
  }

  &.admin {
    background: rgba($color-primary, 0.1);
    color: $color-primary;
    border: 1px solid rgba($color-primary, 0.2);
  }
}

/* Status badges */
.status-badge {
  &.active {
    background: rgba($color-primary, 0.1);
    color: $color-primary;
    border: 1px solid rgba($color-primary, 0.2);
  }
  
  &.inactive {
    background: rgba(#f44336, 0.1);
    color: #f44336;
    border: 1px solid rgba(#f44336, 0.2);
  }
  border: 1px solid #9A8F84;
}

/* Estado vacío */
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  min-height: 200px;
  color: #757575;
  font-size: 1.1rem;
  background: #fafafa;
  border-radius: 8px;
  margin: 0;
  padding: 2rem;
  
  p {
    margin: 0;
    padding: 1rem 2rem;
    background: white;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
}

/* Modal overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

/* Modal content */
.modal-content {
  background: $bg-white;
  border-radius: $border-radius;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: $shadow-lg;
  position: relative;
  animation: modalFadeIn 0.3s ease-out;
  border: 1px solid $border-color;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid $border-color;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  h2 {
    margin: 0;
    font-size: 1.5rem;
    color: $text-primary;
  }
}

.close-btn {
  background: none;
  border: none;
  padding: 0.5rem;
  color: #9e9e9e;
  cursor: pointer;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  
  &:hover {
    background: #f5f5f5;
    color: #757575;
  }
  
  svg {
    width: 1.25rem;
    height: 1.25rem;
  }
}

/* Estilos del formulario en modal */
.form-content {
  padding: 1.5rem;
  
  .input-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1rem;
    
    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }
  
  .input-wrapper {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    
    label {
      font-weight: 500;
      color: #333;
      font-size: 0.95rem;
    }
    
    input,
    select {
      width: 100%;
      padding: 0.75rem 1rem;
      font-size: 1rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      background: #fff;
      transition: all 0.2s ease;
      
      &:focus {
        outline: none;
        border-color: #4CAF50;
        box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
      }
      
      &.error {
        border-color: #f44336;
      }
    }
    
    .error-msg {
      color: #f44336;
      font-size: 0.85rem;
      margin-top: 0.25rem;
    }
  }
  
  .submit-btn {
    width: 100%;
    padding: 0.875rem;
    font-size: 1rem;
    font-weight: 600;
    margin-top: 0.5rem;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover:not(:disabled) {
      background: #43A047;
      transform: translateY(-1px);
    }
    
    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
      background: #81C784;
    }
  }
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

/* Confirmation Modal */
.confirmation-modal {
  background: #fff;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  max-width: 500px;
  width: 90%;
  margin: 0 auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
  
  .confirmation-icon {
    width: 4rem;
    height: 4rem;
    margin: 0 auto 1.5rem;
    background: rgba(244, 67, 54, 0.1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    
    svg {
      width: 2rem;
      height: 2rem;
      color: #f44336;
    }
  }
  
  h3 {
    margin: 0 0 1rem;
    color: #333;
    font-size: 1.5rem;
    font-weight: 600;
  }
  
  p {
    margin: 0.5rem 0;
    color: #666;
    line-height: 1.6;
    
    strong {
      color: #333;
      font-weight: 600;
    }
  }
  
  .confirmation-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
    
    .cancel-btn {
      min-width: 100px;
      padding: 0.75rem 1.5rem;
      background: transparent;
      border: 1px solid #757575;
      color: #616161;
      border-radius: 4px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
      
      &:hover {
        background: #f5f5f5;
        border-color: #9e9e9e;
      }
    }
    
    .confirm-btn {
      min-width: 100px;
      padding: 0.75rem 1.5rem;
      background: #f44336;
      color: white;
      border: 1px solid #f44336;
      border-radius: 4px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
      
      &:hover:not(:disabled) {
        background: #e53935;
        transform: translateY(-1px);
      }
      
      &:disabled {
        opacity: 0.7;
        cursor: not-allowed;
      }
    }
  }
}

/* Success Modal */
.modal-exito-titulo {
  color: #4CAF50;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
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
  .header-bar {
    flex-direction: column;
    gap: 1rem;
    justify-content: center;
    align-items: center;
  }
  .page-title {
    font-size: 1.5rem;
  }
  .add-btn {
    width: 100%;
    min-width: 0;
    max-width: 100%;
    padding: 0.7rem 0.5rem;
    font-size: 1rem;
    justify-content: center;
  }
}

.page-title {
  flex: 1;
  text-align: center;
  margin: 0;
  color: #1e293b;
  font-size: 1.8rem;
  font-weight: 600;
}
</style>