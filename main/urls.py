from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bookshelves/', views.books, name='books'),
    path('statistics/', views.stats, name='stats'),
    path('view/<str:id>', views.view_book, name="view")

]