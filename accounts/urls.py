from django.conf.urls import patterns, url

import accounts.views
import django.contrib.auth.views


urlpatterns = [
	url(r'^login$', accounts.views.persona_login, name='persona_login'),
	url(r'^logout$', django.contrib.auth.views.logout, {'next_page': '/'}, name='logout')
]