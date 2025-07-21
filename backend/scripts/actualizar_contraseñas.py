import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from sgta.models import Usuario
from django.contrib.auth.hashers import make_password

def actualizar_contraseñas():
    """Actualizar contraseñas de usuarios existentes"""
    
    print("=== ACTUALIZANDO CONTRASEÑAS DE USUARIOS ===")
    print()
    
    # Contraseñas por defecto según rol
    contraseñas_default = {
        'ADM': 'admin123',
        'DOC': 'docente123', 
        'EST': 'estudiante123'
    }
    
    usuarios = Usuario.objects.all()
    
    for usuario in usuarios:
        # Solo actualizar si la contraseña es la temporal
        if usuario.contrasenia == 'temp123':
            nueva_contraseña = contraseñas_default.get(usuario.rol, 'password123')
            usuario.contrasenia = make_password(nueva_contraseña)
            usuario.save()
            
            print(f"✅ {usuario.nombre} {usuario.apellido} ({usuario.email})")
            print(f"   Rol: {usuario.get_rol_display()}")
            print(f"   Nueva contraseña: {nueva_contraseña}")
            print()
    
    print("=== CONTRASEÑAS ACTUALIZADAS ===")
    print()
    print("CREDENCIALES DE ACCESO:")
    print("- Administradores: contraseña 'admin123'")
    print("- Docentes: contraseña 'docente123'")
    print("- Estudiantes: contraseña 'estudiante123'")

if __name__ == "__main__":
    actualizar_contraseñas()
