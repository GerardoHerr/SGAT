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
            <span v-else">Registrar</span>
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
      tipoMensaje: ''
    }
  },
  methods: {
  async registrarAsignatura() {
  this.loading = true;
  this.mensaje = '';

  try {
    const response = await fetch('http://localhost:8000/api/asignaturas/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        admin_id: 1,
        codigo: this.form.codigo,
        nombre: this.form.nombre,
        descripcion: this.form.descripcion,
        activa: this.form.activa
      })
    });

    const result = await response.json();
    console.log(result); // ✅ te ayudará a depurar

    if (response.ok) {
      this.mensaje = 'Asignatura registrada correctamente';
      this.tipoMensaje = 'success';
      this.limpiarFormulario();
    } else {
      this.mensaje = result.error || 'Error al registrar la asignatura';
      this.tipoMensaje = 'error';
    }
  } catch (error) {
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

<style scoped>
.registrar-asignatura {
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

.form-group input,
.form-group textarea,
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
.form-group textarea:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
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

.register-btn:hover {
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
  .form-group textarea,
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