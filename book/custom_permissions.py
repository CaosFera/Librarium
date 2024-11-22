from rest_framework.permissions import BasePermission

class IsCollectorOrReadOnly(BasePermission):
    """
    Permissão para que apenas o colecionador possa modificar suas coleções.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.collector == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Permissão para permitir que apenas administradores façam modificações.
    Usuários não administradores terão acesso apenas aos métodos GET, HEAD e OPTIONS.
    """
    def has_permission(self, request, view):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            return False
        
        # Se o usuário for admin, permite todas as ações
        if request.user.is_staff:
            return True
        
        # Se não for admin, permite apenas os métodos GET, HEAD e OPTIONS
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Caso contrário, nega o acesso
        return False

