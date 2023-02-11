from django.shortcuts import render, redirect
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

def search(response):
    if response.method == "GET":
        print(response.GET)
        if response.GET.get("search"):
            url = "https://www.googleapis.com/books/v1/volumes?q=" + response.GET.get("search").replace(" ", "+")
            search_results = requests.get(url).json()
            for result in search_results["items"]:
                print(result["volumeInfo"]["title"])

    return render(response, "main/search.html", {"terms":response.GET.get("search"), "results":search_results["items"]})


def log(response,id):
    if response.method == "POST":
        print(response.POST)
        b = Book.objects.get(id=id)
        if response.POST.get("save"):
            if int(response.POST.get('progress')) >= 100:
                b.progress = 100
            else:
                b.progress = response.POST.get('progress')

            b.save()
            if response.POST.get('status') == 'To Read':
                b.started = False
                b.finished = False
                b.dnfed = False
            elif response.POST.get('status') == 'Started':
                b.started = True
                b.finished = False
                b.dnfed = False
            elif response.POST.get('status') == 'Finished':
                b.started = True
                b.finished = True
                b.dnfed = False
        
    return redirect(home)

def view_book(response, id):
    added = False
    try:
        book = Book.objects.get(id=id)
        added = True
    except Book.DoesNotExist:
        book = None
        added = False
    """
    if(Book.objects.get(id=id)):
        book = Book.objects.get(id=id)
        added = True
    """
    return render(response, "main/view.html", {"added": added, "book_id": id, "book": book})

def books(response):
    shelves = Bookshelf.objects.all()
    return render(response, "main/books.html", {"shelves": shelves})

def shelf(response, id):
    b = Bookshelf.objects.get(id=id)
    return render(response, "main/shelf.html", {"shelf": b})

def stats(response):
    return render(response, "main/stats.html", {})
