# Generated by Django 5.1.3 on 2024-12-26 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_imageforlogo_alter_imageforcover_poster_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutWebsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField(blank=True, max_length=3000, null=True)),
            ],
        ),
    ]
