from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.pk)])


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('publisher-detail', args=[str(self.pk)])


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.pk)])

    def display_authors(self):
        return ', '.join([authors.name for authors in self.authors.all()[:3]])

    display_authors.short_description = 'Authors'


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store-detail', args=[str(self.pk)])

    def display_books(self):
        return ', '.join([books.name for books in self.books.all()[:3]])

    display_books.short_description = 'Books'
