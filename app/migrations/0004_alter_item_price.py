# Generated by Django 4.1.3 on 2022-11-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_stripe_id_item_stripe_price_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(default=0, help_text='От 5к для рублей, от 50 для usd'),
        ),
    ]