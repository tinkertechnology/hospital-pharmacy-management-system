# Generated by Django 2.2.2 on 2020-05-28 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
