# Generated by Django 4.2.6 on 2024-11-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0021_user_orders_delivered_on"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user_orders",
            name="delivered_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
