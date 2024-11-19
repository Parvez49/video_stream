# Generated by Django 5.1.3 on 2024-11-19 08:39

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Video",
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
                ("title", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("original_video", models.FileField(upload_to="videos/originals/")),
                (
                    "low_resolution_video",
                    models.FileField(blank=True, null=True, upload_to="videos/low/"),
                ),
                (
                    "medium_resolution_video",
                    models.FileField(blank=True, null=True, upload_to="videos/medium/"),
                ),
                (
                    "high_resolution_video",
                    models.FileField(blank=True, null=True, upload_to="videos/high/"),
                ),
            ],
        ),
    ]