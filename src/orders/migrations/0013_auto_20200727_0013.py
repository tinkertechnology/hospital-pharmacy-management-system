# Generated by Django 2.2.2 on 2020-07-26 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20200711_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_auto_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='storewiseorder',
            name='is_auto_order',
            field=models.BooleanField(default=False),
        ),
    ]
