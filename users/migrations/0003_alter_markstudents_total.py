# Generated by Django 4.1.3 on 2022-11-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_profile_contact"),
    ]

    operations = [
        migrations.AlterField(
            model_name="markstudents",
            name="total",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
