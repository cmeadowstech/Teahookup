# Generated by Django 4.1.6 on 2024-01-02 23:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tealist", "0018_alter_location_options_alter_collection_unique_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="unique_id",
            field=models.CharField(default="e70d", editable=False, max_length=6),
        ),
    ]
