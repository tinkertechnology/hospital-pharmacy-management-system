# Generated by Django 2.2.2 on 2020-08-08 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20200728_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='storewiseorder',
            name='remarks',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]