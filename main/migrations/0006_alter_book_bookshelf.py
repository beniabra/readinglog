# Generated by Django 4.1.5 on 2023-02-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_book_book_bookshelf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='bookshelf',
            field=models.ManyToManyField(related_name='books', to='main.bookshelf'),
        ),
    ]
