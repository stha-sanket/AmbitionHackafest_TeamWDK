# Generated by Django 4.2.7 on 2025-06-27 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharmacy", "0004_prescription_medicine_price_prescriptionitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="medicine",
            name="manufacturer",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
