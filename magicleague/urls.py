from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'magicleague.views.home', name='home'),
    url(r'^leaguematches/', include('leaguematches.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
