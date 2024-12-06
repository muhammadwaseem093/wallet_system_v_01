# Generated by Django 5.1.3 on 2024-12-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_address_alter_user_groups_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.TextField(blank=True, null=True, verbose_name="Address"),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=15, null=True, verbose_name="Phone Number"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("merchant", "Merchant"),
                    ("user", "User"),
                ],
                default="user",
                max_length=10,
                verbose_name="Role",
            ),
        ),
    ]
