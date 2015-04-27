from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Season(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Player(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    seasons = models.ManyToManyField(Season, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        ordering = ['first_name', 'last_name']

class MatchReport(models.Model):
    reporter = models.ForeignKey(Player, related_name='+')
    opponent = models.ForeignKey(Player, related_name='+')
    round = models.PositiveIntegerField(choices = (map(lambda x: (x, 'Round ' +                                               str(x)), range(1,6))))
    season = models.ForeignKey(Season)
    report_date = models.DateTimeField()
    played_date = models.DateField()
    win = models.BooleanField(choices = ((True, 'Win'), (False, 'Loss')))
    verified = models.BooleanField()

    def victor(self):
        return self.reporter if self.win else self.opponent
    
    def loser(self):
        return self.reporter if not self.win else self.opponent

    def __unicode__(self):
        return self.played_date.strftime("%Y-%m-%d") + ' Round ' + \
               str(self.round) + ': ' + str(self.victor()) + ' beat ' + \
               str(self.loser())

    class Meta:
        ordering = ['round', 'played_date', 'report_date']
        unique_together = ('played_date', 'reporter', 'opponent')
