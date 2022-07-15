# Generated by Django 3.2.2 on 2022-05-24 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_search'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=256)),
                ('lng', models.CharField(blank=True, max_length=128, null=True)),
                ('lnt', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='product.restaurant'),
        ),
    ]
