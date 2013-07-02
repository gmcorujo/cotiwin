from django.contrib.auth.models import User
from django.db.models import Model, ForeingKey, DecimalField, DateTimeField
from django.db.models import CharField, ManyToManyField, IntegerField

from proyectos.modes import Categoria,Pais, Solicitud


class Cotizador(Model):
	user = ForeingKey(User)
	pais = ForeingKey(Pais)
	categorias = ManyToManyField(Categoria)
	#aptitudes = ManyToManyField(Aptitud)

class Points(Model):
	from_user = ForeingKey(User)
	to_user = ForeingKey(User)
	cant = IntegerField()

class State():
	name = CharField(max_length = 64)

	def __unicode__(self):
		return self.name

class Cotizacion(Model):
	user = ForeingKey(User)
	solicitud = ForeingKey(Solicitud)
	state = ForeingKey(State)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	deliver_date = DatetimeField()
	created = DatetimeField(auto_now=False,auto_now_add=True)
