# Generated by Django 5.1.3 on 2024-12-13 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_rename_is_shipped_order_shipped_order_date_shiped'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_shiped',
            new_name='date_shipped',
        ),
    ]
