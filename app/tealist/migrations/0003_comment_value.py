# Generated by Django 4.1.6 on 2023-03-14 20:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tealist", "0002_comment_one comment per user per vendor"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="value",
            field=models.IntegerField(
                choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")], default=5
            ),
            preserve_default=False,
        ),
    ]
