# Generated by Django 4.2.9 on 2024-01-12 16:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tealist", "0029_alter_collection_unique_id_alter_tea_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="unique_id",
            field=models.CharField(default="eb4d", editable=False, max_length=6),
        ),
        migrations.AlterField(
            model_name="teavariant",
            name="title",
            field=models.CharField(max_length=256),
        ),
    ]
