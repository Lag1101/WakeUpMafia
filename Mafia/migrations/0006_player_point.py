# Generated by Django 3.2.12 on 2022-04-11 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mafia', '0005_auto_20220412_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='point',
            field=models.IntegerField(default=0),
        ),
    ]
