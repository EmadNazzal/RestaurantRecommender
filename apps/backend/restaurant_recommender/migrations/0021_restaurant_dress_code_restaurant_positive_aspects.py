# Generated by Django 5.0.6 on 2024-07-18 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_recommender', '0020_remove_restaurant_negative_aspects_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='dress_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='positive_aspects',
            field=models.TextField(blank=True, null=True),
        ),
    ]
