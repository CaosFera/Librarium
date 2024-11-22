from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework import serializers
from .models import User



class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=30)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # Aqui estamos criando um campo extra para retornar o nome completo
    full_name = serializers.ReadOnlyField(source='get_full_name')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'full_name']
        read_only_fields = ['date_joined']  # 'date_joined' não deve ser modificado

    def create(self, validated_data):
        # Criação de usuário com a senha criptografada
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Atualizando a senha, se ela for fornecida
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        return super().update(instance, validated_data)

