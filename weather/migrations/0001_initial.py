# Generated by Django 3.1.2 on 2021-06-19 23:55

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sounding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('forecast_date', models.DateTimeField()),
            ],
        ),
    ]
