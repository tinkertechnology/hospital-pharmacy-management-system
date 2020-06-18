# Generated by Django 2.2.2 on 2020-06-17 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200613_1735'),
        ('orders', '0007_auto_20200610_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fk_ordered_by_store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fk_ordered_by_store', to='store.Store'),
        ),
    ]