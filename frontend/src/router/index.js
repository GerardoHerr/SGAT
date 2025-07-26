import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegistrarUsuario from '../components/Autenticacion/RegistrarUsuario.vue'
import RegistrarAsignatura from '../components/GestionAcademica/RegistrarAsignatura.vue'
import AsignarDocente from '../components/GestionAcademica/AsignarDocente.vue'
import Login from '../components/Autenticacion/Login.vue'
import RegistrarPeriodo from '../components/GestionAcademica/RegistrarPeriodo.vue'
import CursosEstudiante from '../components/GestionAcademica/CursosEstudiante.vue'
import AsignarTarea from '../components/GestionTarea/AsignarTarea.vue'
import ListarTareas from '../components/GestionTarea/ListarTareas.vue'
import GestionGrupos from '../components/GestionTarea/GestionGrupos.vue'
import SolicitarRegistro from '../components/GestionAcademica/SolicitarRegistro.vue'
import AceptarSolicitud from '../components/GestionAcademica/AceptarSolicitud.vue'
import CursosDocente from '../components/GestionAcademica/CursosDocente.vue'
import MostrarTareas from '../components/GestionTarea/MostrarTareas.vue'
import CalificarTarea from '../components/GestionTarea/CalificarTarea.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/registrarUsuario',
      name: 'registrarUsuario',
      component: RegistrarUsuario,
    },
    {
      path: '/admin/usuarios',
      name: 'AdminUsuarios',
      component: RegistrarUsuario,
    },
    {
      path: '/admin/asignaturas',
      name: 'AdminAsignaturas',
      component: RegistrarAsignatura,
    },
    {
      path: '/registrar-asignatura',
      name: 'RegistrarAsignatura',
      component: RegistrarAsignatura,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    { 
      path: '/registrar-periodo',
      name: 'RegistrarPeriodo',
      component: RegistrarPeriodo,
    },
    {
      path: '/estudiante/cursos-estudiante',
      name: 'CursosEstudiante',
      component: CursosEstudiante,
    },
    {
      path: '/estudiante/solicitar-asignatura',
      name: 'SolicitarAsignatura',
      component: SolicitarRegistro,
    },
    {
      path: '/admin/periodos',
      name: 'AdminPeriodos',
      component: RegistrarPeriodo,
    },
    {
      path: '/admin/asignar-docente',
      name: 'AsignarDocente',
      component: AsignarDocente,
    },
    {
      path: '/docente/asignar-tareas',
      name: 'AsignarTareas',
      component: AsignarTarea,
    },
    {
      path: '/docente/entregas',
      name: 'ListarTareas',
      component: ListarTareas,
    },
    {
      path: '/docente/gestion-grupos',
      name: 'GestionGrupos',
      component: GestionGrupos,
    }
  ],
})

export default router
