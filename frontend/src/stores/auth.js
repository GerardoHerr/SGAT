import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

// URL base de la API (ajusta según tu configuración)
const API_URL = 'http://localhost:8000/api';

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter();
  
  // Estado
  const user = ref(null);
  const token = ref(localStorage.getItem('token') || null);
  const isAuthenticated = computed(() => !!token.value);
  const userRole = computed(() => user.value?.rol || null);
  const userEmail = computed(() => user.value?.email || null);
  
  // Acciones
  async function login(credentials) {
    try {
      const response = await fetch(`${API_URL}/token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error de autenticación');
      }
      
      const data = await response.json();
      
      // Guardar token y datos del usuario
      token.value = data.access;
      localStorage.setItem('token', data.access);
      
      // Obtener información del usuario
      await fetchUserData();
      
      return true;
    } catch (error) {
      console.error('Error en login:', error);
      throw error;
    }
  }
  
  async function fetchUserData() {
    try {
      // Obtener el email del token decodificado
      const tokenParts = token.value.split('.');
      if (tokenParts.length !== 3) {
        throw new Error('Token inválido');
      }
      
      const payload = JSON.parse(atob(tokenParts[1]));
      const userEmail = payload.user_email;
      
      // Obtener los datos del usuario usando el email
      const response = await fetch(`${API_URL}/usuarios/by-email/?email=${encodeURIComponent(userEmail)}`, {
        headers: {
          'Authorization': `Bearer ${token.value}`,
          'Content-Type': 'application/json'
        },
      });
      
      if (!response.ok) {
        throw new Error('Error al obtener datos del usuario');
      }
      
      user.value = await response.json();
      return user.value;
    } catch (error) {
      console.error('Error al obtener datos del usuario:', error);
      logout();
      throw error;
    }
  }
  
  function logout() {
    // Limpiar estado
    user.value = null;
    token.value = null;
    
    // Eliminar token del almacenamiento local
    localStorage.removeItem('token');
    
    // Redirigir al login
    router.push('/login');
  }
  
  // Verificar autenticación al cargar la aplicación
  if (token.value) {
    fetchUserData().catch(() => {
      // Si hay un error al cargar los datos del usuario, hacer logout
      logout();
    });
  }
  
  return {
    // Estado
    user,
    token,
    isAuthenticated,
    userRole,
    userEmail,
    
    // Acciones
    login,
    logout,
    fetchUserData,
  };
});