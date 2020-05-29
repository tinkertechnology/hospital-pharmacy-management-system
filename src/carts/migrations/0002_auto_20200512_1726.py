# Generated by Django 2.0 on 2020-05-12 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='carts.Cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='line_item_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10),
        ),
    ]