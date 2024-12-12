# Generated by Django 5.1.4 on 2024-12-11 20:40

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "payment_gateway",
            "0004_merchant_paymentmethod_delete_paymentgateway_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentGateway",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("api_key", models.CharField(default="API_KEY", max_length=255)),
                ("api_secret", models.CharField(default="API_SECRET", max_length=255)),
                ("enabled", models.BooleanField(default=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name="ValidatePayment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("payment_id", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("PAID", "Paid"),
                            ("FAILED", "Failed"),
                        ],
                        default="PENDING",
                        max_length=10,
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name="PaymentMethod",
        ),
        migrations.RemoveField(
            model_name="invoice",
            name="merchant",
        ),
        migrations.RemoveField(
            model_name="merchant",
            name="address",
        ),
        migrations.RemoveField(
            model_name="merchant",
            name="phone",
        ),
        migrations.AddField(
            model_name="invoice",
            name="merchant_id",
            field=models.CharField(default="MERCHANT", max_length=100),
        ),
        migrations.AddField(
            model_name="invoice",
            name="merchant_webhook_url",
            field=models.URLField(default="http://localhost:8000/api/webhook/"),
        ),
        migrations.AddField(
            model_name="invoice",
            name="timestampt",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="merchant",
            name="api_key",
            field=models.CharField(default="API_KEY", max_length=255),
        ),
        migrations.AddField(
            model_name="merchant",
            name="api_secret",
            field=models.CharField(default="API_SECRET", max_length=255),
        ),
        migrations.AddField(
            model_name="merchant",
            name="timestamp",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="invoice_id",
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="payment_method_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("PAID", "Paid"),
                    ("FAILED", "Failed"),
                ],
                default="PENDING",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="merchant",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="merchant",
            name="webhook_url",
            field=models.URLField(default="http://localhost:8000/api/webhook/"),
        ),
        migrations.AddField(
            model_name="validatepayment",
            name="invoice",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="payment_gateway.invoice",
            ),
        ),
        migrations.AddField(
            model_name="validatepayment",
            name="payment_gateway",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="payment_gateway.paymentgateway",
            ),
        ),
    ]
