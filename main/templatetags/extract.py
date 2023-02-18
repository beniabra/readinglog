from django import template
from bs4 import BeautifulSoup
import requests
register = template.Library()

@register.filter
def extract_data(id):
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
    try:
        publisher = book["volumeInfo"]["publisher"]
    except KeyError:
        publisher = "No Publisher found"
    try: 
        pub_date = book["volumeInfo"]["publishedDate"]
    except KeyError:
        pub_date = "No Date found"
    try:
        desc = book["volumeInfo"]["description"]
    except KeyError:
        desc = "No Description found"
    try:
        page_count = book["volumeInfo"]["pageCount"]
    except KeyError:
        page_count = "No Page Count found"
    try:
        avg_rating = book["volumeInfo"]["averageRating"]
    except KeyError:
        avg_rating = 0
    try:
        image = book["volumeInfo"]["imageLinks"]["thumbnail"]
    except KeyError:
        image = "https://islandpress.org/sites/default/files/default_book_cover_2015.jpg"
    return {"url": url, "title": title, "authors": authors, "publisher": publisher, "pub_date": pub_date, 
        "desc": desc, "page_count": page_count, "avg_rating": avg_rating, "image": image}

@register.filter
def extract_html(desc):
    soup = BeautifulSoup(desc, 'html.parser')
    return soup.getText()
