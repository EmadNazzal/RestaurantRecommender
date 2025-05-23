# Generated by Django 5.0.6 on 2024-07-18 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_recommender', '0022_remove_restaurant_positive_aspects'),
        ('user_management', '0014_remove_bookmark_dress_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmark',
            name='dress_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='positive_aspects',
            field=models.ManyToManyField(blank=True, related_name='bookmarks', to='restaurant_recommender.aspect'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='primary_cuisine',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
