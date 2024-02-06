# Generated by Django 5.0 on 2023-12-10 19:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Producto o Servicio',
                'verbose_name_plural': 'Productos y Servicios',
                'db_table': 'ProductoServicio',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='garantia',
            name='producto_servicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='index.productoservicio'),
        ),
    ]
