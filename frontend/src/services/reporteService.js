// Obtener entregas de tareas por curso
export async function getEntregasPorCurso(cursoId) {
  const res = await fetch(`http://localhost:8000/api/entregas/?curso=${cursoId}`);
  if (!res.ok) throw new Error('No se pudieron obtener las entregas');
  return await res.json();
}
// src/services/reporteService.js
// Servicios para generación de reportes de docentes

import { authService } from './authService';

// Obtener cursos del docente autenticado
export async function getCursosDocente() {
  const user = authService.getCurrentUser();
  if (!user || user.rol !== 'DOC') throw new Error('No autenticado como docente');
  // Filtrar por el id o email del docente logeado
  const res = await fetch(`http://localhost:8000/api/cursos/?docente_email=${encodeURIComponent(user.email)}`);
  if (!res.ok) throw new Error('No se pudieron obtener los cursos');
  return await res.json();
}

// Generar reporte para un curso y tipo

// Generar reporte para un curso y tipo (PDF directo)
export async function generarReporteDocente(cursoId, tipo) {
  const user = authService.getCurrentUser();
  if (!user || user.rol !== 'DOC') throw new Error('No autenticado como docente');
  // Ajusta la URL a tu endpoint real de PDF
  const url = `http://localhost:8000/api/reportes/curso/pdf/?curso=${cursoId}&tipo=${tipo}`;
  const res = await fetch(url, {
    method: 'GET',
    headers: {
      // Si necesitas autenticación, agrega el token aquí
      // 'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  });
  if (!res.ok) throw new Error('No se pudo generar el reporte');
  const blob = await res.blob();
  const pdfUrl = window.URL.createObjectURL(blob);
  return { url: pdfUrl };
}

export async function getTareasPorCurso(cursoId) {
  const res = await fetch(`http://localhost:8000/api/asignaciones/?curso=${cursoId}`);
  if (!res.ok) throw new Error('No se pudieron obtener las tareas');
  return await res.json();
}
