from django.conf.urls.defaults import *
from django.contrib import admin
from tst.main.models import content
from django.contrib.auth.views import login, logout
from tst.feeds import LastEntries, CategoryLastEntries
from django.contrib.syndication.feeds import Feed

admin.autodiscover()

feeds = {'latest': LastEntries,
         'category': CategoryLastEntries}

urlpatterns = patterns("",
    (r"^$", "tst.main.views.main"),
    (r'^id(?P<ID>[\d]+)$', 'tst.main.views.view_content'),
    (r'^category/(?P<category>[^/]+)$', 'tst.main.views.category_views'),
    (r'category/(?P<category>[^/]+)/(?P<name>[^/]+)', 'tst.main.views.category_content'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^accounts/login$', login),
    (r'^accounts/logout$', logout),
    (r'^login$', 'tst.main.views.login'),
    (r'^search/', 'tst.main.views.search_all'),
    (r'^test/([\w]+)', 'tst.main.views.test'),
    (r'^admin/(.*)', admin.site.root),
    (r'^commentdel/(?P<ID>[\d]+)$', 'tst.main.views.del_comment'),
    (r"^id([\d]+)/add$", "tst.main.views.add"),
    (r'^openid/login$', 'tst.main.views.login_openid'),
    (r'^openid/test$', 'tst.main.views.auth_openid'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
        {'feed_dict': feeds}),
)

