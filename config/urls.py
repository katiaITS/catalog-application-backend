from django.contrib import admin
from django.urls import path, include
#funzioni per servire file statici/media
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,      # Login (ottieni token)
    TokenRefreshView,         # Refresh (nuovo access token)
    TokenVerifyView,          # Verifica token valido
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('catalogo.urls')), #Includi le rotte API definite in catalogo/urls.py   
    
    # JWT Authentication endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]