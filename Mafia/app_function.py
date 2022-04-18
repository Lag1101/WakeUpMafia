from .models import *


def check_best_move(black_team, best_move):
    black_team_num = []
    for x in black_team:
        if x.isdigit():
            black_team_num.append(int(x))
    if len(black_team_num) > 3:
        if black_team_num[2] == 1 and black_team_num[3] == 0:
            black_team_num = [black_team_num[0], black_team_num[1], 10]
        else:
            black_team_num = [black_team_num[0], black_team_num[1], black_team_num[2]]

    best_move_num = []
    for x in best_move:
        if x.isdigit():
            best_move_num.append(int(x))
    if len(best_move_num) > 3:
        if best_move_num[2] == 1 and best_move_num[3] == 0:
            best_move_num = [best_move_num[0], best_move_num[1], 10]
        else:
            best_move_num = [best_move_num[0], best_move_num[1], best_move_num[2]]

    targets = 0
    for x in black_team_num:
        for y in best_move_num:
            if x == y:
                targets += 1

    return targets


def calculate_point(game):
    this_game = Game.objects.get(id=game)
    this_players = Player.objects.filter(game_id=this_game).order_by('number')

    game_result = this_game.win
    black_team = ''
    for player in this_players:
        if player.role == 'MAFIA' or player.role == 'DON':
            black_team += str(player.number)

    for player in this_players:
        if game_result == 'NONE':
            player.point = 0
            player.save()
        elif game_result == 'RED':
            if player.role == 'CITIZEN' or player.role == 'SHERIFF':
                if player.best_move != 'none':
                    targets = check_best_move(black_team, player.best_move)
                    if targets == 2:
                        player.add_point = 0.25
                    elif targets == 3:
                        player.add_point = 0.4
                player.point = 1 + player.add_point
                player.save()
            else:
                player.point = 0 + player.add_point
                player.save()
        elif game_result == 'BLACK':
            if player.role == 'MAFIA' or player.role == 'DON':
                player.point = 1 + player.add_point
                player.save()
            else:
                if player.best_move != 'none':
                    targets = check_best_move(black_team, player.best_move)
                    if targets == 2:
                        player.add_point = 0.25
                    elif targets == 3:
                        player.add_point = 0.4
                player.point = 0 + player.add_point
                player.save()


