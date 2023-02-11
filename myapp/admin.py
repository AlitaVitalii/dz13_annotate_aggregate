from django.contrib import admin

from myapp.models import Author, Publisher, Book, Store


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')

    fieldsets = [
        (None, {'fields': ['name']}),
        ('Query', {'fields': ['age']}),
    ]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', )


# admin.site.register(Store)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_authors', 'pubdate')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_books')
