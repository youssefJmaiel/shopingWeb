# Generated by Django 3.2.19 on 2023-05-22 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20230522_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]
