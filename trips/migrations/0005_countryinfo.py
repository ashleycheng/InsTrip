# Generated by Django 4.2.13 on 2024-07-05 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trips", "0004_cityinfo_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="CountryInfo",
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
                ("country_name", models.CharField(max_length=30)),
                ("country_name_ch", models.CharField(max_length=30)),
                ("image", models.URLField(blank=True, null=True)),
                ("analysis", models.TextField(blank=True, null=True)),
            ],
            options={"db_table": "CountryInfo",},
        ),
    ]
