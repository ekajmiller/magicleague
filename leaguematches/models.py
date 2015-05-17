from django.db import models
from django.contrib.auth.models import User

class Season(models.Model):
    name = models.CharField(max_length=50, unique=True)

    # As a convenience you can't add matches for > than the current round
    current_round = models.PositiveIntegerField(default=1)

    # If closed then no more matches can be input
    closed = models.BooleanField(default=False)

    # NegTieBreakLosses: MP (first 5 matches), 3 for Win, 1 For Loss. TB, 2 for win, -1 for loss, can't go below 0 (order matters)
    # Simple: MP (first 5 matches), 4 for Win, 2 for Loss, 1 for Tie. TB, 
    calcmethod = models.CharField(max_length=30, choices = [('NegTieBreakLosses', "Negative Tie Breaker Points for Losses"),
                                                           ('Simple', "Regular scoring where order of matches doesn't matter for tiebreakers")],
                                                           default='Simple')
    
    def __unicode__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User)
    seasons = models.ManyToManyField(Season, blank=True)

    def __unicode__(self):
        return self.user.get_full_name()

class MatchReport(models.Model):
    reporter = models.ForeignKey(Player, related_name='+')
    opponent = models.ForeignKey(Player, related_name='+')
    winner = models.ForeignKey(Player, related_name='+')
    loser = models.ForeignKey(Player, related_name='+')
    round = models.PositiveIntegerField(choices = (map(lambda x: (x, 'Round ' + str(x)), range(1,6))))
    season = models.ForeignKey(Season)
    report_date = models.DateTimeField()
    played_date = models.DateField()
    win = models.BooleanField(choices = ((True, 'Win'), (False, 'Loss')))
    verified = models.BooleanField()

    def __unicode__(self):
        return self.played_date.strftime("%Y-%m-%d") + ': ' + \
               str(self.winner) + ' beat ' + str(self.loser)

    class Meta:
        ordering = ['round', 'played_date', 'report_date']
        unique_together = ('played_date', 'reporter', 'opponent')

class MatchOrder(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(MatchReport)
    order = models.IntegerField()

    def __unicode__(self):
        return str(self.match)

    class Meta:
        unique_together = ('player', 'match')
