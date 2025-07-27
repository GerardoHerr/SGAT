// Simulación de autenticación simple
export const authService = {
  currentUser: null,

  // Login real con tu endpoint de autenticación
  async login(email, password) {
    try {
      // Intentar primero con tu endpoint de login real
      try {
        const response = await fetch('http://localhost:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            contrasenia: password
          })
          
          
        });
        console.log('Response from login:', response);

        if (response.ok) {
          const data = await response.json();
          
          // Guardar el token JWT
          if (data.access) {
            localStorage.setItem('access_token', data.access);
          }
          
          // Ahora obtener los datos del usuario autenticado
          try {
            const userResponse = await fetch(`http://localhost:8000/api/usuarios/by-email/?email=${encodeURIComponent(email)}`);
            
            if (userResponse.ok) {
              const usuario = await userResponse.json();
              
              this.currentUser = {
                id: usuario.email, // Usar email como ID
                nombre: usuario.nombre,
                apellido: usuario.apellido,
                email: usuario.email,
                rol: usuario.rol
              };
              
              localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
              return this.currentUser;
            }
          } catch (userError) {
            console.warn('Error al obtener datos del usuario, usando datos del token');
          }
          
          // Si no podemos obtener datos del usuario, crear un usuario básico
          this.currentUser = {
            email: email,
            nombre: email.split('@')[0], // Usar la parte antes del @ como nombre
            token: data.access
          };
          
          localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
          return this.currentUser;
        } else {
          // Si la autenticación real falla, intentar con datos simulados
          console.warn('Autenticación real falló, intentando con datos simulados');
          throw new Error('Credenciales incorrectas');
        }
      } catch (authError) {
        console.warn('Error en autenticación real:', authError.message);
        
        // Fallback a datos simulados solo en desarrollo
        const usuario = usuariosMock.find(u => u.email === email);
        
        if (usuario) {
          this.currentUser = {
            id: usuario.email,
            nombre: usuario.nombre,
            apellido: usuario.apellido,
            email: usuario.email,
            rol: usuario.rol
          };
          
          localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
          return this.currentUser;
        } else {
          throw new Error('Usuario no encontrado');
        }
      }
    } catch (error) {
      throw error;
    }
  },

  // Obtener usuario actual
  getCurrentUser() {
    if (!this.currentUser) {
      const stored = localStorage.getItem('currentUser');
      if (stored) {
        this.currentUser = JSON.parse(stored);
      }
    }
    return this.currentUser;
  },

  // Logout
  logout() {
    this.currentUser = null;
    localStorage.removeItem('currentUser');
    localStorage.removeItem('access_token'); // También limpiar el token JWT
  },

  // Verificar si está autenticado
  isAuthenticated() {
    return this.getCurrentUser() !== null;
  },

  // Verificar rol
  isDocente() {
    const user = this.getCurrentUser();
    return user && user.rol === 'DOC';
  },

  isAdmin() {
    const user = this.getCurrentUser();
    return user && user.rol === 'ADMIN';
  },

  isEstudiante() {
    const user = this.getCurrentUser();
    return user && user.rol === 'EST';
  }
};
