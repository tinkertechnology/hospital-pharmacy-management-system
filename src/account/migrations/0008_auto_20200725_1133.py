# Generated by Django 2.2.2 on 2020-07-25 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20200723_2332'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='firstname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='lastname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
