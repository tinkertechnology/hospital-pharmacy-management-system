# Generated by Django 2.2.2 on 2020-12-31 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0011_uservariationquantityhistory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserVariationQuantityHistory',
        ),
    ]