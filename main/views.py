from django.shortcuts import render
from django.http import HttpResponse

def home(response):
    return HttpResponse("<h1>Hello World</h1>")
