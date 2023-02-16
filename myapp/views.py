from django.db.models import Avg, Max, Min, Sum, Count
from django.shortcuts import render
from django.views import generic

from myapp.models import Book, Author, Publisher, Store


def index(request):
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_publisher = Publisher.objects.all().count()
    num_store = Store.objects.count()
    aggr_books = Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))
    avg_p, max_p, min_p = round(aggr_books['price__avg'], 2), aggr_books['price__max'], aggr_books['price__min']

    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_authors': num_authors,
            'num_publishers': num_publisher,
            'num_store': num_store,
            'avg_p': avg_p,
            'max_p': max_p,
            'min_p': min_p,
        }

    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    queryset = Book.objects.prefetch_related('authors', 'store_set', 'publisher').all().order_by('name')


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    queryset = Author.objects.all().annotate(avg_rating=Avg('book__rating')).order_by('name')


class AuthorDetailView(generic.DetailView):
    model = Author


class PublisherListView(generic.ListView):
    model = Publisher
    paginate_by = 10
    queryset = Publisher.objects.all().annotate(num_book=Count('book')).order_by('name')


class PublisherDetailView(generic.DetailView):
    model = Publisher


class StoreListView(generic.ListView):
    model = Store
    paginate_by = 10
    queryset = Store.objects.all().annotate(
        num_book=Count('books'),
        avg_price=Avg('books__price'),
        min_price=Min('books__price'),
        max_price=Max('books__price'),
    ).order_by('name')


class StoreDetailView(generic.DetailView):
    model = Store
