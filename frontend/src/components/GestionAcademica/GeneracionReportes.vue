<template>
  <div class="reporte-container">
    <h2><i class="fa fa-file-alt"></i> Generación de Reportes</h2>
    <div class="reporte-form">
      <div class="form-group">
        <label for="curso"><i class="fa fa-chalkboard-teacher"></i> Curso</label>
        <div class="input-icon-group">
          <i class="fa fa-book"></i>
          <select v-model="cursoSeleccionado" id="curso" @change="fetchTareas">
            <option disabled value="">Seleccione un curso</option>
            <option v-for="curso in cursos" :key="curso.id" :value="curso.id">
              {{ curso.asignatura_nombre }} - {{ curso.periodo }}
            </option>
          </select>
        </div>
      </div>
      <div class="form-group">
        <label for="tipo"><i class="fa fa-file-alt"></i> Tipo de reporte</label>
        <div class="input-icon-group">
          <i class="fa fa-list"></i>
          <select v-model="tipoReporte" id="tipo" @change="fetchTareas">
            <option disabled value="">Seleccione tipo</option>
            <option value="entregas">Entregas de tareas</option>
            <option value="tareas">Tareas del curso</option>
          </select>
        </div>
      </div>

      <!-- No mostrar entregas en pantalla, solo cargarlas para el PDF -->
      <!-- No mostrar tareas en pantalla, solo cargarlas para el PDF -->
      
      
      <button class="btn-generar" :disabled="!cursoSeleccionado || !tipoReporte || cargando" @click="generarReporte">
        <span v-if="cargando"><i class="fa fa-spinner fa-spin"></i> Generando...</span>
        <span v-else><i class="fa fa-download"></i> Generar Reporte</span>
      </button>
    </div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="reporteUrl" class="reporte-descarga">
      <a :href="reporteUrl" target="_blank" download>
        <i class="fa fa-file-pdf"></i> Descargar reporte
      </a>
    </div>
    <div v-if="reporteHtml" class="reporte-preview" v-html="reporteHtml"></div>
  </div>
</template>

<script>


import { ref, onMounted } from 'vue';
import { getCursosDocente, generarReporteDocente, getTareasPorCurso, getEntregasPorCurso } from '@/services/reporteService';

export default {
  name: 'GeneracionReportes',
  setup() {

    const cursos = ref([]);
    const cursoSeleccionado = ref('');
    const tipoReporte = ref('');
    const tareas = ref([]);
    const entregas = ref([]);
    const cargando = ref(false);
    const error = ref('');
    const reporteUrl = ref('');
    const reporteHtml = ref('');


    onMounted(async () => {
      try {
        cursos.value = await getCursosDocente();
        //console.log('Cursos obtenidos:', cursos.value);
      } catch (e) {
        error.value = 'No se pudieron cargar los cursos.';
      }
    });


    async function fetchTareas() {
      tareas.value = [];
      entregas.value = [];
      if (tipoReporte.value === 'entregas' && cursoSeleccionado.value) {
        try {
          // Primero obtenemos las tareas del curso seleccionado
          const tareasCurso = await getTareasPorCurso(cursoSeleccionado.value);
          const tareaIds = tareasCurso.map(t => t.id);
          // Luego traemos todas las entregas y filtramos solo las que correspondan a esas tareas
          const allEntregas = await getEntregasPorCurso(cursoSeleccionado.value);
          console.log('Entregas obtenidas:', allEntregas);
          entregas.value = allEntregas.filter(e => tareaIds.includes(e.tarea));
          console.log('Entregas filtradas:', entregas.value);
        } catch (e) {
          entregas.value = [];
        }
      } else if (tipoReporte.value === 'tareas' && cursoSeleccionado.value) {
        try {
          tareas.value = await getTareasPorCurso(cursoSeleccionado.value);
          // console.log('Tareas obtenidas:', tareas.value);
        } catch (e) {
          tareas.value = [];
        }
      }
    }


    async function generarReporte() {
      cargando.value = true;
      error.value = '';
      reporteUrl.value = '';
      reporteHtml.value = '';
      try {
        const res = await generarReporteDocente(cursoSeleccionado.value, tipoReporte.value);
        if (res.url) {
          reporteUrl.value = res.url;
        } else if (res.html) {
          reporteHtml.value = res.html;
        } else {
          error.value = 'No se pudo generar el reporte.';
        }
      } catch (e) {
        error.value = 'Error al generar el reporte.';
      } finally {
        cargando.value = false;
      }
    }

    return {
      cursos,
      cursoSeleccionado,
      tipoReporte,
      tareas,
      cargando,
      error,
      reporteUrl,
      reporteHtml,
      generarReporte,
      fetchTareas
    };
  }
};
</script>

<style scoped>
.reporte-container {
  max-width: 500px;
  margin: 40px auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.10);
  padding: 32px 28px 24px 28px;
}
.reporte-container h2 {
  text-align: center;
  margin-bottom: 28px;
  color: #002147;
  font-size: 1.7rem;
  font-weight: 600;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.reporte-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 10px;
}
.input-icon-group {
  position: relative;
  display: flex;
  align-items: center;
}
.input-icon-group i {
  position: absolute;
  left: 12px;
  color: #888;
  font-size: 1.1rem;
  z-index: 1;
}
.input-icon-group select {
  padding-left: 36px;
  width: 100%;
}
.btn-generar {
  width: 100%;
  padding: 15px;
  background: linear-gradient(90deg, #002147 60%, #005fa3 100%);
  color: #fff;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 18px;
  box-shadow: 0 2px 8px rgba(0,33,71,0.08);
  transition: background 0.2s, transform 0.2s;
}
.btn-generar:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}
.centrado-tareas {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}
.titulo-tareas {
  margin-bottom: 10px;
  color: #002147;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
  letter-spacing: 0.5px;
}
.centrado-tareas ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.tarea-card {
  background: #f7fafc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,33,71,0.04);
  padding: 12px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: box-shadow 0.2s;
}
.tarea-card i {
  color: #005fa3;
  font-size: 1.2rem;
}
.tarea-info {
  flex: 1;
  text-align: left;
}
.tarea-titulo {
  font-weight: 600;
  color: #222;
  font-size: 1rem;
}
.no-tareas {
  text-align: center;
  color: #888;
  margin: 12px 0 0 0;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}

select, button {
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #d1d5db;
  font-size: 1rem;
}
button {
  background: #002147;
  color: #fff;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
}
button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}
.error {
  margin-top: 18px;
  color: #c33;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
}
.reporte-descarga {
  margin-top: 24px;
  text-align: center;
}
.reporte-descarga a {
  color: #002147;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.reporte-descarga a:hover {
  text-decoration: underline;
}
.reporte-preview {
  margin-top: 24px;
  background: #f7fafc;
  border-radius: 8px;
  padding: 18px;
  font-size: 0.98rem;
  color: #222;
}
.centrado-tareas {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 10px;
}
.titulo-tareas {
  margin-bottom: 10px;
  color: #002147;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
}
.centrado-tareas ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}
.centrado-tareas li {
  text-align: center;
  margin-bottom: 6px;
}
</style>
