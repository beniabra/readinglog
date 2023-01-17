from django.shortcuts import render
from django.http import HttpResponse

def home(response):
    return render(response, "main/home.html", {})

def books(response):
    return render(response, "main/books.html", {})

def stats(response):
    return render(response, "main/stats.html", {})
