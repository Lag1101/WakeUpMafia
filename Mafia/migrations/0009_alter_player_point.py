# Generated by Django 3.2.12 on 2022-04-11 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mafia', '0008_alter_player_add_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='point',
            field=models.FloatField(default=0),
        ),
    ]
