# Generated by Django 3.2.2 on 2021-10-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новый'), ('APPROVED', 'Подтвержденный'), ('DONE', 'Завершен')], default='NEW', max_length=24),
        ),
    ]