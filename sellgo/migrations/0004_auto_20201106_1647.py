# Generated by Django 3.1.3 on 2020-11-06 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellgo', '0003_auto_20201106_1637'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csv_product',
            old_name='created',
            new_name='uploaded_date',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='created',
            new_name='created_date',
        ),
    ]