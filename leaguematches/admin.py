from django.contrib import admin

from .models import Player
from .models import Season
from .models import MatchReport
from .models import MatchOrder

admin.site.register(Player)
admin.site.register(Season)
admin.site.register(MatchReport)
admin.site.register(MatchOrder)