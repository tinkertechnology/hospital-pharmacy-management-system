# Generated by Django 2.2.2 on 2020-07-11 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_storewiseorder_is_transit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storewiseorder',
            options={'ordering': ['-created_at']},
        ),
    ]