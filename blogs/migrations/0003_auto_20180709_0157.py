# Generated by Django 2.0.7 on 2018-07-09 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20180708_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.TextField(default=''),
        ),
    ]
