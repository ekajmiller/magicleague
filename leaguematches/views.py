from django.shortcuts import render
from django.db.models import Q

from .models import Season
from .models import Player
from .models import MatchReport

def season(request, season_id):
    matches = MatchReport.objects.filter(season__id=season_id)
    _results = {}
    for match in matches:
        victor = match.victor()
        loser = match.loser()
        if victor not in _results:
            _results[victor] = {'wins':1, 'losses':0, 'main_points':3, 'tb_points': 0}
        else:
            _results[victor]['wins'] += 1
            if _results[victor]['wins'] + _results[victor]['losses'] < 6:
                _results[victor]['main_points'] += 3
            else:
                _results[victor]['tb_points'] += 3
        if loser not in _results:
            _results[loser] = {'wins':0, 'losses':1, 'main_points':1, 'tb_points': 0}
        else:
            _results[loser]['losses'] += 1
            if _results[loser]['wins'] + _results[loser]['losses'] < 6:
                _results[loser]['main_points'] += 1
            else:
                _results[loser]['tb_points'] -= 2
                if _results[loser]['tb_points'] < 0: _results[loser]['tb_points'] = 0
    results=[]
    for player in _results:
        results += {'player':player, 'wins': _results[player]['wins'], 'losses': _results[player]['losses'],
                    'main_points': _results[player]['main_points'], 'tb_points': _results[player]['tb_points']},
    final_results = sorted(results, key=lambda k: k['main_points'], reverse=True)

    context = {'season': Season.objects.get(id=season_id),
               'players': Player.objects.filter(seasons=season_id),
               'matches': MatchReport.objects.filter(season__id=season_id),
               'results': final_results}
    return render(request, 'leaguematches/season.html', context)

def player(request, player_id):
    player_matches=MatchReport.objects.filter(Q(reporter=player_id)|Q(opponent=player_id))
    view_matches = []
    for season in Season.objects.filter(player=player_id):
        view_matches += {'season': season, 'matches': player_matches.filter(season=season.id)},
    context = {'player': Player.objects.get(id=player_id),
               'matches': view_matches,}
    return render(request, 'leaguematches/player.html', context)

def index(request):
    season_list = Season.objects.all();
    context = {'season_list': season_list}
    return render(request, 'leaguematches/index.html', context)
