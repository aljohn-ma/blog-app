# Generated by Django 2.0.7 on 2018-07-09 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_auto_20180709_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='cover_image',
            field=models.FileField(upload_to='documents/'),
        ),
    ]