# Generated by Django 4.1.5 on 2023-01-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='progress',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
