# Generated by Django 4.1.3 on 2022-12-02 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flights", "0002_book"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={
                "ordering": ["name", "contact", "email", "flight", "date", "created_at"]
            },
        ),
        migrations.AddField(
            model_name="book",
            name="email",
            field=models.EmailField(default="admin@mail.com", max_length=254),
            preserve_default=False,
        ),
    ]