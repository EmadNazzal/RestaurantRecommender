# Generated by Django 5.0.6 on 2024-07-15 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_recommender', '0011_restaurant_attributes_restaurant_cuisine_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='hours_of_operation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='parking_details',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='parking_information',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
