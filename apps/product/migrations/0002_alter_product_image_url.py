# Generated by Django 3.2.2 on 2021-10-01 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, max_length=5000, null=True, verbose_name='Изображение'),
        ),
    ]