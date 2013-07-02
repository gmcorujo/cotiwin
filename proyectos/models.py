import time
from datetime import datetime, timedelta
import calendar
from django.contrib.auth.models import User
from django.db.models import Model, CharField,ForeignKey,TextField, FileField
from django.db.models import DateTimeField, ManyToManyField, BooleanField

class Aptitud(Model):
	short = CharField(max_length = 64)
	descrption = TextField()

	def __unicode__(self):
		return self.short

class Categoria(Model):
	short = CharField(max_length = 64)
	descrption = TextField()

	def __unicode__(self):
		return self.short

class Pais(Model):
	nombre = CharField(max_length = 200)

	def __unicode__(self):
		return self.nombre

class Cliente(Model):
	user = ForeignKey(User)
	confirm = CharField(max_length=200)

class Solicitud(Model):
	user = ForeignKey(User)
	categoria = ForeignKey(Categoria)
	#aptitudes = ManyToManyField(Aptitud)
	pais = ForeignKey(Pais)
	description = TextField()
	plazo = DateTimeField()
	adjunto = FileField(upload_to="adjuntos/",blank=True)
	enabled = BooleanField(default=False)
	created = DateTimeField(auto_now=True, auto_now_add=True)

	def time_left(self):
		tup =self.created.utctimetuple()
		now = datetime.now().utctimetuple()
		created_stamp = calendar.timegm(tup)
		now_stamp = calendar.timegm(now)
		left = (now_stamp+10797) - created_stamp
		return int(left)


class Requerimientos(Model):
	solicitud = ForeignKey(Solicitud)
	descrption = CharField(max_length= 250)

	
