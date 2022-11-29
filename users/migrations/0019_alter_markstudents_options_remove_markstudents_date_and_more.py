# Generated by Django 4.1.3 on 2022-11-29 07:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0018_alter_markstudents_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="markstudents",
            options={"ordering": ["created_at", "student", "status"]},
        ),
        migrations.RemoveField(
            model_name="markstudents",
            name="date",
        ),
        migrations.AddField(
            model_name="markstudents",
            name="created_at",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="markstudents",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]