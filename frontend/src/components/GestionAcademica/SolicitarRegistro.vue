<template>
  <div class="contenedor">
    <h2 class="titulo">Asignaturas disponibles</h2>

    <div v-if="asignaturas.length" class="asignaturas-container">
      <div
        v-for="asignatura in asignaturas"
        :key="asignatura.id"
        class="tarjeta-asignatura"
      >
        <h3>{{ asignatura.titulo }}</h3>
        <p class="nombre">{{ asignatura.nombre }}</p>
        <p class="descripcion">{{ asignatura.descripcion }}</p>
        <p class="docente">
          <strong>Docente:</strong>
          {{ asignatura.docente_responsable_nombre }} {{ asignatura.docente_responsable_apellido }}
        </p>
        <button @click="solicitarAsignatura(asignatura.id)">Solicitar registro</button>
      </div>
    </div>

    <div v-else class="mensaje-vacio">
      <p>No hay asignaturas disponibles.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SolicitarRegistro',
  data() {
    return {
      asignaturas: []
    }
  },
  mounted() {
    this.obtenerAsignaturas()
  },
  methods: {
    async obtenerAsignaturas() {
      try {
        const response = await fetch('http://localhost:8000/api/asignaturas')
        const data = await response.json()
        this.asignaturas = data
      } catch (error) {
        console.error('Error al obtener asignaturas:', error)
      }
    },
    async solicitarAsignatura(asignatura_id) {
    try {
      const token = localStorage.getItem('access_token');  // Asegúrate de haber guardado el JWT aquí
      console.log('access_token:', token);
      const response = await fetch('http://localhost:8000/api/solicitudAsignatura/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ asignatura_id })
      });

      const data = await response.json();

      if (response.ok) {
        alert('✅ Solicitud enviada con éxito');
      } else {
        alert(`❌ Error: ${data.error || 'No se pudo enviar la solicitud'}`);
      }
    } catch (err) {
      console.error(err);
      alert('❌ Error al enviar la solicitud');
    }
  }
  }
}
</script>

<style scoped>
.contenedor {
  padding: 20px;
}

.titulo {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  color: #333;
}

.asignaturas-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.tarjeta-asignatura {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  padding: 20px;
  width: 280px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}

.tarjeta-asignatura:hover {
  transform: translateY(-5px);
}

.descripcion {
  font-size: 14px;
  color: #555;
  margin: 10px 0;
}

.docente {
  font-size: 14px;
  margin-bottom: 10px;
}

button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #2980b9;
}

.mensaje-vacio {
  text-align: center;
  color: #888;
}
</style>
