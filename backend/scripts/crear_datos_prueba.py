import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from sgta.models import Usuario, Asignatura, PeriodoLectivo

def crear_datos_prueba():
    """Crear datos de prueba para el sistema"""
    
    # Crear usuarios de prueba
    usuarios = [
        {
            'email': 'admin@universidad.edu',
            'nombre': 'Admin',
            'apellido': 'Sistema',
            'rol': 'ADM'
        },
        {
            'email': 'maria.garcia@universidad.edu',
            'nombre': 'María',
            'apellido': 'García',
            'rol': 'DOC'
        },
        {
            'email': 'juan.rodriguez@universidad.edu',
            'nombre': 'Juan',
            'apellido': 'Rodríguez',
            'rol': 'DOC'
        },
        {
            'email': 'ana.lopez@universidad.edu',
            'nombre': 'Ana',
            'apellido': 'López',
            'rol': 'EST'
        },
        {
            'email': 'carlos.martinez@universidad.edu',
            'nombre': 'Carlos',
            'apellido': 'Martínez',
            'rol': 'EST'
        },
        {
            'email': 'lucia.fernandez@universidad.edu',
            'nombre': 'Lucía',
            'apellido': 'Fernández',
            'rol': 'EST'
        }
    ]
    
    for usuario_data in usuarios:
        usuario, created = Usuario.objects.get_or_create(
            email=usuario_data['email'],
            defaults=usuario_data
        )
        if created:
            print(f"Usuario creado: {usuario.nombre} {usuario.apellido} ({usuario.email})")
        else:
            print(f"Usuario ya existe: {usuario.nombre} {usuario.apellido} ({usuario.email})")
    
    # Crear período lectivo de prueba
    periodo, created = PeriodoLectivo.objects.get_or_create(
        nombre='2025-1',
        defaults={
            'fecha_inicio': '2025-01-15',
            'fecha_fin': '2025-06-15',
            'activo': True
        }
    )
    if created:
        print(f"Período lectivo creado: {periodo.nombre}")
    else:
        print(f"Período lectivo ya existe: {periodo.nombre}")
    
    print("Datos de prueba creados exitosamente.")

if __name__ == "__main__":
    crear_datos_prueba()
