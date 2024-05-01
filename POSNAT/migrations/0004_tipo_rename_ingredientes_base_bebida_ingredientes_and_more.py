# Generated by Django 5.0.3 on 2024-04-18 00:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POSNAT', '0003_categoria_bebida_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('detalles', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='bebida',
            old_name='ingredientes_base',
            new_name='ingredientes',
        ),
        migrations.RenameField(
            model_name='ingrediente',
            old_name='precio',
            new_name='precio_extra',
        ),
        migrations.RenameField(
            model_name='proveedor',
            old_name='apellido',
            new_name='compañia',
        ),
        migrations.RemoveField(
            model_name='ingrediente',
            name='proveedores',
        ),
        migrations.RemoveField(
            model_name='venta',
            name='cliente',
        ),
        migrations.AddField(
            model_name='bebida',
            name='imagen',
            field=models.ImageField(default='default_image.jpg', upload_to='imagenes'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='venta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='POSNAT.venta'),
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='cantidad_extra',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='imagen',
            field=models.ImageField(default='default_image.jpg', upload_to='imagenes'),
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POSNAT.proveedor'),
        ),
        migrations.AlterField(
            model_name='bebida',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POSNAT.categoria'),
        ),
        migrations.AlterField(
            model_name='bebida',
            name='precio_base',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bebida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POSNAT.bebida')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='POSNAT.venta')),
            ],
        ),
        migrations.AddField(
            model_name='venta',
            name='bebida',
            field=models.ManyToManyField(through='POSNAT.DetalleVenta', to='POSNAT.bebida'),
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='tipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='POSNAT.tipo'),
        ),
    ]
