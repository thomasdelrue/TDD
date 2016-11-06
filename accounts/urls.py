from django.conf.urls import patterns, url

import accounts.views

urlpatterns = [
	url(r'^login$', accounts.views.persona_login, name='persona_login'),
]