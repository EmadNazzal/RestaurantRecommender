# Generated by Django 5.0.6 on 2024-07-18 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_recommender', '0021_restaurant_dress_code_restaurant_positive_aspects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='positive_aspects',
        ),
    ]
