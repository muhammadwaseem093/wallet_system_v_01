# Generated by Django 5.1.4 on 2024-12-11 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment_gateway", "0003_invoice_alter_paymentgateway_created_at_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Merchant",
            fields=[
                (
                    "id",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=255)),
                ("webhook_url", models.URLField()),
                ("address", models.TextField()),
                ("phone", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("enabled", models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name="PaymentGateway",
        ),
        migrations.RemoveField(
            model_name="invoice",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="invoice",
            name="merchant_id",
        ),
        migrations.RemoveField(
            model_name="invoice",
            name="merchant_webhook_url",
        ),
        migrations.RemoveField(
            model_name="invoice",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="invoice",
            name="address",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="invoice_id",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="payment_method_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.CharField(default="PENDING", max_length=50),
        ),
        migrations.AddField(
            model_name="invoice",
            name="merchant",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="payment_gateway.merchant",
            ),
        ),
    ]