# Generated by Django 5.1.2 on 2024-11-08 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreviews',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='store.product', verbose_name='პროდუქტი'),
        ),
    ]
