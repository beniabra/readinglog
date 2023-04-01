from django.shortcuts import render, redirect
from .models import Bookshelf, Book
from .forms import EditDetails
from datetime import date
import requests


def home(response):
    f = Bookshelf.objects.get(name="Finished").book_set.all().count()
    results = {
        "books_finished": f,
        "book_goal": 35,
        "percent": round(f/35*100),
        "bookshelf": Bookshelf.objects.get(name="Currently Reading"),
    }
    return render(response, "main/home.html", results)

def search(response):
    if response.method == "GET":
        if response.GET.get("search"):
            url = "https://www.googleapis.com/books/v1/volumes?q=" + response.GET.get("search").replace(" ", "+")
            search_results = requests.get(url).json()

    return render(response, "main/search.html", {"terms":response.GET.get("search"), "results":search_results["items"], "bookshelves": Bookshelf.objects.all()})

def log(response,id):
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

def view_book(response, id):
    added = False
    try:
        book = Book.objects.get(id=id)
        added = True
    except Book.DoesNotExist:
        book = None
        added = False
    return render(response, "main/view.html", {"added": added, "book_id": id, "book": book})

def editDetails(response, id):
    book = Book.objects.get(id=id)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("startDate"):
            book.start_date = response.POST.get("startDate")
        if response.POST.get("finishDate"):
            book.finish_date = response.POST.get("finishDate")
        if response.POST.get("progress"):
            print(book.progress)
            book.progress = response.POST.get("progress")
            print(book.progress)
        book.save()
    return redirect(view_book,id=id)

def addToBookshelf(response, id):
    if response.method == "POST":
        print(response.POST)
        if not Book.objects.filter(id=id).exists():
            Book.objects.create(id=id)
        b = Book.objects.get(id=id)
        print(int(response.POST.get("bookshelf")))
        s = Bookshelf.objects.get(id=int(response.POST.get("bookshelf")))
        if s.name == "Currently Reading":
            return redirect(start, id=id)
        elif s.name == "Finished":
            return redirect(finish, id=id)
        elif s.name == "Did Not Finish":
            return redirect(dnf, id=id)
        else:
            s.book_set.add(b)
    return redirect(view_book, id=id)
    
def changeBookshelf(response, id):
    if response.method == "POST":
        if not Book.objects.filter(id=id).exists():
            Book.objects.create(id=id)
        b = Book.objects.get(id=id)
        if response.POST.get("start"):
            return redirect(start, id=id)
        elif(response.POST.get("finish")):
            return redirect(finish, id=id)
        elif(response.POST.get("dnf")):
            return redirect(dnf, id=id)
    return redirect(view_book, id=id)


def start(response, id):
    book = Book.objects.get(id=id)
    book.started = True
    book.finished = False
    book.dnfed = False
    book.start_date = date.today()
    book.save()
    s = Bookshelf.objects.get(name="Currently Reading")
    s.book_set.add(book)
    s.save()
    if Bookshelf.objects.get(name="To Read").book_set.filter(id=book.id).exists():
        s2 = Bookshelf.objects.get(name="To Read")
        s2.book_set.remove(book)
        s2.save()
    return redirect(home)

def finish(response, id):
    book = Book.objects.get(id=id)
    book.started = True
    book.finished = True
    book.dnfed = False
    if not book.start_date:
        book.start_date = date.today()
    book.finish_date = date.today()
    book.progress = 100
    book.save()
    s = Bookshelf.objects.get(name="Finished")
    s.book_set.add(book)
    s.save()
    if Bookshelf.objects.get(name="Currently Reading").book_set.filter(id=book.id).exists():
        s2 = Bookshelf.objects.get(name="Currently Reading")
        s2.book_set.remove(book)
        s2.save()
    if Bookshelf.objects.get(name="To Read").book_set.filter(id=book.id).exists():
        s2 = Bookshelf.objects.get(name="To Read")
        s2.book_set.remove(book)
        s2.save()            
    return redirect(view_book, id=book.id)

def dnf(response, id):
    book = Book.objects.get(id=id)
    book.started = True
    book.finished = False
    book.dnfed = True
    if not book.start_date:
        book.start_date = date.today()
    book.finish_date = date.today()
    book.save()
    s = Bookshelf.objects.get(name="Did Not Finish")
    s.book_set.add(book)
    s.save()
    if Bookshelf.objects.get(name="Currently Reading").book_set.filter(id=book.id).exists():
        s2 = Bookshelf.objects.get(name="Currently Reading")
        s2.book_set.remove(book)
        s2.save()
    if Bookshelf.objects.get(name="To Read").book_set.filter(id=book.id).exists():
        s2 = Bookshelf.objects.get(name="To Read")
        s2.book_set.remove(book)
        s2.save()
    return redirect(home)



def books(response):
    shelves = Bookshelf.objects.all()
    return render(response, "main/books.html", {"shelves": shelves})

def shelf(response, id):
    b = Bookshelf.objects.get(id=id)
    return render(response, "main/shelf.html", {"shelf": b})

def stats(response):
    return render(response, "main/stats.html", {})
