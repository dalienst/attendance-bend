# Generated by Django 4.1.3 on 2022-11-29 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0019_alter_markstudents_options_remove_markstudents_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="contact",
            field=models.BigIntegerField(
                default=0, unique=True, verbose_name="phone number"
            ),
        ),
    ]