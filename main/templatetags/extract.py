from django import template
from bs4 import BeautifulSoup
import requests
register = template.Library()

@register.filter
def extract_data(id):
    url = "https://www.googleapis.com/books/v1/volumes/" + id
    book = requests.get(url).json()
    title = book["volumeInfo"]["title"]
    authors = ''
    for author in book["volumeInfo"]["authors"]:
        authors = authors + author + ", "
    authors = authors[0:-2]
    publisher = book["volumeInfo"]["publisher"]
    pub_date = book["volumeInfo"]["publishedDate"]
    desc = book["volumeInfo"]["description"]
    page_count = book["volumeInfo"]["pageCount"]
    avg_rating = book["volumeInfo"]["averageRating"]
    image = book["volumeInfo"]["imageLinks"]["thumbnail"]
    return {"url": url, "title": title, "authors": authors, "publisher": publisher, "pub_date": pub_date, 
        "desc": desc, "page_count": page_count, "avg_rating": avg_rating, "image": image}

@register.filter
def extract_html(desc):
    soup = BeautifulSoup(desc, 'html.parser')
    return soup.getText()
