from django.conf.urls import include, url
from django.contrib import admin

urlpatterns_prod = [
    url(r'', include('leaguematches.urls')),
]

urlpatterns_dev = [
    # Examples:
    # url(r'^$', 'magicleague.views.home', name='home'),
    url(r'^leaguematches/', include('leaguematches.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

# For some reason can't get this to work for both dev and not dev
urlpatterns = urlpatterns_prod