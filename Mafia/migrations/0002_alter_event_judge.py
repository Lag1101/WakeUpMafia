# Generated by Django 3.2.12 on 2022-04-09 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Mafia', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='judge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
