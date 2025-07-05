from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sgta.api.views import TareaViewSet

router = DefaultRouter()
router.register(r'tareas', TareaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]