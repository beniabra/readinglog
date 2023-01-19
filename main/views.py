from django.shortcuts import render
from django.http import HttpResponse
import requests

def home(response):
    url = 'https://www.googleapis.com/books/v1/volumes/lxGuDwAAQBAJ'
    book = requests.get(url).json()
    book_title = book["volumeInfo"]["title"]
    book_author = book["volumeInfo"]["authors"][0]
    results = {
        "books_finished": 5,
        "book_goal": 35,
        "percent": round(5/35*100),
        "book_title": book_title,
        "book_author": book_author
    }
    return render(response, "main/home.html", results)

def books(response):
    return render(response, "main/books.html", {})

def stats(response):
    return render(response, "main/stats.html", {})
