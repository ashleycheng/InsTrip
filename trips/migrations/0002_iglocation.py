# Generated by Django 4.2.13 on 2024-06-20 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="IgLocation",
            fields=[
                (
                    "location_id",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
                ("location_name", models.CharField(max_length=100)),
                (
                    "location_city",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("country", models.CharField(blank=True, max_length=30, null=True)),
                ("category", models.CharField(blank=True, max_length=30, null=True)),
                ("address", models.CharField(blank=True, max_length=200, null=True)),
                ("city", models.CharField(blank=True, max_length=50, null=True)),
                ("lat", models.CharField(blank=True, max_length=30, null=True)),
                ("lng", models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={"db_table": "IgLocation", "managed": False,},
        ),
    ]
