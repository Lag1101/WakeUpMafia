# Generated by Django 3.2.12 on 2022-04-11 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mafia', '0004_auto_20220411_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='add_point',
            field=models.DecimalField(choices=[(-0.5, -0.5), (0, 0), (0.1, 0.1), (0.2, 0.2), (0.25, 0.25), (0.3, 0.3), (0.4, 0.4), (0.5, 0.5), (0.6, 0.6), (0.7, 0.7)], decimal_places=3, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='player',
            name='comment',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='number',
            field=models.IntegerField(choices=[(1, 'Игрок #1'), (2, 'Игрок #2'), (3, 'Игрок #3'), (4, 'Игрок #4'), (5, 'Игрок #5'), (6, 'Игрок #6'), (7, 'Игрок #7'), (8, 'Игрок #8'), (9, 'Игрок #9'), (10, 'Игрок #10')]),
        ),
        migrations.AlterField(
            model_name='player',
            name='role',
            field=models.CharField(choices=[('CITIZEN', 'Мирный'), ('SHERIFF', 'Шериф'), ('MAFIA', 'Мафия'), ('DON', 'Дон')], default='CITIZEN', max_length=20),
        ),
    ]
