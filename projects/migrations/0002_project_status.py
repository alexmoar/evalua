# Generated by Django 4.0.4 on 2022-05-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('created', 'Creado'), ('draft', 'Borrador'), ('send', 'Enviado'), ('for_correction', 'Para corrección'), ('in_correction', 'En corrección'), ('qualified', 'Calificado')], default='created', max_length=15),
        ),
    ]
