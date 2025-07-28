<template>
  <div class="container">
    <div class="left"></div>
    <div class="right">
      <div class="login-box">
        <h2>Iniciar Sesión</h2>
        <img 
          src="/src/assets/login-img.png" 
          alt="SGAT Logo" 
          class="login-image"
        >

        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="email">Email</label>
            <div class="input-icon">
              <i class="fa fa-envelope"></i>
              <input type="email" v-model="email" id="email" placeholder="Ingresa tu email" required />
            </div>
          </div>

          <div class="input-group">
            <label for="password">Contraseña</label>
            <div class="input-icon">
              <i class="fa fa-lock"></i>
              <input type="password" v-model="password" id="password" placeholder="Ingresa tu contraseña" required />
            </div>
          </div>

          <button type="submit" :disabled="loading">
            <span v-if="loading">Iniciando sesión...</span>
            <span v-else>Iniciar Sesión</span>
          </button>

          <div v-if="error" class="error-message">
            {{ error }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '@/services/authService'

export default {
  name: 'LoginView',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      loading: false
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';
      
      try {
        console.log('Intentando login con:', this.email);
        
        const user = await authService.login(this.email, this.password);
        
        if (user) {
          console.log('Login exitoso:', user);
          // Redirigir según el rol del usuario
          if (user.rol === 'ADM') {
            this.$router.push('/admin/usuarios');
          } else if (user.rol === 'DOC') {
            this.$router.push('/docente/cursos');
          } else if (user.rol === 'EST') {
            this.$router.push('/estudiante/calendario-tareas');
          } else {
            this.$router.push('/');
          }
        }
      } catch (error) {
        this.error = 'Usuario o contraseña incorrectos';
        console.error('Error en login:', error);
      } finally {
        this.loading = false;
      }
    }
  }
};

</script>

<style scoped>
/* Reset específico para el login */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Container del login - pantalla completa */
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  font-family: 'Segoe UI', sans-serif;
  z-index: 1000;
}

/* Mitad izquierda: imagen de fondo */
.left {
  flex: 1;
  background-image: url('/src/assets/fondo-formulario.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
}

/* Mitad derecha: login con recuadro */
.right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f2f2f2;
  min-height: 100vh;
  padding: 2rem;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
  width: 100%;
  max-width: 450px;
  text-align: center;
}

.login-box h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.8rem;
  font-weight: 600;
}

.login-image {
  width: 100%;
  max-width: 180px;
  height: auto;
  margin: 20px auto 30px auto;
  display: block;
  border-radius: 12px;
}

/* Grupos de entrada */
.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  color: #444;
  font-weight: 500;
  font-size: 14px;
}

/* Íconos dentro del input */
.input-icon {
  position: relative;
}

.input-icon i {
  position: absolute;
  top: 50%;
  left: 15px;
  transform: translateY(-50%);
  color: #888;
  font-size: 16px;
  z-index: 1;
}

.input-icon input {
  width: 100%;
  padding: 15px 20px 15px 45px;
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  background-color: #fafbfc;
}

.input-icon input:focus {
  outline: none;
  border-color: #002147;
  background-color: white;
}

.input-icon input::placeholder {
  color: #a0a0a0;
}

/* Botón */
button {
  width: 100%;
  padding: 15px;
  background-color: #002147;
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

button:hover {
  background-color: #00152e;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 33, 71, 0.3);
}

button:active {
  transform: translateY(0);
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Mensaje de error */
.error-message {
  margin-top: 15px;
  padding: 12px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  color: #c33;
  font-size: 14px;
  text-align: center;
}

/* Texto de registro */
.register-text {
  margin-top: 25px;
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.register-text a {
  color: #002147;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.register-text a:hover {
  color: #00152e;
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }
  
  .left, .right {
    flex: none;
    width: 100%;
    min-height: 50vh;
  }
  
  .left {
    order: -1;
  }
  
  .right {
    padding: 1rem;
  }
  
  .login-box {
    padding: 30px 25px;
    max-width: 100%;
  }
  
  .login-box h2 {
    font-size: 1.5rem;
  }
  
  .login-image {
    max-width: 150px;
    margin: 15px auto 25px auto;
  }
  
  .input-icon input {
    padding: 12px 15px 12px 40px;
    font-size: 16px;
  }
  
  button {
    padding: 12px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .right {
    padding: 0.5rem;
  }
  
  .login-box {
    padding: 25px 20px;
    border-radius: 12px;
  }
}

</style>
