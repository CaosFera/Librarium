from django.urls import path
from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.registration.views import RegisterView
from user.serializers import CustomRegisterSerializer

urlpatterns = [
    
        path('login/', LoginView.as_view(), name='rest_login'),
        path('logout/', LogoutView.as_view(), name='rest_logout'),  
        path('registration/', RegisterView.as_view(serializer_class=CustomRegisterSerializer), name='custom_register'),
      
]
