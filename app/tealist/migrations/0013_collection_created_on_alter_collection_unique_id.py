# Generated by Django 4.1.6 on 2023-03-22 19:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("tealist", "0012_alter_collection_unique_id_alter_collection_vendors"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="created_on",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="collection",
            name="unique_id",
            field=models.CharField(default="57ec", editable=False, max_length=6),
        ),
    ]