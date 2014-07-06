


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from mysite.tttoe.models import Space, Board
from django.template import RequestContext
import random

def BuildSquares():
	squares=[]
	for each in Space.objects.all():
		if each.iso: squares.append('O')
		elif each.isx: squares.append('X')
		else: squares.append('empty')
	return squares

	
def index(request):
	results=[]
	for n in xrange(0,100):
		moves=''
		squares=BuildSquares()
		new=Board()
		new.save()
		for x in xrange(1,4):
			for y in xrange(1,4):
				newspace=Space(game=new, posx=x, posy=y)
				newspace.save()
		while True:
			value=False
			for each in Board.objects.all(): 
				if each.compwin==True: 
					value=True
					endgame()
			if value: break		
			counter=0
			for each in Space.objects.all():
				if each.isempty: counter+=1
			if counter==0:
				if checkwin(): 
					if moves not in results: results.append(moves)
				endgame()
				break
			while True:
				ran1=random.randint(1,3)
				ran2=random.randint(1,3)
				check=Space.objects.get(posx=ran1, posy=ran2)
				if check.isempty: 
					check.PlayerClicked()
					moves+='P'+' '+str(ran1)+str(ran2)+' '
					break
			for each in Board.objects.all():
				each.Turn()
	return render_to_response('tttoe/test.html', {'wins':results})

	
def endgame():
	#will completely clear both database tables
	for each in Space.objects.all(): each.delete()
	for each in Board.objects.all(): each.delete()
	return True
	
def checkwin():
	
	#finished board
	
	oneone=Space.objects.get(posx=1, posy=1)
	onetwo=Space.objects.get(posx=1, posy=2)
	onethree=Space.objects.get(posx=1, posy=3)
	twoone=Space.objects.get(posx=2, posy=1)
	twotwo=Space.objects.get(posx=2, posy=2)
	twothree=Space.objects.get(posx=2, posy=3)
	threeone=Space.objects.get(posx=3, posy=1)
	threetwo=Space.objects.get(posx=3, posy=2)
	threethree=Space.objects.get(posx=3, posy=3)

	#did player beat computer
	
	if oneone.isx and ((onetwo.isx and onethree.isx) or (twotwo.isx and threethree.isx) or (twoone.isx and threeone.isx)): return True
	if onethree.isx and ((twotwo.isx and threeone.isx) or (twothree.isx and threethree.isx)): return True
	if twotwo.isx and twoone.isx and twothree.isx: return True
	if onetwo.isx and twotwo.isx and threetwo.isx: return True
	if threeone.isx and threetwo.isx and threethree.isx: return True
		
	return False