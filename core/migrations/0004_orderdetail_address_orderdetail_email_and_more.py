# Generated by Django 5.0.4 on 2024-05-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_product_id_cart_product_orderdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='email',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='firstname',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='lasttname',
            field=models.TextField(blank=True, null=True),
        ),
    ]