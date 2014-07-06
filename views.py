from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from mysite.tictactoe.models import Space, Board
from django.template import RequestContext

def BuildSquares():
	squares=[]
	for each in Space.objects.all():
		if each.iso: squares.append('O')
		elif each.isx: squares.append('X')
		else: squares.append('empty')
	return squares

	
def index(request):
	squares=BuildSquares()
	message="Click Play to begin.  Click a checkbox to take Square.  You can try to click more checkboxes, you big cheater, but it won't work!!@!  Then click Play to Continue!@!"
	count=int(Board.objects.count())
	if count==0:
		new=Board()
		new.save()
		for x in xrange(1,4):
			for y in xrange(1,4):
				newspace=Space(game=new, posx=x, posy=y)
				newspace.save()
	else:
		for each in Board.objects.all():
			if each.compwin: 
				endgame()
				message="You Lose!!!  How could you lose at Tic Tac Toe?  Would you like to play Global Thermonuclear War instead?  (Or click Play to try again)"
				for x in xrange(0,9):
					if squares[x]=='empty': squares[x]='NULL'
				return render_to_response('tictactoe/index.html', {'spaces':squares, 'message':message},context_instance=RequestContext(request))
		counter=0
		for each in Space.objects.all():
			if each.isempty: counter+=1
		if counter==0:
			endgame()
			message="Another Tie.  Would you like to play Global Thermonuclear War instead? (Or click Play to try again)"
	return render_to_response('tictactoe/index.html', {'spaces':squares, 'message':message},context_instance=RequestContext(request))

def processmove(request):
	x=1
	y=1
	for z in xrange(1,10):
		string='button'+str(z)
		if request.POST.get(string)=='Take':
			check=Space.objects.get(posx=x, posy=y)
			check.PlayerClicked()
			for each in Board.objects.all():
				each.Turn()
			return HttpResponseRedirect('/tictactoe')
		if y==3:
			y=1
			x+=1
		else: y+=1		
	return HttpResponseRedirect('/tictactoe/')

	
def endgame():
	#will completely clear both database tables
	for each in Space.objects.all(): each.delete()
	for each in Board.objects.all(): each.delete()
	return True