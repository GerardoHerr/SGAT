<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Iniciar Sesión - SGAT</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email:</label>
          <input 
            v-model="email" 
            type="email" 
            placeholder="usuario@universidad.edu"
            required
          >
        </div>
        
        <div class="form-group">
          <label>Contraseña:</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="********"
            required
          >
        </div>
        
        <button type="submit" :disabled="loading" class="login-btn">
          <span v-if="loading">Iniciando sesión...</span>
          <span v-else>Iniciar Sesión</span>
        </button>
      </form>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <!-- Información de autenticación -->
      <div class="auth-info">
        <p><strong>Autenticación Real:</strong> Usa tus credenciales reales del sistema</p>
        <p><em>Si falla la autenticación real, se usarán los usuarios de prueba como fallback</em></p>
      </div>
      
      <!-- Usuarios de prueba -->
      <div class="demo-users">
        <h3>Usuarios de Prueba (Fallback):</h3>
        <div class="user-demo" @click="setDemoUser('admin@universidad.edu')">
          <strong>Administrador:</strong> admin@universidad.edu
        </div>
        <div class="user-demo" @click="setDemoUser('maria.garcia@universidad.edu')">
          <strong>Docente:</strong> maria.garcia@universidad.edu
        </div>
        <div class="user-demo" @click="setDemoUser('juan.rodriguez@universidad.edu')">
          <strong>Docente:</strong> juan.rodriguez@universidad.edu
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '@/services/authService.js'

export default {
  name: 'LoginComponent',
  data() {
    return {
      email: '',
      password: '123456',
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';
      
      try {
        const user = await authService.login(this.email, this.password);
        
        // Redirigir según el rol
        if (user.rol === 'ADMIN') {
          this.$router.push('/admin/usuarios');
        } else if (user.rol === 'DOC') {
          this.$router.push('/docente/asignar-tareas');
        } else {
          this.$router.push('/');
        }
        
        // Recargar la página para actualizar el AppLayout
        window.location.reload();
        
      } catch (error) {
        this.error = 'Error al iniciar sesión. Verifique sus credenciales.';
      }
      
      this.loading = false;
    },
    
    setDemoUser(email) {
      this.email = email;
      this.password = '123456';
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #323232;
  padding: 2rem;
}

.login-card {
  background: #DDD0C8;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  width: 100%;
  max-width: 450px;
}

.login-card h2 {
  text-align: center;
  color: #323232;
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 600;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #323232;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #323232;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
}

.login-btn {
  width: 100%;
  padding: 1rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.login-btn:hover:not(:disabled) {
  background: #2980b9;
}

.login-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-top: 1rem;
  text-align: center;
}

.auth-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #e3f2fd;
  border-radius: 0.5rem;
  border-left: 4px solid #3498db;
}

.auth-info p {
  margin: 0.5rem 0;
  color: #323232;
  font-size: 0.9rem;
}

.auth-info em {
  color: #666;
  font-size: 0.8rem;
}

.demo-users {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 2px solid #323232;
}

.demo-users h3 {
  color: #323232;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.user-demo {
  background: white;
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #ddd;
}

.user-demo:hover {
  background: #f8f9fa;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.user-demo strong {
  color: #3498db;
}
</style>
