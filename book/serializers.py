from rest_framework import serializers
from book.models import Category, Author, Book, Collection
from user.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):    
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    published_on = serializers.DateField(format='%d/%m/%Y')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'published_on']

    def create(self, validated_data):       
        author_instance = validated_data.pop('author')
        category_instance = validated_data.pop('category')
        book = Book.objects.create(author=author_instance, category=category_instance, **validated_data)
        return book

    def update(self, instance, validated_data):        
        author_instance = validated_data.pop('author', None)
        category_instance = validated_data.pop('category', None)
        
        if author_instance:
            instance.author = author_instance
        if category_instance:
            instance.category = category_instance
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance




class CollectionSerializer(serializers.ModelSerializer):
    collector_id = serializers.PrimaryKeyRelatedField(source='collector', read_only=True)
    collector_username = serializers.CharField(source='collector.username', read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'books', 'collector_id', 'collector_username']
        


class BookInCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_on']


class CollectionCreateUpdateSerializer(serializers.ModelSerializer):
    collector_id = serializers.PrimaryKeyRelatedField(source='collector', read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'collector_id']
