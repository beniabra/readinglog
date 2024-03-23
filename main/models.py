from django.db import models
from django.urls import reverse

class Bookshelf(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateField(auto_now=False, auto_now_add=True)
    editable = models.BooleanField(default=False, blank=True)

    class Meta:
        ordering = ['date_created']

    def get_absolute_url(self):
        return reverse('model_detail_view', args=[str(self.id)])

    def __str__(self):
        return self.name

class Book(models.Model):
    bookshelf = models.ManyToManyField(Bookshelf, related_name='book_set')
    id = models.CharField(max_length=12, primary_key=True)
    title = models.CharField(max_length=100, default=False, blank=True)
    author = models.CharField(max_length=100, default=False, blank=True)
    started = models.BooleanField(default=False, blank=True)
    finished = models.BooleanField(default=False, blank=True)
    dnfed = models.BooleanField(default=False, blank=True)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    current_page = models.PositiveIntegerField(default=0, blank=True)
    progress = models.PositiveIntegerField(default=0, blank=True)
    RATING_CHOICES = [
        (0.5, '0.5'),
        (1.0, '1'),
        (1.5, '1.5'),
        (2.0, '2'),
        (2.5, '2.5'),
        (3.0, '3'),
        (3.5, '3.5'),
        (4.0, '4'),
        (4.5, '4.5'),
        (5.0, '5'),
    ]
    rating = models.DecimalField(max_digits=2, decimal_places= 1, choices=RATING_CHOICES, default=0.0, blank=True)
    likes = models.TextField(help_text='What did you like about the book?', blank=True)
    dislikes = models.TextField(help_text='What did you dislike about the book?', blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-finish_date']

    def get_absolute_url(self):
        return reverse('model_detail_view', args=[str(self.id)])

    def __str__(self):
        return self.id

    def get_fields(self):
        print("id: " + str(self.id))
        print("title: " + str(self.title) + " | author: " + str(self.author))
        print("started: " + str(self.started) + " | finished: " + str(self.finished) + " | dnfed: " + str(self.dnfed))
        print("start date: " + str(self.start_date) + " | finish date: " + str(self.finish_date))
        print("current page: " + str(self.current_page) + " | progress: " + str(self.progress))
        print("rating: " + str(self.rating))
        print("likes: " + str(self.likes) + " | dislikes: " + str(self.dislikes) + " | notes: " + str(self.notes))