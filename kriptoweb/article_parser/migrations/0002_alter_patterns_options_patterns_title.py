# Generated by Django 4.0.4 on 2022-06-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_parser', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patterns',
            options={'ordering': ['datetime']},
        ),
        migrations.AddField(
            model_name='patterns',
            name='title',
            field=models.TextField(default='noTitle'),
        ),
    ]
