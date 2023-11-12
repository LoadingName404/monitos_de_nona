# Generated by Django 4.2.5 on 2023-11-08 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Jornadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_cierre', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
                ('sku', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_usuario', models.CharField(max_length=50)),
                ('nombre_completo', models.CharField(max_length=250)),
                ('contra', models.CharField(max_length=20)),
                ('id_cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazarapp.cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('id_jornada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazarapp.jornadas')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazarapp.usuarios')),
            ],
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazarapp.productos')),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bazarapp.ventas')),
            ],
        ),
    ]
