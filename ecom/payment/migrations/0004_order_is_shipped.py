# Generated by Django 5.1.3 on 2024-12-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_shippingaddress_shipping_address2_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
