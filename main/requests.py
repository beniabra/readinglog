from .models import Bookshelf, Book
from bs4 import BeautifulSoup
import requests

def setTitleAndAuthor(id):
    url = "https://www.googleapis.com/books/v1/volumes/" + id
    book = requests.get(url).json()
    try:
        title = book["volumeInfo"]["title"]
    except KeyError:
        title = "No Title Found"
    try:
        authors = ''
        for author in book["volumeInfo"]["authors"]:
            authors = authors + author + ", "
        authors = authors[0:-2]
    except KeyError:
        authors = "No Authors Found"
    b = Book.objects.get(id=id)
    b.title = title
    b.author = author
    b.save()
    return {"title": title, "authors": authors}

if __name__=="__main__": 
    books = Book.objects.all()
    for book in books:
        data = setTitleAndAuthor(book.id)
        book.author = data['authors']
        book.title = data['title']
        book.save()
