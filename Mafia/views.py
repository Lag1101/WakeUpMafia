from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import Http404
from .forms import *
from .models import *
from .app_function import *
import random
from django.db.models import Count, Sum


def index(request):
    event_list = Event.objects.all().order_by('-date_event')
    paginator = Paginator(event_list, 10)

    page = request.GET.get('page')
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'main.html', context={'events': events, })


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        x = user_form.fields['username']
        x.help_text = None
    return render(request, 'register.html', {'user_form': user_form})


def create_league(request):
    if request.method == "POST":
        form = CreateLeague(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/')
    else:
        form = CreateLeague()

    return render(request, 'create_league.html', {'form': form})


def create_event(request):
    if request.method == "POST":
        form = CreateEvent(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/')
    else:
        form = CreateEvent()

    return render(request, 'create_event.html', {'form': form})


def event(request, event_id):
    try:
        event_id = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")

    league = League.objects.get(name=event_id.type)
    game_with_player = []
    games = Game.objects.filter(event_id=event_id)
    for game in games:
        players = Player.objects.filter(game_id=game).order_by('number')
        game_with_player.append([game, players])

    return render(request, 'event.html', context={'event': event_id,
                                                  'game_with_player': game_with_player,
                                                  'league': league, })


def create_game(request, event_id):
    if request.method == "POST":
        event_id = Event.objects.get(id=event_id)
        g = Game(
            event_id=event_id,
            win=request.POST['win']
        )
        g.save()

        for i in range(10):
            people_id = User.objects.get(id=int(request.POST.getlist('people_id')[i]))
            p = Player(
                game_id=g,
                people_id=people_id,
                number=int(request.POST.getlist('number')[i]),
                role=request.POST.getlist('role')[i],
                best_move=request.POST.getlist('best_move')[i],
                add_point=int(request.POST.getlist('add_point')[i]),
                comment=int(request.POST.getlist('comment')[i]),
            )
            p.save()

        calculate_point(g.id)

        return HttpResponseRedirect('/')
    else:
        game_form = CreateGame()
        players_form = []
        for i in range(10):
            players_form.append(CreatePlayer(initial={'number': i + 1}))

    return render(request, 'create_game.html', {'game_form': game_form, 'players_form': players_form, })


def generate_game(request, event_id):
    this_page = '/mafia/event/' + str(event_id)
    event_id = Event.objects.get(id=event_id)
    games = Game.objects.all().order_by('id')
    if games:
        last_game = games.reverse()[0]
        players = Player.objects.filter(game_id=last_game)
        new_game_list = []
        for player in players:
            new_game_list.append([random.randint(1, 100), player.people_id])
        new_game_list.sort(key=lambda el: el[0])

        g = Game(
            event_id=event_id
        )
        g.save()

        for i in range(len(new_game_list)):
            p = Player(
                game_id=g,
                people_id=new_game_list[i][1],
                number=i+1,
            )
            p.save()

    return HttpResponseRedirect(this_page)


def game_info(request, event_id, game_id):
    event_id = Event.objects.get(id=event_id)
    league = League.objects.get(name=event_id.type)
    game_id = Game.objects.get(id=game_id)
    players = Player.objects.filter(game_id=game_id).order_by('number')

    return render(request, 'game_info.html', context={'event': event_id,
                                                      'league': league,
                                                      'game': game_id,
                                                      'players': players, })


def game_edit_players(request, event_id, game_id):
    if request.method == "POST":
        players = Player.objects.filter(game_id=game_id).order_by('number')
        for player in players:
            for i in range(10):
                if int(player.number) == int(request.POST.getlist('number')[i]):
                    people = User.objects.get(id=int(request.POST.getlist('people_id')[i]))
                    player.people_id = people
                    player.save()

        return HttpResponseRedirect('../' + str(game_id))

    else:
        players = Player.objects.filter(game_id=game_id).order_by('number')
        players_form = []
        for i in range(len(players)):
            players_form.append(EditPlayers(initial={'number': players[i].number, 'people_id': players[i].people_id}))

    return render(request, 'game_edit_players.html', {'players_form': players_form, })


def game_edit_results(request, event_id, game_id):
    if request.method == "POST":

        game = Game.objects.get(id=game_id)
        game_result = request.POST['win']
        game.win = game_result
        game.save()

        players = Player.objects.filter(game_id=game_id).order_by('number')
        for i in range(10):
            player = players[i]
            player.role = request.POST.getlist('role')[i]
            player.save()

        calculate_point(game_id)

        return HttpResponseRedirect('../' + str(game_id))
    else:
        game = Game.objects.get(id=game_id)
        game_form = CreateGame(initial={'win': game.win, })

        players = Player.objects.filter(game_id=game_id).order_by('number')
        players_form = []
        for i in range(len(players)):
            players_form.append([players[i], EditResults(initial={'role': players[i].role})])

    return render(request, 'game_edit_results.html', {'game_form': game_form, 'players_form': players_form, })


def game_edit_points(request, event_id, game_id):
    if request.method == "POST":

        game = Game.objects.get(id=game_id)
        game_result = game.win

        players = Player.objects.filter(game_id=game_id).order_by('number')
        for i in range(10):
            player = players[i]
            player.add_point = float(request.POST.getlist('add_point')[i])
            player.save()

        calculate_point(game_id)

        return HttpResponseRedirect('../' + str(game_id))
    else:
        players = Player.objects.filter(game_id=game_id).order_by('number')
        players_form = []
        for i in range(len(players)):
            players_form.append([players[i], EditPoints(initial={'add_point': players[i].add_point})])

    return render(request, 'game_edit_points.html', {'players_form': players_form, })


def game_edit_best_move(request, event_id, game_id):
    if request.method == "POST":

        first_kill = int(request.POST['number'])
        best_move = request.POST['best_move']

        players = Player.objects.filter(game_id=game_id).order_by('number')
        for player in players:
            if player.best_move != 'none' and player.number != first_kill:
                player.best_move = 'none'
                player.add_point = 0
                player.save()
            if player.number == first_kill:
                player.best_move = best_move
                player.save()

        for player in players:
            print(player.people_id)
            print(player.best_move)

        calculate_point(game_id)

        return HttpResponseRedirect('../' + str(game_id))
    else:
        players = Player.objects.filter(game_id=game_id).order_by('number')
        change_move = False
        number = 0
        best = 'none'
        for player in players:
            if player.best_move != 'none':
                change_move = True
                number = player.number
                best = player.best_move

        if change_move:
            form = EditBestMove(initial={'number': number, 'best_move': best, })
        else:
            form = EditBestMove()
    return render(request, 'game_edit_best_move.html', {'form': form, })


def rating(request):
    leagues = League.objects.filter(active=True)
    rating_tables = []
    for league in leagues:
        events = Event.objects.filter(type=league)
        games = Game.objects.filter(event_id__in=events)
        players = Player.objects.filter(game_id__in=games)

        rate = dict()
        for p in players:
            if p.people_id not in rate:
                # ник, игры, победы, баллы, доп. баллы
                if p.point >= 1:
                    rate[p.people_id] = [p.people_id, 1, 1, p.point, p.add_point]
                else:
                    rate[p.people_id] = [p.people_id, 1, 0, p.point, p.add_point]
            else:
                values = rate[p.people_id]
                values[1] += 1
                if p.point >= 1:
                    values[2] += 1
                values[3] += p.point
                values[4] += p.add_point

        values = rate.values()

        rating_table = []
        for x in values:
            line = []
            for y in x:
                line.append(y)

            if league.rating_type == 'SEASON':
                line.append(round(2 * line[2] * 2 * line[2]/line[1], 2))
            elif league.rating_type == 'SERIES':
                line.append(round(line[3], 2))
            else:
                line.append(round(line[3], 2))

            rating_table.append(line)

        rating_table.sort(key=lambda el: el[5], reverse=True)

        place = 1
        for x in rating_table:
            x.append(place)
            place += 1

        rating_tables.append([league.name, league.id, rating_table])

    return render(request, 'rating_table.html', {'rating_tables': rating_tables, })


def full_rating(request, league_id):
    leagues = League.objects.filter(id=league_id)
    rating_tables = []

    for league in leagues:
        events = Event.objects.filter(type=league)
        games = Game.objects.filter(event_id__in=events)
        players = Player.objects.filter(game_id__in=games)

        rate = dict()
        for p in players:
            if p.people_id not in rate:
                # ник, игры, победы, баллы, доп. баллы
                if p.point >= 1:
                    rate[p.people_id] = [p.people_id, 1, 1, p.point, p.add_point]
                else:
                    rate[p.people_id] = [p.people_id, 1, 0, p.point, p.add_point]
            else:
                values = rate[p.people_id]
                values[1] += 1
                if p.point >= 1:
                    values[2] += 1
                values[3] += p.point
                values[4] += p.add_point

        values = rate.values()

        rating_table = []
        for x in values:
            line = []
            for y in x:
                line.append(y)

            if league.rating_type == 'SEASON':
                line.append(round(2 * line[2] * 2 * line[2] / line[1], 2))
            elif league.rating_type == 'SERIES':
                line.append(round(line[3], 2))
            else:
                line.append(round(line[3], 2))

            rating_table.append(line)

        rating_table.sort(key=lambda el: el[5], reverse=True)

        place = 1
        for x in rating_table:
            x.append(place)
            place += 1

        rating_tables.append([league.name, league.id, rating_table])

    return render(request, 'rating_table_full.html', {'rating_tables': rating_tables, })
