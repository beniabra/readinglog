from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bookshelves/', views.books, name='books'),
    path('bookshelves/view/<int:id>', views.shelf, name='shelf'),
    path('statistics/', views.stats, name='stats'),
    path('view/<str:id>', views.view_book, name="view"),
    path('log/<str:id>', views.log, name="log")
]