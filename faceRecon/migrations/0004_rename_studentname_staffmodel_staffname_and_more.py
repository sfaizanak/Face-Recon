# Generated by Django 5.0.3 on 2024-03-22 06:30

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("faceRecon", "0003_staffmodel"),
    ]

    operations = [
        migrations.RenameField(
            model_name="staffmodel",
            old_name="studentName",
            new_name="staffName",
        ),
        migrations.RemoveField(
            model_name="staffmodel",
            name="year",
        ),
        migrations.AddField(
            model_name="staffmodel",
            name="desg",
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="staffmodel",
            name="img",
            field=models.FileField(upload_to="staffImg/"),
        ),
        migrations.AlterField(
            model_name="staffmodel",
            name="name_slug",
            field=autoslug.fields.AutoSlugField(
                default=None,
                editable=False,
                null=True,
                populate_from="staffName",
                unique=True,
            ),
        ),
    ]
