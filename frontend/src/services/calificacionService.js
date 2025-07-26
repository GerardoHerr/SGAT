import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

// Configuración de axios
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir el token a las peticiones
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

const calificacionService = {
  // Obtener todas las calificaciones de una tarea
  async getCalificacionesPorTarea(tareaId) {
    try {
      const response = await api.get(`/calificaciones/por-tarea/${tareaId}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener calificaciones:', error);
      throw error;
    }
  },

  // Obtener estudiantes sin calificar para una tarea
  async getEstudiantesSinCalificar(tareaId) {
    try {
      const response = await api.get(`/calificaciones/estudiantes-sin-calificar/${tareaId}`);
      return response.data;
    } catch (error) {
      console.error('Error al obtener estudiantes sin calificar:', error);
      throw error;
    }
  },

  // Crear o actualizar una calificación
  async guardarCalificacion(calificacionData) {
    try {
      const url = calificacionData.id 
        ? `/calificaciones/${calificacionData.id}/`
        : '/calificaciones/';
      
      const method = calificacionData.id ? 'put' : 'post';
      
      const response = await api({
        method,
        url,
        data: calificacionData
      });
      
      return response.data;
    } catch (error) {
      console.error('Error al guardar la calificación:', error);
      throw error;
    }
  },

  // Obtener calificaciones de un estudiante
  async getCalificacionesEstudiante(estudianteId) {
    try {
      const response = await api.get('/calificaciones/', {
        params: { estudiante_id: estudianteId }
      });
      return response.data;
    } catch (error) {
      console.error('Error al obtener calificaciones del estudiante:', error);
      throw error;
    }
  },
};

export default calificacionService;
