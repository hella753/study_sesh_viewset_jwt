# Generated by Django 5.1.2 on 2024-11-07 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_producttags_tag_name_en_producttags_tag_name_ka'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='სლაგი'),
        ),
    ]
