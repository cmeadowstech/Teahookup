# Generated by Django 4.1.6 on 2023-03-20 22:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tealist", "0008_collection_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="rating",
            field=models.ManyToManyField(
                blank=True,
                related_name="collection_voters",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="collection_owner",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]