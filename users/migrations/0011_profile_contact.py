# Generated by Django 4.1.3 on 2022-11-28 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_profile_created_at_profile_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="contact",
            field=models.PositiveBigIntegerField(null=True, unique=True),
        ),
    ]
