from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Avg, Max, Min, Sum, Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from myapp.models import Book, Author, Publisher, Store


# @cache_page(10)
def index(request):
    num_books = Book.objects.count()
    num_authors = Author.objects.count()
    num_publisher = Publisher.objects.count()
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


@method_decorator(cache_page(10), name='get')
class BookListView(generic.ListView):
    model = Book
    paginate_by = 500
    queryset = Book.objects.prefetch_related('authors', 'store_set').select_related('publisher').order_by('name')


class BookDetailView(generic.DetailView):
    model = Book
    queryset = Book.objects.prefetch_related('authors').order_by('name')


@method_decorator(cache_page(10), name='get')
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 500
    queryset = Author.objects.annotate(
        avg_rating=Avg('book__rating')
    ).prefetch_related('book_set').order_by('name')


class AuthorDetailView(generic.DetailView):
    model = Author
    queryset = Author.objects.annotate(
        num_books=Count('book'),
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price'),
        avg_rating=Avg('book__rating')
        ).prefetch_related('book_set')


@method_decorator(cache_page(10), name='get')
class PublisherListView(generic.ListView):
    model = Publisher
    paginate_by = 500
    queryset = Publisher.objects.annotate(
        num_book=Count('book')
    ).prefetch_related('book_set').order_by('name')


class PublisherDetailView(generic.DetailView):
    model = Publisher
    queryset = Publisher.objects.annotate(
        num_books=Count('book'),
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price'),

    ).prefetch_related('book_set')


@method_decorator(cache_page(10), name='get')
class StoreListView(generic.ListView):
    model = Store
    paginate_by = 500
    queryset = Store.objects.annotate(
        num_book=Count('books'),
        avg_price=Avg('books__price'),
        min_price=Min('books__price'),
        max_price=Max('books__price'),
    ).prefetch_related('books').order_by('name')


class StoreDetailView(generic.DetailView):
    model = Store
    queryset = Store.objects.annotate(
        num_books=Count('books'),
        avg_price=Avg('books__price'),
        min_price=Min('books__price'),
        max_price=Max('books__price'),
    ).prefetch_related('books')


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['name', 'pages', 'price', 'rating', 'authors', "publisher", 'pubdate']
    permission_required = 'myapp.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['name', 'pages', 'price', 'rating', 'authors', "publisher", 'pubdate']
    permission_required = 'myapp.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'myapp.can_mark_returned'
