from django.shortcuts import render, redirect
from django.middleware.csrf import get_token
from django.http import HttpResponse
from .models import Bookshelf, Book
from datetime import date
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
        if response.GET.get("search"):
            url = "https://www.googleapis.com/books/v1/volumes?q=" + response.GET.get("search").replace(" ", "+")
            search_results = requests.get(url).json()

    return render(response, "main/search.html", {"terms":response.GET.get("search"), "results":search_results["items"], "bookshelves": Bookshelf.objects.all()})

def addToBookshelf(request, id, shelfId):
    if not Book.objects.filter(id=id).exists():
        Book.objects.create(id=id)
    b = Book.objects.get(id=id)
    s = Bookshelf.objects.get(id=shelfId)
    if s.name == "Currently Reading":
        pass
        """
        csrf_token = get_token(request)
        r = requests.post('http://127.0.0.1:8000/start/'+id, data={'csrfmiddlewaretoken': csrf_token, 'start': True})
        #csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" />'.format(csrf_token)
        print(csrf_token)"""
    elif s.name == "To Read":
        pass
    elif s.name == "Finished":
        pass
    elif s.name == "Did Not Finish":
        pass
    else:
        pass

    return redirect(view_book, id=id)

def log(response,id):
    print(response.POST)
    if response.method == "POST":
        b = Book.objects.get(id=id)
        if response.POST.get("save"):
            if int(response.POST.get('progress')) >= 100:
                return redirect(finish, id=id)
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
                return redirect(finish, id=id)
            b.save()
    return redirect(home)

def start(response, id):
    if response.method == "POST":
        if(response.POST.get("start")):
            Book.objects.create(id=id, started = True, finished = False, dnfed = False, start_date = date.today())
            b = Book.objects.get(id=id)
            b.save()
            s = Bookshelf.objects.get(name="Currently Reading")
            s.book_set.add(b)
            s.save()
    return redirect(view_book, id=id)

def finish(response, id):
    if response.method == "POST":
        b = Book.objects.get(id=id)
        if(response.POST.get("finish")):
            b.progress = 100
            b.started = True
            b.finished = True
            b.dnfed = False
            b.finish_date = date.today()
            b.save()
            s2 = Bookshelf.objects.get(name="Finished")
            s2.book_set.add(b)
            if Bookshelf.objects.get(name="Currently Reading").book_set.filter(id=id).exists():
                s1 = Bookshelf.objects.get(name="Currently Reading")
                s1.book_set.remove(b)
                s1.save()
            s2.save()
    return redirect(view_book, id=id)

def dnf(response, id):
    if response.method == "POST":
        b = Book.objects.get(id=id)
        if(response.POST.get("dnf")):
            b.started = True
            b.finished = False
            b.dnfed = True
            b.finish_date = date.today()
            b.save()
            s2 = Bookshelf.objects.get(name="Did Not Finish")
            s2.book_set.add(b)
            if Bookshelf.objects.get(name="Currently Reading").book_set.filter(id=id).exists():
                s1 = Bookshelf.objects.get(name="Currently Reading")
                s1.book_set.remove(b)
            s1.save()
            s2.save()
    return redirect(home)

def view_book(response, id):
    added = False
    try:
        book = Book.objects.get(id=id)
        added = True
    except Book.DoesNotExist:
        book = None
        added = False
    return render(response, "main/view.html", {"added": added, "book_id": id, "book": book})

def books(response):
    shelves = Bookshelf.objects.all()
    return render(response, "main/books.html", {"shelves": shelves})

def shelf(response, id):
    b = Bookshelf.objects.get(id=id)
    return render(response, "main/shelf.html", {"shelf": b})

def stats(response):
    return render(response, "main/stats.html", {})
