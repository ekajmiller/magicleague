from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash

from operator import itemgetter

from .models import Season
from .models import Player
from .models import MatchReport
from .models import MatchOrder

from .forms import ProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from datetime import *

def addMatch(player_id, opponent_id, season_id, round, date_str, won):
    # Get objects; plus this double checks everything exists and in correct format
    reporter = Player.objects.get(pk=player_id)
    opponent = Player.objects.get(pk=opponent_id)
    season = Season.objects.get(pk=season_id, player=player_id)
    date = datetime.strptime(date_str, '%Y-%m-%d')
    winner = reporter if won else opponent
    loser = reporter if not won else opponent

    # First add match
    match = MatchReport(reporter=reporter,
                        opponent=opponent,
                        winner=winner,
                        loser=loser,
                        round=round,
                        season=season,
                        report_date=datetime.now(),
                        played_date=date,
                        win=won,
                        verified=False)
    match.save()

    # Now add order matches, one for each player
    reporter_order = MatchOrder.objects.filter(player=reporter,match__round=round).count() + 1
    opponent_order = MatchOrder.objects.filter(player=opponent,match__round=round).count() + 1
    reporter_mo = MatchOrder(player=reporter, match=match, order=reporter_order)
    opponent_mo = MatchOrder(player=opponent, match=match, order=opponent_order)
    reporter_mo.save()
    opponent_mo.save()


@login_required(login_url='login')
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

@login_required(login_url='login')
def player(request, player_id):
    if request.method == 'POST':
        errmsg = None
        if request.user.player.id == int(player_id) or request.user.is_superuser:
            for field in request.POST:
                vals = field.split("_")
                if len(vals) == 2:
                    cmd, oid = vals
                    if cmd in ['up', 'down', 'remove', 'verify', 'new']:
                        orderMatch = MatchOrder.objects.get(pk=oid)
                        player = orderMatch.player
                        if cmd in ['up', 'down']:
                            switchmatchorder = orderMatch.order - 1 if cmd == 'up' else orderMatch.order + 1
                            switchmatches = MatchOrder.objects.filter(match__season=orderMatch.match.season,
                                                                      match__round=orderMatch.match.round,
                                                                      player=player,
                                                                      order=switchmatchorder)
                            if switchmatches.count() != 1:
                                break
                            switchmatch = switchmatches[0]
                            tmp = switchmatch.order
                            switchmatch.order = orderMatch.order
                            orderMatch.order = tmp
                            switchmatch.save()
                            orderMatch.save()
                        elif cmd == 'remove':
                            if orderMatch.match.verified or orderMatch.match.reporter != player:
                                break
                            otherOrderMatch = MatchOrder.objects.get(match=orderMatch.match, player=orderMatch.match.opponent)
                            match = orderMatch.match

                            # Save info for future use of adjusting ordering
                            otherPlayer = otherOrderMatch.player
                            order = orderMatch.order
                            otherOrder = otherOrderMatch.order
                            season = orderMatch.match.season
                            round = orderMatch.match.round

                            # Remove the ordered entries and the anchor entry
                            orderMatch.delete()
                            otherOrderMatch.delete()
                            match.delete()

                            # Now adjust order for all matches in round after one removed
                            for p in [player, otherPlayer]:
                                for o in MatchOrder.objects.filter(match__season=season, match__round=round, player=p, order__gt=order).order_by('order'):
                                    o.order-=1
                                    o.save()
                        elif cmd == 'verify':
                            if orderMatch.match.verified or orderMatch.match.reporter == player:
                                break
                            orderMatch.match.verified = True
                            orderMatch.match.save()
                    break
                elif len(vals) == 3:
                    cmd, season_id, round = vals
                    if cmd == 'new':
                        date = request.POST['new_%s_%s_playdate' % (season_id, round)]
                        opponent_id = request.POST['new_%s_%s_opponent' % (season_id, round)]
                        won = 'new_%s_%s_result' % (season_id, round) in request.POST
                        try:
                            addMatch(player_id, opponent_id, season_id, round, date, won)
                        except Exception as e:
                            errmsg="Error in input data: " + str(e)
                    break
        if errmsg:
            messages.error(request, errmsg)
        return redirect('/leaguematches/player/' + str(player_id))
    else:
        #[ [season1, [[round1, [matchlist], [round2, [matchlist]] ... ]]], season2, ...]
        player_matches = MatchOrder.objects.filter(player=player_id)
        view_matches = []
        for season in Season.objects.filter(player=player_id):
            season_matches = player_matches.filter(match__season=season.id)
            round_matches = []
            for round in season_matches.order_by('match__round').values_list('match__round',flat=True).distinct():
                round_matches += [round, season_matches.filter(match__round=round).order_by('order')],
            view_matches += [season, round_matches],

        opponents = Player.objects.exclude(id=player_id).order_by("user__first_name", "user__last_name")
        context = {'player': Player.objects.get(id=player_id),
                   'matches': view_matches,
                   'opponents': opponents,}
        return render(request, 'leaguematches/player.html', context)

def index(request):
    season_list = Season.objects.all();
    context = {'season_list': season_list}
    return render(request, 'leaguematches/index.html', context)

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            password_changed = False
            if form.cleaned_data['new_password'] != "" or form.cleaned_data['confirm_password'] != "":
                if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                    password_changed = True
                    request.user.set_password(form.cleaned_data['new_password'])
                else:
                    return render(request, 'leaguematches/profile.html', {'form': form, 'error_message': "Passwords don't match"})
            if request.user.username != form.cleaned_data['username']:
                request.user.username = form.cleaned_data['username']
            if request.user.email != form.cleaned_data['email']:
                request.user.email = form.cleaned_data['email']
            if request.user.first_name != form.cleaned_data['first_name']:
                request.user.first_name = form.cleaned_data['first_name']
            if request.user.last_name != form.cleaned_data['last_name']:
                request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            if password_changed:
                update_session_auth_hash(request, request.user)
            return redirect('/leaguematches/player/' + str(request.user.id))
    else:
        form = ProfileForm(initial={'username': request.user.username,
                                    'email': request.user.email,
                                    'first_name': request.user.first_name,
                                    'last_name': request.user.last_name})

    return render(request, 'leaguematches/profile.html', {'form': form})