# Generated by Django 4.1.6 on 2024-02-19 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("traductor", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="image",
            field=models.ImageField(default=1, upload_to="blog/images"),
            preserve_default=False,
        ),
    ]
