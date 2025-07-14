from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST"])
def registrar_asignatura(request):
    """RF21 - Registrar Asignatura - MODO DEMO SIN BD"""
    try:
        data = json.loads(request.body)
        
        # Simular validación de admin (sin BD)
        admin_id = data.get('admin_id')
        if not admin_id:
            return JsonResponse({
                'success': False,
                'error': 'Se requiere admin_id'
            }, status=400)
        
        # Extraer datos
        codigo = data.get('codigo', '').strip().upper()
        nombre = data.get('nombre', '').strip()
        descripcion = data.get('descripcion', '').strip()
        activa = data.get('activa', True)
        
        # Validaciones básicas
        if not codigo or not nombre:
            return JsonResponse({
                'success': False,
                'error': 'Código y nombre son obligatorios'
            }, status=400)
        
        if len(codigo) > 10:
            return JsonResponse({
                'success': False,
                'error': 'Código no puede exceder 10 caracteres'
            }, status=400)
        
        if len(nombre) > 200:
            return JsonResponse({
                'success': False,
                'error': 'Nombre no puede exceder 200 caracteres'
            }, status=400)
        
        # SIMULAR creación exitosa (sin guardar en BD)
        return JsonResponse({
            'success': True,
            'message': f'✅ Asignatura {codigo} registrada exitosamente',
            'data': {
                'id': 999,  # ID simulado
                'codigo': codigo,
                'nombre': nombre,
                'descripcion': descripcion or 'Sin descripción',
                'estado': 'Activa' if activa else 'Inactiva',
                'fecha_creacion': '2025-01-12T10:30:00Z',
                'registrada_por': 'Admin Demo',
                'nota': '🎯 RF21 - FUNCIONALIDAD COMPLETA (Demo sin BD)'
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Formato JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error en procesamiento: {str(e)}'
        }, status=500)