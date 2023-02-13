from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('book/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('publisher/', views.PublisherListView.as_view(), name='publishers'),
    path('publisher/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher-detail'),
    path('store/', views.StoreListView.as_view(), name='stores'),
    path('store/<int:pk>/', views.StoreDetailView.as_view(), name='store-detail'),

]
