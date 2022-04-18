from django import forms
from django.forms import ModelForm, Textarea, CharField, widgets
from .models import *
from django.contrib.auth.models import User


class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class CreateEvent(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date_event', 'judge', 'type']


class CreateLeague(ModelForm):
    class Meta:
        model = League
        fields = ['name', 'rating_type']


class CreateGame(ModelForm):
    class Meta:
        model = Game
        fields = ['win']
        labels = {'win': 'Результат '}


class CreatePlayer(ModelForm):
    class Meta:
        model = Player
        fields = ['number', 'people_id', 'role', 'best_move', 'add_point', 'comment']
        labels = {
            'number': 'Номер ',
            'people_id': 'Игрок ',
            'role': 'Роль ',
            'best_move': 'Лучший ход ',
            'add_point': 'Доп.баллы ',
            'comment': 'Замечаний ',
        }
        widgets = {'best_move': widgets.TextInput(attrs={"class": "form-control"})}


class EditPlayers(ModelForm):
    class Meta:
        model = Player
        fields = ['number', 'people_id']
        labels = {
            'number': 'Номер ',
            'people_id': 'Игрок ',
        }


class EditResults(ModelForm):
    class Meta:
        model = Player
        fields = ['role']
        labels = {
            'role': 'Роль ',
        }


class EditBestMove(ModelForm):
    class Meta:
        model = Player
        fields = ['number', 'best_move']
        labels = {
            'number': 'Номер ',
            'best_move': 'Лучший ход ',
        }


class EditPoints(ModelForm):
    class Meta:
        model = Player
        fields = ['add_point']
        labels = {
            'add_point': 'Доп.балл ',
        }
