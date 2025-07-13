from django.contrib import admin

# Register your models here.

from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/registrar-asignatura/', views.registrar_asignatura),
]