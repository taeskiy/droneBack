# Generated by Django 3.2.2 on 2021-12-18 12:00

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('product', '0003_alter_product_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Картинка')),
                ('url', models.URLField(blank=True, default=None, null=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', ckeditor.fields.RichTextField()),
                ('my_order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Вопросы ответы',
                'verbose_name_plural': 'Вопросы ответы',
                'ordering': ['my_order'],
            },
        ),
        migrations.CreateModel(
            name='MainCollections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='category.category')),
            ],
            options={
                'verbose_name': 'Коллекция на главной',
                'verbose_name_plural': 'Коллекции на главной',
            },
        ),
        migrations.CreateModel(
            name='CollectionProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='main.maincollections')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_product', to='product.product')),
            ],
            options={
                'verbose_name': 'Коллекция на главной',
                'verbose_name_plural': 'Коллекции на главной',
            },
        ),
    ]
