# Generated by Django 3.2.2 on 2021-12-19 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_imei'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CART', 'В корзине'), ('NEW', 'Новый'), ('APPROVED', 'Подтвержденный'), ('DONE', 'Завершен')], default='NEW', max_length=24),
        ),
    ]
