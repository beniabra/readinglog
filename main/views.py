from django.shortcuts import render
from django.http import HttpResponse
from .models import Bookshelf, Book
import requests

def home(response):
    f = Bookshelf.objects.get(id=1).book_set.all().count()
    results = {
        "books_finished": f,
        "book_goal": 35,
        "percent": round(f/35*100),
        "bookshelf": Bookshelf.objects.get(id=2),
    }
    return render(response, "main/home.html", results)

def view_book(response, id):
    return render(response, "main/view.html", {"id": id})

def books(response):
    shelves = Bookshelf.objects.all()
    return render(response, "main/books.html", {"shelves": shelves})

def shelf(response, id):
    b = Bookshelf.objects.get(id=id)
    return render(response, "main/shelf.html", {"shelf": b})

def stats(response):
    return render(response, "main/stats.html", {})
