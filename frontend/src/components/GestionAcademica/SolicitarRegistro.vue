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
        // Obtener todas las asignaturas
        const response = await fetch('http://localhost:8000/api/asignaturas');
        const data = await response.json();

        // Obtener solicitudes aceptadas del estudiante
        let solicitudesAceptadas = [];
        try {
          const token = localStorage.getItem('access_token');
          const respSol = await fetch('http://localhost:8000/api/solicitudAsignatura/', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (respSol.ok) {
            const solicitudes = await respSol.json();
            solicitudesAceptadas = solicitudes
              .filter(s => s.estado === 'aceptado')
              .map(s => s.asignatura_id || s.asignatura); // id o nombre según backend
          }
        } catch (e) {
          // Si falla, mostrar todas
        }

        // Filtrar asignaturas que no estén aceptadas
        this.asignaturas = data.filter(a => !solicitudesAceptadas.includes(a.id));
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

<style scoped lang="scss">
@import '@/assets/styles/variables';
@import '@/assets/styles/base';
.contenedor {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.titulo {
  color: $text-primary;
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  position: relative;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 3px;
    background: $color-primary;
  }
}

.asignaturas-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.tarjeta-asignatura {
  background: $bg-white;
  border: 1px solid $border-color;
  border-radius: $border-radius;
  padding: 1.5rem;
  box-shadow: $shadow-sm;
  transition: $transition-base;
  display: flex;
  flex-direction: column;
  height: 100%;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: $shadow-md;
    border-color: $color-primary-light;
  }
  
  h3 {
    color: $text-primary;
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-size: 1.25rem;
  }
  
  .nombre {
    font-weight: 600;
    color: $text-primary;
    margin: 0.5rem 0;
    font-size: 1.1rem;
  }
  
  .descripcion {
    color: $text-secondary;
    font-size: 0.95rem;
    line-height: 1.5;
    margin: 0.75rem 0;
    flex-grow: 1;
  }
  
  .docente {
    color: $text-secondary;
    font-size: 0.9rem;
    margin: 0.5rem 0 1rem;
    
    strong {
      color: $text-primary;
    }
  }
  
  button {
    @extend .btn;
    @extend .btn-primary;
    width: 100%;
    margin-top: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    
    &:hover {
      transform: translateY(-2px);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
}

.mensaje-vacio {
  text-align: center;
  color: $text-secondary;
  padding: 2rem;
  background: $bg-lighter;
  border-radius: $border-radius;
  margin: 2rem 0;
  font-style: italic;
}

/* Responsive */
@media (max-width: $breakpoint-md) {
  .contenedor {
    padding: 1.5rem;
  }
  
  .asignaturas-container {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.25rem;
  }
  
  .titulo {
    font-size: 1.5rem;
  }
}

@media (max-width: $breakpoint-sm) {
  .contenedor {
    padding: 1rem;
  }
  
  .asignaturas-container {
    grid-template-columns: 1fr;
  }
  
  .tarjeta-asignatura {
    padding: 1.25rem;
    
    h3 {
      font-size: 1.1rem;
    }
    
    .nombre {
      font-size: 1rem;
    }
    
    .descripcion, .docente {
      font-size: 0.9rem;
    }
  }
}
</style>
