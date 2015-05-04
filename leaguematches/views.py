from django.shortcuts import render
from django.db.models import Q

from operator import itemgetter

from .models import Season
from .models import Player
from .models import MatchReport
from .models import MatchOrder


def season(request, season_id):
    # [round1, [{'player':player 'main_wins': %d, 'main_losses': %d, 'tb_wins': %d, 'tb_losses': %d, 'main_pts': %d, 'tb_pts': %d}, ...],
    #  round2, [...]]
    season_matches = MatchOrder.objects.filter(match__season_id=1)
    players = season_matches.distinct('player').values_list('player', flat=True)
    # [round1, [{'player':player 'main_wins': %d, 'main_losses': %d, 'tb_wins': %d, 'tb_losses': %d, 'main_pts': %d, 'tb_pts': %d}, ...],
    #  round2, [...]]
    results = []

    for round in season_matches.order_by('match__round').values_list('match__round',flat=True).distinct():
        p_res = []
        for player_id in players:
            # Get first 5 matches of the player for mains
            round_matches = season_matches.filter(player__id=player_id, match__round=round).order_by('order')
            mains = round_matches[0:5]
            # The rest are tiebreaker matches
            tbs = round_matches[5:]
            # 3 points for win and 1 point for a loss
            main_wins = 0
            main_losses = 0
            main_pts = 0
            for match in mains:
                if match.match.winner.id == player_id:
                    main_wins += 1
                    main_pts += 3
                else:
                    main_losses += 1
                    main_pts += 1
            # 3 points for a win and -1 for a loss (can't go below 0)
            tb_wins = 0
            tb_losses = 0
            tb_pts = 0
            for match in tbs:
                if match.match.winner.id == player_id:
                    tb_wins += 1
                    tb_pts += 3
                else:
                    tb_losses += 1
                    if (tb_pts > 0):
                        tb_pts -= 1
            player = Player.objects.get(pk=player_id)
            p_res += {'player': player,
                      'player_ln': player.user.last_name,
                      'player_fn': player.user.first_name,
                      'main_wins': main_wins, 'main_losses': main_losses,
                      'tb_wins': tb_wins, 'tb_losses': tb_losses,
                      'main_pts': main_pts, 'tb_pts': tb_pts},
        p_res = sorted(p_res, key=itemgetter('player_ln', 'player_fn'))
        p_res = sorted(p_res, key=itemgetter('main_pts', 'tb_pts'), reverse=True)
        results += [round, p_res],

#    for round, round_res in results:
#        print round
#        for p_res in round_res:
#            print '%s %s (mains %d-%d tbs %d-%d): mp=%d tbp=%d)' % \
#                   (p_res['player_fn'], p_res['player_ln'],
#                    p_res['main_wins'], p_res['main_losses'],
#                    p_res['tb_wins'], p_res['tb_losses'],
#                    p_res['main_pts'], p_res['tb_pts'])

    # Get total results by adding up the rounds
    total_results = []
    for player_id in players:
        player = Player.objects.get(pk=player_id)
        total_results+= {'player': player,
                         'player_ln': player.user.last_name,
                         'player_fn': player.user.first_name,
                         'main_wins': 0, 'main_losses': 0,
                         'tb_wins': 0, 'tb_losses': 0,
                         'main_pts': 0, 'tb_pts': 0},


    for round, round_res in results:
        for p_res in round_res:
           total_p_res = [rec for rec in total_results if rec['player'] == p_res['player']][0]
           for field in ['main_wins', 'main_losses', 'tb_wins', 'tb_losses', 'main_pts', 'tb_pts']:
               total_p_res[field] += p_res[field]
    total_results = sorted(total_results, key=itemgetter('player_ln', 'player_fn'))
    total_results = sorted(total_results, key=itemgetter('main_pts', 'tb_pts'), reverse=True)

    context = {'season': Season.objects.get(id=season_id),
               'matches': MatchReport.objects.filter(season__id=season_id),
               'results': results,
               'total_results': total_results}
    return render(request, 'leaguematches/season.html', context)

def player(request, player_id):
    #[ [season1, [[round1, [matchlist], [round2, [matchlist]] ... ]]], season2, ...]
    player_matches = MatchOrder.objects.filter(player=player_id)
    view_matches = []
    for season in Season.objects.filter(player=player_id):
        season_matches = player_matches.filter(match__season=season.id)
        round_matches = []
        for round in season_matches.order_by('match__round').values_list('match__round',flat=True).distinct():
            round_matches += [round, season_matches.filter(match__round=round).order_by('order')],
        view_matches += [season, round_matches],

    context = {'player': Player.objects.get(id=player_id),
               'matches': view_matches,}
    return render(request, 'leaguematches/player.html', context)

def index(request):
    season_list = Season.objects.all();
    context = {'season_list': season_list}
    return render(request, 'leaguematches/index.html', context)
