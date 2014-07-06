from django.conf.urls.defaults import *

urlpatterns = patterns('mysite.tictactoe.views',
	('^$', 'index'),
	('^processmove/$', 'processmove'),
	('^BuildSquares/$', 'BuildSquares'),
	('^endgame/$', 'endgame'),
)
