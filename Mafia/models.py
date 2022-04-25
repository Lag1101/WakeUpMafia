from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class League(models.Model):
    TYPE = [
        ('SEASON', 'Сезон'),
        ('SERIES', 'Серия'),
        ('FINAL', 'Финал'),
    ]

    name = models.CharField(max_length=100)
    rating_type = models.CharField(max_length=20, choices=TYPE, default='SEASON')
    admins_tag = models.CharField(max_length=20, default='NONE')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(max_length=100)
    date_event = models.DateField(auto_now=False)
    date_insert = models.DateField(auto_now_add=True, editable=False)
    judge = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(League, on_delete=models.DO_NOTHING)
    # type = models.CharField(max_length=20, choices=TYPE, default='FUN')
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    TEAM = [
        ('BLACK', 'Победа черных'),
        ('RED', 'Победа красных'),
        ('NONE', 'Нет результата')
    ]

    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    win = models.CharField(max_length=20, choices=TEAM, default='NONE')
    stats_calc = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.win


class Player(models.Model):
    ROLE = [
        ('CITIZEN', 'Мирный'),
        ('SHERIFF', 'Шериф'),
        ('MAFIA', 'Мафия'),
        ('DON', 'Дон'),
    ]

    NUMBER = [
        (1, 'Игрок #1'),
        (2, 'Игрок #2'),
        (3, 'Игрок #3'),
        (4, 'Игрок #4'),
        (5, 'Игрок #5'),
        (6, 'Игрок #6'),
        (7, 'Игрок #7'),
        (8, 'Игрок #8'),
        (9, 'Игрок #9'),
        (10, 'Игрок #10'),
    ]

    ADD_POINTS = [
        (0, 0),
        (-0.5, -0.5),
        (0.1, 0.1),
        (0.2, 0.2),
        (0.25, 0.25),
        (0.3, 0.3),
        (0.4, 0.4),
        (0.5, 0.5),
        (0.6, 0.6),
        (0.7, 0.7),
    ]

    COMMENT = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    ]

    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    people_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    number = models.IntegerField(choices=NUMBER)
    role = models.CharField(max_length=20, choices=ROLE, default='CITIZEN')
    best_move = models.CharField(max_length=20, default='none')
    point = models.FloatField(default=0)
    add_point = models.FloatField(choices=ADD_POINTS, default=0)
    comment = models.IntegerField(choices=COMMENT, default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.role


class PeopleStatistic(models.Model):
    people_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # all, win
    games = models.CharField(max_length=100, default='0|0')
    # CITIZEN SHERIFF MAFIA DON
    roles = models.CharField(max_length=100, default='0|0|0|0')
    win_roles = models.CharField(max_length=100, default='0|0|0|0')
    # times in2 full_best_move
    best_move = models.CharField(max_length=100, default='0|0|0')
    # played on 1, 2, 3...
    number_love = models.CharField(max_length=100, default='0|0|0|0|0|0|0|0|0|0')

    def __str__(self):
        return self.people_id
