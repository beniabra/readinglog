from django.shortcuts import render, redirect
from .models import Bookshelf, Book
from .forms import EditDetails
from .requests import setTitleAndAuthor
from datetime import date
import requests


def home(response):
    f = Bookshelf.objects.get(name="Finished").book_set.all().count()
    results = {
        "books_finished": f,
        "book_goal": 50,
        "percent": round(f/50*100),
        "recently_finished": Bookshelf.objects.get(name="Finished").book_set.all().latest("finish_date"),
        "bookshelf": Bookshelf.objects.get(name="Currently Reading"),
        "to_read_bookshelf": Bookshelf.objects.get(name="To Read")
    }
    return render(response, "main/home.html", results)

def search(response):
    if response.method == "GET":
        if response.GET.get("search"):
            url = "https://www.googleapis.com/books/v1/volumes?q=" + response.GET.get("search").replace(" ", "+")
            search_results = requests.get(url).json()
            all_books = Bookshelf.objects.all()

    return render(response, "main/search.html", {"terms":response.GET.get("search"), "results":search_results["items"], "bookshelves": Bookshelf.objects.all(), "book_ids":  list(Book.objects.values_list("id",flat=True)), "all_books": Book.objects.all()})

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
        bookshelves = book.bookshelf.all()
    except Book.DoesNotExist:
        book = None
        added = False
        bookshelves = None
    return render(response, "main/view.html", {"added": added, "book_id": id, "book": book, "bookshelves": bookshelves})

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

def editRating(response,id):
    if response.method == "POST":
        print(response.POST)
        b = Book.objects.get(id=id)
        if response.POST.get('rating'):
            b.rating = float(response.POST.get('rating'))
            b.save()
    return redirect(view_book, id=id)

def editLikesDislikes(response, id):
    if response.method == "POST":
        print(response.POST)
        b = Book.objects.get(id=id)
        b.likes = response.POST.get('likes')
        b.dislikes = response.POST.get('dislikes')
        b.save()
    return redirect(view_book, id=id)

def addToBookshelf(response, id):
    if response.method == "POST":
        print(response.POST)
        if not Book.objects.filter(id=id).exists():
            Book.objects.create(id=id)
            setTitleAndAuthor(id)
        b = Book.objects.get(id=id)
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

def newBookshelf(response):
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("Name") and not Bookshelf.objects.filter(name=response.POST.get("Name")):
            Bookshelf.objects.create(name=response.POST.get("Name"))
            new_id = Bookshelf.objects.get(name=response.POST.get("Name")).id
            if response.POST.get("Books"):
                s = Bookshelf.objects.get(id=new_id)
                for b_id in response.POST.getlist("Books"):
                    print(b_id)
                    if Book.objects.filter(id=b_id).exists():
                        book = Book.objects.get(id=b_id)
                        s.book_set.add(book)
                s.save()
            return redirect(shelf,id=new_id, page=1, sort='finish_date')
    return redirect(books)
    
def changeBookshelf(response, id):
    if response.method == "POST":
        if not Book.objects.filter(id=id).exists():
            Book.objects.create(id=id)
            setTitleAndAuthor(id)
        b = Book.objects.get(id=id)
        if response.POST.get("start"):
            return redirect(start, id=id)
        elif(response.POST.get("finish")):
            return redirect(finish, id=id)
        elif(response.POST.get("dnf")):
            return redirect(dnf, id=id)
    return redirect(view_book, id=id)

def removeBook(response, shelf_id, book_id):
    if response.method == "POST":
        s = Bookshelf.objects.get(id=shelf_id)
        b = Book.objects.get(id=book_id)
        s.book_set.remove(b)
        s.save()
    return redirect(shelf,id=shelf_id, page=1, sort='finish_date')

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
    books = Book.objects.all()
    return render(response, "main/books.html", {"shelves": shelves, "books": books})

def shelf(response, id, page, sort):
    s = Bookshelf.objects.get(id=id)
    num = 15
    pages = int(s.book_set.count() / num)
    if s.book_set.count() % num > 0:
        pages += 1
    s_id = id
    if sort == "title":
        books = s.book_set.all().order_by('title')
    elif sort == "author":
        books = s.book_set.all().order_by('author')
    elif sort == "rating":
        books = s.book_set.all().order_by('-rating')
    elif sort == "start_date":
        books = s.book_set.all().order_by('start_date')
    elif sort == "finish_date":
        books = s.book_set.all().order_by('-finish_date')
    else:
        books = s.book_set.all()
    return render(response, "main/shelf.html", {"shelf": s, "books": books, "shelf_id": s_id, "pages": range(pages), "currPage": page, "sort": sort})

def shelfSort(response, id, page, sort):
    pass


def stats(response):
    return render(response, "main/stats.html", {})
