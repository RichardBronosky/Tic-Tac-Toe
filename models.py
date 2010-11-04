from django.db import models
from django.http import HttpResponse, HttpResponseRedirect


class Board(models.Model):

	compwin=models.BooleanField(default=False)
	gamestarted=models.BooleanField(default=True)
	
	def Turn(self):
		oneone=Space.objects.get(posx=1, posy=1)
		onetwo=Space.objects.get(posx=1, posy=2)
		onethree=Space.objects.get(posx=1, posy=3)
		twoone=Space.objects.get(posx=2, posy=1)
		twotwo=Space.objects.get(posx=2, posy=2)
		twothree=Space.objects.get(posx=2, posy=3)
		threeone=Space.objects.get(posx=3, posy=1)
		threetwo=Space.objects.get(posx=3, posy=2)
		threethree=Space.objects.get(posx=3, posy=3)
		
		#first try to win
		
		if oneone.iso:
			if onetwo.iso and onethree.isempty: onethree.CompClicked()
			elif onethree.iso and onetwo.isempty: onetwo.CompClicked
			elif twotwo.iso and threethree.isempty: threethree.CompClicked()
			elif threethree.iso and twotwo.isempty: twotwo.CompClicked()
			elif twoone.iso and threeone.isempty: threeone.CompClicked()
			elif threeone.iso and twoone.isempty: twoone.CompClicked()
		elif onetwo.iso:
			if oneone.iso and onethree.isempty: onethree.CompClicked()
			elif onethree.iso and oneone.isempty: oneone.CompClicked
			elif twotwo.iso and threetwo.isempty: threetwo.CompClicked()
			elif threetwo.iso and twotwo.isempty: twotwo.CompClicked()
		elif onethree.iso:
			if twotwo.iso and threeone.isempty: threeone.CompClicked()
			elif threeone.iso and twotwo.isempty: twotwo.CompClicked()
			elif twothree.iso and threethree.isempty: threethree.CompClicked()
			elif threethree.iso and twothree.isempty: twothree.CompClicked()
		elif twoone.iso:
			if twotwo.iso and twothree.isempty: twothree.CompClicked()
			elif twothree.iso and twotwo.isempty: twotwo.CompClicked()
		elif twothree.iso:
			if onethree.iso and threethree.isempty: threethree.CompClicked()
			elif threethree.iso and twothree.isempty: twothree.CompClicked()
			elif twotwo.iso and twoone.isempty: twoone.CompClicked()
			elif twoone.isempty and twotwo.iso: twotwo.CompClicked()
		elif threeone.iso:
			if threetwo.iso and threethree.isempty: threethree.CompClicked()
			elif threethree.iso and threetwo.isempty: threetwo.CompClicked()
		
		# have we won?
		
		if oneone.iso and ((onetwo.iso and onethree.iso) or (twotwo.iso and threethree.iso) or (twoone.iso and threeone.iso)): self.Win()
		if onethree.iso and ((twotwo.iso and threeone.iso) or (twothree.iso and threethree.iso)): self.Win()
		if twotwo.iso and twoone.iso and twothree.iso: self.Win()
		if onetwo.iso and twotwo.iso and threetwo.iso: self.Win()
		if threeone.iso and threetwo.iso and threethree.iso: self.Win()	
		
		if self.compwin: return True
		# then react to player
		
		# if player holds center
		
		if twotwo.isx:
			if oneone.isx and threethree.isempty: threethree.CompClicked()
			elif onetwo.isx and threetwo.isempty: threetwo.CompClicked()
			elif onethree.isx and threeone.isempty: threeone.CompClicked()
			elif twoone.isx and twothree.isempty: twothree.CompClicked()
			elif twothree.isx and twoone.isempty: twoone.CompClicked()
			elif threeone.isx and onethree.isempty: onethree.CompClicked()
			elif threetwo.isx and onetwo.isempty: onetwo.CompClicked()
			elif threethree.isx and oneone.isempty: oneone.CompClicked()
			elif twoone.isx and twothree.isempty: twothree.CompClicked()
			elif oneone.isempty: oneone.CompClicked()
			elif onethree.isempty: onethree.CompClicked()
			elif threeone.isempty: threeone.CompClicked()
			elif threethree.isempty: threethree.CompClicked()
			elif onetwo.isempty: onetwo.CompClicked()
			elif twoone.isempty: twoone.CompClicked()
			elif twothree.isempty: twothree.CompClicked()
			elif threetwo.isempty: threetwo.CompClicked()
			return True
		
		# if computer holds center
		
		elif twotwo.iso:
			if (oneone.isx and onetwo.isx) or (twothree.isx and threethree.isx) and onethree.isempty: onethree.CompClicked()
			elif oneone.isx and onethree.isx and onetwo.isempty: onetwo.CompClicked()
			elif (oneone.isx and twoone.isx) or (threetwo.isx and threethree.isx) and threeone.isempty: threeone.CompClicked()
			elif oneone.isx and threeone.isx and twoone.isempty: twoone.CompClicked()
			elif onethree.isx and threethree.isx and twothree.isempty: twothree.CompClicked()
			elif (onetwo.isx and onethree.isx) or (twoone.isx and threeone.isx) and oneone.isempty: oneone.CompClicked()
			elif threeone.isx and threethree.isx and threetwo.isempty: threetwo.CompClicked()
			elif (threeone.isx and threetwo.isx) or (onethree.isx and twothree.isx) and threethree.isempty: threethree.CompClicked()
			elif oneone.isx and threethree.isx and onetwo.isempty: onetwo.CompClicked()
			elif oneone.isempty: oneone.CompClicked()
			elif onethree.isempty: onethree.CompClicked()
			elif threeone.isempty: threeone.CompClicked()
			elif threethree.isempty: threethree.CompClicked()
			elif onetwo.isempty: onetwo.CompClicked()
			elif twoone.isempty: twoone.CompClicked()
			elif twothree.isempty: twothree.CompClicked()
			elif threetwo.isempty: threetwo.CompClicked()
			
		elif twotwo.isempty: twotwo.CompClicked()
		

		
	def Win(self):
		self.compwin=True
		self.save()
		return HttpResponseRedirect('/tictactoe/')
	

	
class Space(models.Model):
	isempty=models.BooleanField(default=True)
	isx=models.BooleanField(default=False)
	iso=models.BooleanField(default=False)
	posx=models.IntegerField()
	posy=models.IntegerField()
	game=models.ForeignKey(Board)
	
	def PlayerClicked(self):
		self.isempty=False
		self.isx=True
		self.iso=False
		self.save()
	
	def CompClicked(self):
		self.isempty=False
		self.isx=False
		self.iso=True
		self.save()
		return HttpResponseRedirect('/tictactoe/')