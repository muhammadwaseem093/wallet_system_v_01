# Generated by Django 5.1.3 on 2024-12-12 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "payment_gateway",
            "0005_paymentgateway_validatepayment_delete_paymentmethod_and_more",
        ),
    ]

    operations = [
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
            name="timestampt",
        ),
        migrations.RemoveField(
            model_name="merchant",
            name="api_secret",
        ),
        migrations.RemoveField(
            model_name="merchant",
            name="timestamp",
        ),
        migrations.RemoveField(
            model_name="merchant",
            name="webhook_url",
        ),
        migrations.RemoveField(
            model_name="paymentgateway",
            name="api_key",
        ),
        migrations.RemoveField(
            model_name="paymentgateway",
            name="api_secret",
        ),
        migrations.RemoveField(
            model_name="paymentgateway",
            name="description",
        ),
        migrations.RemoveField(
            model_name="paymentgateway",
            name="timestamp",
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
        migrations.AddField(
            model_name="invoice",
            name="webhook_url",
            field=models.URLField(default="www.example.url"),
        ),
        migrations.AddField(
            model_name="merchant",
            name="address",
            field=models.TextField(default="sdfakljdglld a fdasjlk adgjlkd"),
        ),
        migrations.AddField(
            model_name="merchant",
            name="email",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="merchant",
            name="merchant_id",
            field=models.CharField(default="1363646ds", max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name="merchant",
            name="phone",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="paymentgateway",
            name="input_fields",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="address",
            field=models.TextField(
                blank=True, default="abc coudkldjl djlfjdls", null=True
            ),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="amount",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="currency",
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
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
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="payment_method_id",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.CharField(default="PENDING", max_length=20),
        ),
        migrations.AlterField(
            model_name="invoice",
            name="username",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="merchant",
            name="api_key",
            field=models.CharField(default="anasdlkaejrjdfl", max_length=100),
        ),
        migrations.AlterField(
            model_name="merchant",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="merchant",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="paymentgateway",
            name="name",
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name="ValidatePayment",
        ),
    ]
