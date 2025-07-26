// Servicio de autenticación
export const authService = {
  currentUser: null,

  // Autenticación con el backend
  async login(email, password) {
    try {
      // Hacer login para obtener el token JWT
      const response = await fetch('http://localhost:8000/api/token/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const data = await response.json();
      console.log(data);
      
      if (!response.ok) {
        throw new Error(data.detail || 'Error de autenticación');
      }
      
      // Guardar el token JWT
      if (data.access) {
        localStorage.setItem('access_token', data.access);
        
        // Si el backend devuelve los datos del usuario en la respuesta
        if (data.user) {
          this.currentUser = {
            email: data.user.email,
            nombre: data.user.nombre,
            apellido: data.user.apellido,
            rol: data.user.rol
          };
          
          localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
          return this.currentUser;
        }
        
        // Si no vienen los datos del usuario, hacer una petición para obtenerlos
        const userResponse = await fetch(`http://localhost:8000/api/usuarios/by-email/?email=${encodeURIComponent(email)}`, {
          headers: {
            'Authorization': `Bearer ${data.access}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (userResponse.ok) {
          const usuario = await userResponse.json();
          this.currentUser = {
            email: usuario.email,
            nombre: usuario.nombre,
            apellido: usuario.apellido,
            rol: usuario.rol
          };
          
          localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
          return this.currentUser;
        }
        
        // Si no se pueden obtener los datos del usuario, devolver un error
        throw new Error('No se pudieron obtener los datos del usuario');
      }
      
      throw new Error('Error en la respuesta del servidor');
    } catch (error) {
      console.error('Error en login:', error);
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
