from django.shortcuts import render
from django.views import generic

from myapp.models import Book, Author, Publisher, Store


def index(request):
    num_books = Book.objects.all().count()
    num_authors = Author.objects.count()
    num_publisher = Publisher.objects.all().count()
    num_store = Store.objects.count()

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_authors': num_authors,
            'num_publishers': num_publisher,
            'num_store': num_store},
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class PublisherListView(generic.ListView):
    model = Publisher
    paginate_by = 10


class PublisherDetailView(generic.DetailView):
    model = Publisher


class StoreListView(generic.ListView):
    model = Store
    paginate_by = 10


class StoreDetailView(generic.DetailView):
    model = Store
