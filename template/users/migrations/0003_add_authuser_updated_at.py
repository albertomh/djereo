from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_userprofile"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="authuser",
            options={"verbose_name": "auth user"},
        ),
        migrations.AddField(
            model_name="authuser",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
