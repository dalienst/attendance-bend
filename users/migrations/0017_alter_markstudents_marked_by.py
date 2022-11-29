# Generated by Django 4.1.3 on 2022-11-28 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0016_markstudents_delete_approved"),
    ]

    operations = [
        migrations.AlterField(
            model_name="markstudents",
            name="marked_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
