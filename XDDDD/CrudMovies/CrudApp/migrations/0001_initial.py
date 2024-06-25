# Generated by Django 5.0.6 on 2024-06-25 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Critica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_pelicula', models.CharField(max_length=200)),
                ('año_estreno', models.IntegerField()),
                ('puntuacion', models.FloatField()),
                ('sinopsis', models.TextField()),
            ],
        ),
    ]