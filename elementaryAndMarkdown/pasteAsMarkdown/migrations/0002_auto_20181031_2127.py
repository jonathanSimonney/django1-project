# Generated by Django 2.1.2 on 2018-10-31 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pasteAsMarkdown', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pastebin',
            name='path',
            field=models.CharField(max_length=34),
        ),
    ]