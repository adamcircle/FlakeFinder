# Generated by Django 3.1.2 on 2021-07-13 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Soundings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('latitude',
                 models.DecimalField(decimal_places=2, max_digits=5)),
                ('longitude',
                 models.DecimalField(decimal_places=2, max_digits=5)),
                ('temp', models.DecimalField(decimal_places=1, max_digits=4)),
                ('dewpt', models.DecimalField(decimal_places=1, max_digits=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
