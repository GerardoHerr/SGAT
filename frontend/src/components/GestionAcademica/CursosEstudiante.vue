<template>
  <div>
    <h2 style="margin-bottom: 20px;">Cursos disponibles del estudiante</h2>

    <!-- Botón principal -->
    <button class="btn-principal" @click="mostrarFormulario = true">
      ➕ Agregar nueva asignatura
    </button>

    <!-- Modal -->
    <div v-if="mostrarFormulario" class="modal-overlay">
      <div class="modal-contenido animate-entrada">
        <h3>📚 Asignaturas disponibles</h3>

        <!-- Lista de asignaturas -->
        <div v-if="asignaturas.length">
          <div v-for="asignatura in asignaturas" :key="asignatura.id" class="asignatura-item">
            <div>
              <strong>{{ asignatura.nombre }}</strong>
              <p style="margin: 5px 0;">{{ asignatura.descripcion || 'Sin descripción' }}</p>
            </div>
            <button @click="enviarSolicitud(asignatura.id)" class="btn-enviar">✅ Solicitar</button>
          </div>
        </div>
        <div v-else>
          <p>No hay asignaturas disponibles.</p>
        </div>

        <!-- Cancelar -->
        <div class="botones">
          <button type="button" @click="cerrarModal" class="btn-cancelar">❌ Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      mostrarFormulario: false,
      asignaturas: []
    };
  },
  methods: {
    async cargarAsignaturas() {
      try {
        const response = await axios.get('http://localhost:8000/api/asignaturas/');
        this.asignaturas = response.data;
      } catch (error) {
        console.error('Error al cargar asignaturas:', error);
      }
    },
    async enviarSolicitud(asignaturaId) {
      try {
        console.log('Enviando solicitud para asignatura ID:', asignaturaId);
        // Aquí puedes hacer la solicitud POST
        // await axios.post('/api/solicitudes/', { asignatura: asignaturaId });

        alert(`Solicitud enviada para asignatura ID: ${asignaturaId}`);
        this.cerrarModal();
      } catch (error) {
        console.error('Error al enviar solicitud:', error);
        alert('Hubo un error al enviar la solicitud');
      }
    },
    cerrarModal() {
      this.mostrarFormulario = false;
    }
  },
  watch: {
    mostrarFormulario(val) {
      if (val) {
        this.cargarAsignaturas();
      }
    }
  }
};
</script>

<style scoped>
/* Tipografía general */
* {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Botón principal */
.btn-principal {
  background-color: #3a86ff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}
.btn-principal:hover {
  background-color: #265ecf;
}

/* Fondo del modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

/* Contenedor del modal */
.modal-contenido {
  background-color: #fff;
  padding: 25px 30px;
  border-radius: 15px;
  width: 420px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

/* Animación de entrada */
.animate-entrada {
  animation: fadeInScale 0.3s ease-in-out;
}

@keyframes fadeInScale {
  0% {
    opacity: 0;
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Campos del formulario */
label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
}
select {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-bottom: 20px;
}

/* Botones dentro del modal */
.botones {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.btn-enviar {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-enviar:hover {
  background-color: #218838;
}
.btn-cancelar {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.btn-cancelar:hover {
  background-color: #c82333;
}
.asignatura-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.asignatura-item:last-child {
  border-bottom: none;
}
</style>
