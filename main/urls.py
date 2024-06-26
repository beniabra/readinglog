from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bookshelves/', views.books, name='books'),
    path('bookshelves/view/<int:id>/<int:page>/<str:sort>', views.shelf, name='shelf'),
    path('statistics/', views.stats, name='stats'),
    path('view/<str:id>', views.view_book, name="view"),
    path('log/<str:id>', views.log, name="log"),
    path('search/', views.search, name="search"),
    path('finish/<str:id>', views.finish, name="finish"),
    path('dnf/<str:id>', views.dnf, name="dnf"),
    path('start/<str:id>', views.start, name="start"),
    path('addToBookshelf/<str:id>', views.addToBookshelf, name="addToBookshelf"),
    path('changeBookshelf/<str:id>', views.changeBookshelf, name="changeBookshelf"),
    path('editDetails/<str:id>', views.editDetails, name="editDetails"),
    path('editLikesDislikes/<str:id>', views.editLikesDislikes, name="editLikesDislikes"),
    path('removeBook/<int:shelf_id>/<str:book_id>', views.removeBook, name="removeBook"),
    path('editRating/<str:id>', views.editRating, name="editRating"),
    path('newBookshelf', views.newBookshelf, name="newBookshelf"),
    path('editNotes/<str:id>', views.editNotes, name="editNotes"),
]