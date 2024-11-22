from django.db import models
from user.models import User


class Category(models.Model):
    name = models.CharField("Nome", max_length=100, blank=False)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"] 

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField("Nome", max_length=100, blank=False)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["name"]  

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("Título", max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    published_on = models.DateField("Data de publicação")

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]  

    def __str__(self):
        return self.title


class Collection(models.Model):
    name = models.CharField("Nome", max_length=100, unique=True)
    description = models.TextField("Descrição", blank=True, default="")
    books = models.ManyToManyField(Book, related_name="collections", blank=True)
    collector = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ["name"] 

    def __str__(self):
        return f"{self.name} - {self.collector.username}"
