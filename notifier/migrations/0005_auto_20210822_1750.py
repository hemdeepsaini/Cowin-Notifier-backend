# Generated by Django 3.0.7 on 2021-08-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0004_auto_20210822_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='pin',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
