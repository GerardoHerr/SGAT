<template>
  <div class="container">
    <div class="left"></div>
    <div class="right">
      <div class="login-box">
        <h2>Iniciar Sesión</h2>


        <form @submit.prevent="handleLogin">
          <div class="input-group">
            <label for="username">Usuario</label>
            <div class="input-icon">
              <i class="fa fa-user"></i>
              <input type="text" v-model="username" id="username" placeholder="Ingresa tu usuario" required />
            </div>
          </div>

          <div class="input-group">
            <label for="password">Contraseña</label>
            <div class="input-icon">
              <i class="fa fa-lock"></i>
              <input type="password" v-model="password" id="password" placeholder="Ingresa tu contraseña" required />
            </div>
          </div>

          <button type="submit">Iniciar Sesión</button>

          <p class="register-text">
            ¿No tienes cuenta? <a href="#">Regístrate</a><br />
            <a href="#">Recuperar contraseña</a>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    handleLogin() {
      if (this.username === 'admin' && this.password === '1234') {
        alert('¡Bienvenido, admin!');
      } else {
        alert('Usuario o contraseña incorrectos');
      }
    }
  }
};

</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body, html {
  height: 100%;
  font-family: 'Segoe UI', sans-serif;
}
.container {
  display: flex;
  height: 100vh;
}

/* Mitad izquierda: imagen de fondo */
.left {
  flex: 1;
  background-image: url('fondo-formulario.jpg');
  background-size: cover;
  background-position: center;
}

/* Mitad derecha: login con recuadro */
.right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f2f2f2;
}

.login-box {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-box h2 {
  margin-bottom: 10px;
  color: #333;
}

.login-image {
  width: 100%;
  max-width: 200px;
  margin: 15px auto;
  display: block;
  border-radius: 8px;
}

/* Grupos de entrada */
.input-group {
  margin-bottom: 15px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  color: #444;
}

/* Íconos dentro del input */
.input-icon {
  position: relative;
}
.input-icon i {
  position: absolute;
  top: 50%;
  left: 10px;
  transform: translateY(-50%);
  color: #888;
}
.input-icon input {
  width: 100%;
  padding: 10px;
  padding-left: 35px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

/* Botón */
button {
  width: 100%;
  padding: 10px;
  background-color: #002147; /* azul marino */
  border: none;
  border-radius: 8px;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}
button:hover {
  background-color: #00152e;
}

/* Texto de registro */
.register-text {
  margin-top: 15px;
  font-size: 14px;
  color: #333;
}
.register-text a {
  color: #0a0a0a;
  text-decoration: none;
  font-weight: bold; /* Negrita */
}

/* Responsive */
@media (max-width: 768px) {
  .container {
    flex-direction: column;
  }
  .left, .right {
    flex: none;
    width: 100%;
    height: 50vh;
  }
  .left {
    order: -1;
  }
}

</style>
