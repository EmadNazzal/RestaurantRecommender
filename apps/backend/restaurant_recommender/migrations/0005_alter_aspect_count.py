# Generated by Django 5.0.6 on 2024-07-02 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_recommender', '0004_aspect_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aspect',
            name='count',
            field=models.IntegerField(),
        ),
    ]
