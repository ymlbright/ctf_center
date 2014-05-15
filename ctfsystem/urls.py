from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

url_prefix = r'^ctf/'
admin_perfix = url_prefix + r'adminadminadmin/'

urlpatterns = patterns('',
   # Examples:
    # url(r'^$', 'ctfsystem.views.home', name='home'),
    # url(r'^ctfsystem/', include('ctfsystem.foo.urls')),
    url(url_prefix+r'$','usr.views.index'),
    url(url_prefix+r'index$','usr.views.index'),
	url(url_prefix+r'scoreboard$','usr.views.scoreboard'),
	url(url_prefix+r'notice$','usr.views.notice'),
	url(url_prefix+r'signin$','usr.views.signin'),
	url(url_prefix+r'login$','usr.views.login'),
	url(url_prefix+r'logout$','usr.views.logout'),
	url(url_prefix+r'register$','usr.views.register'),
	url(url_prefix+r'reg$','usr.views.reg'),
	url(url_prefix+r'flag$','usr.views.flag'),
	url(url_prefix+r'myscore$','usr.views.myscore'),
	url(url_prefix+r'question/(?P<id>[0-9]{1,})$','usr.views.detial'),

	url(url_prefix+r'(?P<type>[a-z]{1,10})$','usr.views.question'),

	url(admin_perfix+r'$','admin.views.signin'),
	url(admin_perfix+r'login$','admin.views.login'),
	url(admin_perfix+r'user$','admin.views.user'),
	url(admin_perfix+r'question$','admin.views.question'),
	url(admin_perfix+r'notice$','admin.views.notice'),
	url(admin_perfix+r'notice/add$','admin.views.notice_add'),
	url(admin_perfix+r'notice/del/(?P<id>[0-9]{1,})$','admin.views.notice_del'),
	url(admin_perfix+r'edit/(?P<id>[0-9]{1,})$','admin.views.edit'),
	url(admin_perfix+r'edit','admin.views.editq'),
	url(admin_perfix+r'del/(?P<id>[0-9]{1,})$','admin.views.delq'),
	url(admin_perfix+r'delu/(?P<id>[0-9]{1,})$','admin.views.delu'),
	url(admin_perfix+r'lock/(?P<id>[0-9]{1,})$','admin.views.lock'),
	url(admin_perfix+r'unlock/(?P<id>[0-9]{1,})$','admin.views.unlock'),
	url(admin_perfix+r'logout$','admin.views.logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    #url(url_prefix+r'admin/', include(admin.site.urls)),
)
