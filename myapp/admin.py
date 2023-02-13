from django.contrib import admin

from myapp.models import Author, Book, Publisher, Store


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')

    fieldsets = [
        (None, {'fields': ['name']}),
        ('Age', {'fields': ['age']}),
    ]
    list_per_page = 10
    search_fields = ['name']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_per_page = 10
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_authors', 'pubdate')
    list_per_page = 10
    search_fields = ['name']
    date_hierarchy = 'pubdate'

    # fields = (('name', 'rating', 'pages'), 'price', 'authors', ('publisher', 'pubdate'))

    fieldsets = [
        ('Name', {'fields': ['name', 'rating', 'pages']}),
        ('Price', {'fields': ['price']}),
        ('Authors', {'fields': ['authors']}),
        (None, {'fields': ['publisher', 'pubdate']}),
    ]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_books')
    list_per_page = 10
    search_fields = ['name']
