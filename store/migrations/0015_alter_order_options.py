# Generated by Django 4.0.6 on 2022-08-02 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can Cancel Order')]},
        ),
    ]
