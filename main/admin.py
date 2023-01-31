from django.contrib import admin

# Register your models here.
from .models import Bookshelf,Book
admin.site.register(Bookshelf)
admin.site.register(Book)