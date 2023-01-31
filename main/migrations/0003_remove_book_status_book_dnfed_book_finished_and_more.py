# Generated by Django 4.1.5 on 2023-01-31 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_book_progress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='status',
        ),
        migrations.AddField(
            model_name='book',
            name='dnfed',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='book',
            name='finished',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='book',
            name='started',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
