from django.urls import path, include   
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)  # 'users' es la URL base

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas del router
]
