# Generated by Django 3.2.5 on 2021-07-10 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210707_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
