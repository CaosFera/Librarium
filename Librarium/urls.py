

from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('book/', include('book.urls')),
   # path('auth/', include('dj_rest_auth.urls')),  # Endpoints de login, logout, etc.
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),    
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

]
