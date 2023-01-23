from django import template
import requests
register = template.Library()

@register.filter
def extract_data(book):
    url = 'https://www.googleapis.com/books/v1/volumes/' + book.id
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
    return {"title": title, "authors": authors, "publisher": publisher, "pub_data": pub_date, 
        "desc": desc, "page_count": page_count, "avg_rating": avg_rating, "image": image}