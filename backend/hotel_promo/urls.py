from django.contrib import admin
from django.urls import path, include
from users.views import CustomTokenObtainPairView  # Importa la vista personalizada para obtener el token
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import HttpResponse

# Vista simple para mostrar un mensaje de bienvenida en la raíz del proyecto
def home(request):
    return HttpResponse("Bienvenido al backend de la API")

# Definición de las URLs principales del proyecto
urlpatterns = [
    path('', home),  # Página de bienvenida en la raíz
    path("admin/", admin.site.urls),  # Ruta para el panel de administración de Django
    path('api/users/', include('users.urls')),  # Rutas para las operaciones de usuarios
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Ruta para obtener el token JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Ruta para refrescar el token JWT
]
