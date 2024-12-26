# Generated by Django 5.1.3 on 2024-12-26 10:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_imageforcover_poster_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageForLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='upload/logo/')),
            ],
        ),
        migrations.AlterField(
            model_name='imageforcover',
            name='poster_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
