# Generated by Django 5.0.3 on 2024-04-26 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POSNAT', '0009_alter_ingrediente_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bebida',
            name='imagen',
            field=models.ImageField(default='static\\images\\sin.jpg', upload_to='bebidas/'),
        ),
    ]
