// Datos de usuarios simulados para desarrollo
const usuariosMock = [
  {
    id: 1,
    email: 'admin@universidad.edu',
    nombre: 'Admin',
    apellido: 'Sistema',
    rol: 'ADM'
  },
  {
    id: 2,
    email: 'maria.garcia@universidad.edu',
    nombre: 'María',
    apellido: 'García',
    rol: 'DOC'
  },
  {
    id: 3,
    email: 'juan.rodriguez@universidad.edu',
    nombre: 'Juan',
    apellido: 'Rodríguez',
    rol: 'DOC'
  },
  {
    id: 4,
    email: 'ana.lopez@universidad.edu',
    nombre: 'Ana',
    apellido: 'López',
    rol: 'EST'
  }
];

// Simulación de autenticación simple
export const authService = {
  currentUser: null,

  // Simular login con email
  async login(email, password) {
    try {
      // Intentar primero con el backend real
      try {
        const response = await fetch('http://localhost:8000/api/usuarios/');
        if (response.ok) {
          const usuarios = await response.json();
          const usuario = usuarios.find(u => u.email === email);
          
          if (usuario) {
            this.currentUser = {
              id: usuario.id,
              nombre: usuario.nombre,
              apellido: usuario.apellido,
              email: usuario.email,
              rol: usuario.rol
            };
            
            localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
            return this.currentUser;
          }
        }
      } catch (backendError) {
        console.warn('Backend no disponible, usando datos simulados');
      }
      
      // Si el backend falla, usar datos simulados
      const usuario = usuariosMock.find(u => u.email === email);
      
      if (usuario) {
        this.currentUser = {
          id: usuario.id,
          nombre: usuario.nombre,
          apellido: usuario.apellido,
          email: usuario.email,
          rol: usuario.rol
        };
        
        // Guardar en localStorage para persistencia
        localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
        return this.currentUser;
      } else {
        throw new Error('Usuario no encontrado');
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
