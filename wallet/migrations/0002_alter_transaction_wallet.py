# Generated by Django 5.1.3 on 2024-12-12 05:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallet", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="wallet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="wallet.wallet"
            ),
        ),
    ]
