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
    return soup


print(extract_html("<p><b>En este primer volumen de las «Memorias del Águila y el Jaguar» Alexander Cold va a vivir una aventura que jamás olvidará.</b></p> <p>Alexander Cold es un muchacho americano de quince años que parte al Amazonas con su abuela Kate, periodista especializada en viajes. La expedición se interna en la selva en busca de una extraña bestia gigantesca. Junto a su compañera de viaje, Nadia Santos, y un centenario chamán indígena, Alex conocerá un mundo sorprendente.</p> <p>El universo ya conocido de Isabel Allende se amplía en <i>La Ciudad de las bestias </i>con nuevos elementos de realismo mágico, aventura y naturaleza. Los jóvenes protagonistas, Nadia y Alexander, se internan en la inexplorada selva amazónica llevando de la mano al lector en un viaje sin pausa por un territorio misterioso donde se borran los límites entre la realidad y el sueño, donde hombres y dioses se confunden, donde los espíritus andan de la mano con los vivos.</p> <p><i>«Aquí está todo lo que soy yo: toda mi manera de ser y de ver el mundo.»</i><br><b>Isabel Allende</b></p>"))
