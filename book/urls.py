from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    AuthorViewSet,
    BookViewSet,
    CollectionViewSet,
    BookInCollectionViewSet
)

# Roteador principal
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'collections', CollectionViewSet)

# URLs para os métodos de adicionar e remover livros de coleções
urlpatterns = [
    path('', include(router.urls)),  # Rotas principais
    
    path(
        'collections/<int:collection_pk>/books/<int:book_pk>/',
        BookInCollectionViewSet.as_view({'post': 'create', 'delete': 'destroy', 'get': 'list'}),
        name='manage-book-in-collection'
    ),
]
