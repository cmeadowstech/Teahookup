# Generated by Django 4.2.9 on 2024-01-12 16:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tealist", "0031_alter_collection_unique_id_alter_tea_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="collection",
            name="unique_id",
            field=models.CharField(default="8322", editable=False, max_length=6),
        ),
        migrations.AlterUniqueTogether(
            name="teavariant",
            unique_together={("tea", "title")},
        ),
    ]
