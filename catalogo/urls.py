from django.urls import path, include
from rest_framework.routers import DefaultRouter #DefaultRouter genera automaticamente anche la root view (/)
from .views import CatalogoViewSet, CategoriaViewSet, CartelleViewSet

#Crea istanza del router
router =DefaultRouter()

# Registra ViewSet - sintassi router.register(prefix, viewset, basename)
# Il prefix è la parte di URL dopo /api/ (es. /api/cataloghi/)
# Il viewset dice quale Viewset usare
# Il basename è usato per nominare le route generate (es. 'cataloghi-list', 'cataloghi-detail')
router.register(r'cataloghi', CatalogoViewSet, basename='cataloghi')
router.register(r'categorie', CategoriaViewSet, basename='categorie')
router.register(r'cartelle', CartelleViewSet, basename='cartelle')

#Include tutte le rotte generate dal router sotto il path di base /api/
urlpatterns = [
    path('', include(router.urls)),
]