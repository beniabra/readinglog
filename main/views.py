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

def books(response):
    return render(response, "main/books.html", {})

def stats(response):
    return render(response, "main/stats.html", {})
