from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied, NotFound
from django.shortcuts import get_object_or_404
from .models import Book, Author, Category, Collection
from .serializers import (
    CategorySerializer, AuthorSerializer, BookSerializer, 
    CollectionSerializer, BookInCollectionSerializer, CollectionCreateUpdateSerializer
)
from book.custom_permissions import IsCollectorOrReadOnly, IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated




class CategoryViewSet(viewsets.ModelViewSet):
    """
    Usuários não administradores terão acesso apenas aos métodos GET, HEAD e OPTIONS.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]



class AuthorViewSet(viewsets.ModelViewSet):
    """
    Usuários não administradores terão acesso apenas aos métodos GET, HEAD e OPTIONS.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    """
    Usuários não administradores terão acesso apenas aos métodos GET, HEAD e OPTIONS.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]  
    def create(self, request, *args, **kwargs):       
        author_id = request.data.get('author')
        category_id = request.data.get('category')
        title = request.data.get('title')
        published_on = request.data.get('published_on')        
        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return Response({"detail": "Autor não encontrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {"detail": "Categoria não encontrada."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Criar o livro com author e category como instâncias
        book = Book.objects.create(
            title=title,
            author=author,
            category=category,
            published_on=published_on
        )

        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Views para Coleções
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()    
    permission_classes = [IsAuthenticated, IsCollectorOrReadOnly]
    def get_serializer_class(self):
        """
        Seleciona o serializer apropriado com base no tipo de operação.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return CollectionCreateUpdateSerializer
        return CollectionSerializer

    

    def get_queryset(self):        
        return Collection.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(collector=self.request.user)


# Views para Gerenciamento de Livros em Coleções
class BookInCollectionViewSet(viewsets.ViewSet): 
    serializer_class = BookInCollectionSerializer   
    permission_classes = [IsAuthenticated, IsCollectorOrReadOnly]

    def get_collection(self, collection_pk):        
        collection = get_object_or_404(Collection, pk=collection_pk)
        self.check_object_permissions(self.request, collection)
        return collection

    def list(self, request, collection_pk=None, book_pk=None):        
        collection = self.get_collection(collection_pk)
        try:
            book = collection.books.get(id=book_pk)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Livro não encontrado na coleção."},
                status=status.HTTP_404_NOT_FOUND
            )


        serializer = BookInCollectionSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, collection_pk=None, book_pk=None):        
        collection = self.get_collection(collection_pk)        
        if not book_pk:
            return Response(
                {"detail": "O ID do livro é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

       
        try:
            book = Book.objects.get(id=book_pk)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Livro não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        
        if book in collection.books.all():
            return Response(
                {"detail": "Este livro já está na coleção."},
                status=status.HTTP_400_BAD_REQUEST
            )

       
        collection.books.add(book)
        return Response(
            {"detail": f"O livro '{book.title}' foi adicionado à coleção com sucesso."},
            status=status.HTTP_201_CREATED
        )


    def destroy(self, request, collection_pk=None, book_pk=None):
        """
        Remove um livro de uma coleção.
        Apenas o colecionador pode realizar essa ação.
        """
        collection = self.get_collection(collection_pk)
        try:
            book = Book.objects.get(id=book_pk)  # Usando o book_pk passado na URL
        except Book.DoesNotExist:
            return Response(
                {"detail": "Livro não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        if book not in collection.books.all():
            return Response(
                {"detail": "Este livro não está na coleção."},
                status=status.HTTP_400_BAD_REQUEST
            )

        collection.books.remove(book)
        return Response(
            {"detail": "Livro removido da coleção com sucesso."},
            status=status.HTTP_204_NO_CONTENT
        )

