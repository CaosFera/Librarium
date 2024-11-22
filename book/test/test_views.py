from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from book.models import User
from book.models import Category, Collection, Book, Author



class CategoryViewSetTests(APITestCase):    
    def post_category(self, name):
        url = reverse("category-list")
        data = {"name": name}
        response = self.client.post(url, data, format="json")
        return response
    
    def put_category(self, category_id, name):
        url = reverse("category-detail", args=[category_id])
        data = {"name": name}
        response = self.client.put(url, data, format="json")
        return response
    
    def delete_category(self, category_id):
        url = reverse("category-detail", args=[category_id])
        response = self.client.delete(url)
        return response
    
    def get_category(self, category_id):
        url = reverse("category-detail", args=[category_id])
        response = self.client.get(url)
        return response
    
    # Testa o método POST para não administradores
    def test_post_category_for_non_admin_user(self):
        # Criar um usuário não administrador
        user = User.objects.create_user(username="user", password="password", email="user@example.com")

        # Criar um token para o usuário
        token = Token.objects.create(user=user)

        # Autenticar o usuário via token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        # Criar uma nova categoria
        new_category_name = "Fiction"
        response = self.post_category(new_category_name)

        # Verificar o status da resposta
        print(response.status_code)  # Deve ser 403
        print(response.data)  # Mostrar os detalhes da resposta, caso haja algum erro

        # Verificar que a criação não é permitida (não é administrador)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(0, Category.objects.count())  # A categoria não deve ser criada


    # Testa o método PUT para não administradores
    def test_put_category_for_non_admin_user(self):
        # Criar um usuário não administrador
        user = User.objects.create_user(username="user", password="password", email="user@example.com")
        token = Token.objects.create(user=user)  # Criando o token para o usuário
        
        # Criar uma categoria
        category = Category.objects.create(name="Fiction")
        
        # Autenticar o usuário via token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        # Tentar atualizar a categoria
        response = self.put_category(category.id, "Non-Fiction")
        
        # Verificar que a atualização não é permitida (não é administrador)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        category.refresh_from_db()  # Atualiza a instância do objeto para verificar se não foi alterado
        self.assertEqual(category.name, "Fiction")  # A categoria não deve ter sido atualizada

        # Testa o método DELETE para não administradores
    def test_delete_category_for_non_admin_user(self):
        # Criar um usuário não administrador
        user = User.objects.create_user(username="user", password="password", email="user@example.com")
        token = Token.objects.create(user=user)  # Criando o token para o usuário
        
        # Criar uma categoria
        category = Category.objects.create(name="Fiction")
        
        # Autenticar o usuário via token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        # Tentar excluir a categoria
        response = self.delete_category(category.id)
        
        # Verificar que a exclusão não é permitida (não é administrador)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(Category.objects.count(), 1)  # A categoria não deve ser excluída
    
    # Testa o método GET para não administradores
    def test_get_category_for_non_admin_user(self):
        user = User.objects.create_user(username="user", password="password", email="user@example.com")
        token = Token.objects.create(user=user)         
        category = Category.objects.create(name="Fiction")
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.get_category(category.id)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data["name"], category.name)  

    

class CollectionViewSetTestCase(APITestCase):
    def setUp(self):
        # Cria usuários
        self.user = User.objects.create_user(
            email="user@test.com", username="user1", password="password123"
        )
        self.other_user = User.objects.create_user(
            email="other@test.com", username="user2", password="password456"
        )

        # Gera tokens para os usuários
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)

        # Configura o cliente com autenticação via token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Cria coleções para os usuários
        self.collection_user1 = Collection.objects.create(name="Coleção User 1", collector=self.user)
        self.collection_user2 = Collection.objects.create(name="Coleção User 2", collector=self.other_user)

    def test_list_collections(self):   
        response = self.client.get(reverse("collection-list"))       
        self.assertEqual(response.status_code, status.HTTP_200_OK)       
        collections_in_db = Collection.objects.count()
        self.assertEqual(len(response.data), collections_in_db)
        collection_names = [collection["name"] for collection in response.data]
        self.assertIn(self.collection_user1.name, collection_names)
        self.assertIn(self.collection_user2.name, collection_names)


    def test_create_collection(self):
        data = {"name": "Nova Coleção", "description": "Descrição da coleção"}
        response = self.client.post(reverse("collection-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Nova Coleção")
        self.assertEqual(response.data["collector_id"], self.user.id)
       

class BookInCollectionViewSetTestCase(APITestCase):
    def setUp(self):
        # Criar usuários
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", email="otheruser@example.com", password="password123"
        )

        # Criar categorias e autores
        self.category = Category.objects.create(name="Ficção Científica")
        self.author = Author.objects.create(name="Isaac Asimov")        
        self.book1 = Book.objects.create(
            title="Eu, Robô",
            author=self.author,
            category=self.category,
            published_on="1950-12-02",
        )
        self.book2 = Book.objects.create(
            title="Fundação",
            author=self.author,
            category=self.category,
            published_on="1951-05-15",
        )

        # Criar coleções para os usuários
        self.collection_user1 = Collection.objects.create(
            name="Coleção User 1", collector=self.user
        )
        self.collection_user2 = Collection.objects.create(
            name="Coleção User 2", collector=self.other_user
        )

        self.add_book_url = reverse(
            'manage-book-in-collection', kwargs={'collection_pk': self.collection_user1.pk, 'book_pk': self.book1.pk}
        )
        self.add_book_url_other_user = reverse(
            'manage-book-in-collection', kwargs={'collection_pk': self.collection_user1.pk, 'book_pk': self.book2.pk}
        )

        self.remove_book_url = reverse(
            'manage-book-in-collection', kwargs={'collection_pk': self.collection_user1.pk, 'book_pk': self.book1.pk}
        )

      
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)

       
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_add_book_to_collection(self):        
        response = self.client.post(self.add_book_url)       
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_book_to_other_user_collection(self):       
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_token.key}")       
        response = self.client.post(self.add_book_url_other_user)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_book_from_collection(self):       
        response = self.client.post(self.add_book_url)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)       
        collection = self.collection_user1.books.all()  
        self.assertIn(self.book1, collection)        
        response = self.client.delete(self.remove_book_url)       
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)       
        collection = self.collection_user1.books.all()  
        self.assertNotIn(self.book1, collection)  

    def test_remove_book_to_other_user_collection(self):  
        response = self.client.post(self.add_book_url)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)       
        collection = self.collection_user1.books.all()  
        self.assertIn(self.book1, collection)  
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_token.key}")     
        response = self.client.delete(self.remove_book_url)       
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)       
        collection = self.collection_user1.books.all()  
        self.assertIn(self.book1, collection)  

    def test_remove_book_not_in_collection(self):        
        response = self.client.post(self.add_book_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)         
        collection = self.collection_user1.books.all()
        self.assertIn(self.book1, collection)       
        response = self.client.delete(self.remove_book_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)       
        collection = self.collection_user1.books.all()
        self.assertNotIn(self.book1, collection)       
        response = self.client.delete(self.remove_book_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Este livro não está na coleção.')

        
    def test_remove_non_existent_book(self):      
        non_existent_book_pk = 999  
        remove_non_existent_book_url = reverse(
            'manage-book-in-collection', kwargs={'collection_pk': self.collection_user1.pk, 'book_pk': non_existent_book_pk}
        )
        response = self.client.delete(remove_non_existent_book_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Livro não encontrado.', response.content.decode('utf-8'))

            
    