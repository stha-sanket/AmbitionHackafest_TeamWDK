# Generated by Django 4.2.7 on 2025-06-27 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BloodUnit",
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
                (
                    "blood_group",
                    models.CharField(
                        choices=[
                            ("A+", "A+"),
                            ("A-", "A-"),
                            ("B+", "B+"),
                            ("B-", "B-"),
                            ("AB+", "AB+"),
                            ("AB-", "AB-"),
                            ("O+", "O+"),
                            ("O-", "O-"),
                        ],
                        max_length=3,
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                ("date_added", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
