# Generated by Django 3.1.2 on 2021-07-15 14:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='snowlocation',
            name='og_name',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='snowlocation',
            name='name',
            field=models.TextField(),
        ),
    ]
