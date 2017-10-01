from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import string

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    validated = models.BooleanField()

class Slot(models.Model):
	name = models.CharField(max_length=20)
	shortname = models.CharField(max_length=3)
	num = models.IntegerField(primary_key=True)

	def __str__(self):
		return "{0} [{1}]".format(self.name,self.num)

	def size():
		return len(Slot.object.all())

class Tag(models.Model):
	name = models.CharField(max_length=20)
	link = models.CharField(max_length=16, unique=True)
	description = models.CharField(max_length=1024,null=True,blank=True)
	keywords = models.CharField(max_length=1024,null=True)
	asked = models.ForeignKey(User,null=True,blank=True)

	def __str__(self):
		return (("Système:") if self.special() else "" ) +self.name

	def validated(self):
		return asked == None

	def special(self):
		return hasattr(self,"system") or hasattr(self, "game")

	def modelName(self=None):
		return ""

	def make_link(self):
		transation=self.name.lower().replace(' ','-').replace('é','e').replace('è','e')
		return [x for x in transation if x in "abcdefghijklmnopqrstuvwxyz-_"]

class System(Tag):
	perso = models.BooleanField()

	def __str__(self):
		return self.name

	def modelName(self=None):
		return "System"

class State(models.Model):
	name = models.CharField(max_length=20)
	canjoinfreely = models.BooleanField()
	couldjoin = models.BooleanField()
	active = models.BooleanField()
	show = models.BooleanField()
	done = models.BooleanField()

	def searchable(self):
		return show and not(done)

	def joinable(self):
		return canjoinfreely or couldjoin

	def __str__(self):
		return self.name

class Activity(models.Model):
	name = models.CharField(max_length=60)
	organiser = models.ForeignKey(User)
	slots = models.ManyToManyField(Slot,blank=True,related_name="organising")
	tags = models.ManyToManyField(Tag,blank=True)
	description = models.CharField(max_length=8192)
	players = models.ManyToManyField(User,related_name="playing",through="PlayerRequest")
	minimum = models.IntegerField(default=3)
	maximum = models.IntegerField(default=5)

	def __str__(self):
		return "{0} ({1})".format(self.name,self.organiser)

	def playerBar(self): #TODO
		n_playing = len(self.players.filter(playerrequest__accepted=True))
		maximum = max(self.maximum,n_playing)
		if(n_playing>=self.minimum):
			bar = {
				'type':2,
				'green':int(self.minimum/maximum*100),
				'blue':int((n_playing-minimum)/maximum*100),
			}
			if(n_playing>=maximum):
				bar['flavor']="complet"
			else:
				bar['msg']="({0} dispo)".format(maximum-n_playing)
		else:
			bar = {
				'type':1,
				'green':int(n_playing/self.minimum*100),
			}
			if(n_playing<self.minimum):
				bar['msg']="(encore {0})".format(self.minimum-n_playing)
		bar['playing']=n_playing
		return bar

	def userTag(self,user):
		if user==self.organiser:
			t = "danger"
			i = "MJ"
		else:
			rel = PlayerRequest.objects.filter(user=user,activity=self)
			if rel:
				if rel[0].accepted:
					t = "success"
					i = "Joueur"
				else:
					t = "warning"
					i = "Demande en cours"
			else:
				t = ""
				i = ""
		return {'type':t,'info':i}

	def normalTags(self):
		return self.tags.filter(system__isnull=True)

	def systemTags(self):
		return self.tags.filter(system__isnull=False)

class PlayerRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    accepted = models.BooleanField()