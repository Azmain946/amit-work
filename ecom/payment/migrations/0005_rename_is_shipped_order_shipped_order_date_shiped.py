# Generated by Django 5.1.3 on 2024-12-12 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_is_shipped'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='is_shipped',
            new_name='shipped',
        ),
        migrations.AddField(
            model_name='order',
            name='date_shiped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
