# Generated by Django 4.1.5 on 2023-02-18 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_book_status_book_dnfed_book_finished_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book',
        ),
        migrations.AddField(
            model_name='book',
            name='book',
            field=models.ManyToManyField(to='main.bookshelf'),
        ),
    ]