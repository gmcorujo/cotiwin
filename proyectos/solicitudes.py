# -*- coding: latin-1 -*-
from hashlib import md5

from django.shortcuts import render, redirect
from django.contrib.auth.models import User,Group
from proyectos.models import *

from app.views import baseContext
from app.mail import send_smtp_mail

# Create your views here.

def hashPassword(email):
	h = md5(email)
	o = h.hexdigest()
	return o[:10]

def addClient(p):
	cliente_group = Group.objects.get(name="cliente")
	has_fields = (
		p.has_key('nombre'),
		p.has_key('apellido'),
		p.has_key('email')
		)
	if not (False in has_fields):
		u = User()
		u.first_name = p['nombre']
		u.last_name = p['apellido']
		u.username = u.email = p['email']
		u.set_password(hashPassword(p['email']))
		print hashPassword(p['email'])
		u.is_staff = False
		u.is_active = False
		
		try:
			u.save()
			h = md5(u.email)
			c = Cliente(user = u, confirm = h.hexdigest())
			c.clean_fields()
			c.save(force_insert=True)
			cliente_group.user_set.add(u)
			return u
		except:
			return False
	else:
		return False

def addSolicitud(user,p):
	has_fields = (
		p.has_key('descripcion'),
		p.has_key('pais'),
		p.has_key('categoria'),
		p.has_key('plazo')
		)
	if not (False in has_fields):
		s = Solicitud()
		s.user = user
		categoria = Categoria.objects.get(id=int(p['categoria']))
		s.categoria = categoria
		pais = Pais.objects.get(id=p['pais'])
		s.pais = pais
		plazo = p['plazo']
		plazo = "%s-%s-%s %s" % (plazo[6:10],plazo[3:5],plazo[:2],plazo[11:])
		s.plazo = plazo
		s.description = p['descripcion']

		if not user.is_active:
			s.enabled = False
		else:
			s.enabled = True

		try:
			s.clean_fields()
			s.clean()
			s.save()
		except:
			s = False
		return s

def sendEmailNewUserNotification(u,s):
	c = Cliente.objects.get(user=u)
	msj = u'''
FELICITACIONES %s !!!
Te has registrado en CotiWin y has creado una nueva solicitud de cotizacion:
DESCRIPCION:
%s
TU CLAVE: %s
activa tu cuenta yendo al siguiente enlace %sproyectos/activate/%s/%s/
		''' % (u.first_name,s.description,hashPassword(u.email),HOST_NAME,u.id,c.confirm)
	send_smtp_mail(msj,[u.email])

def sendEmailNewSolicitudNotification(u,s):
	msj = u'''
	%s HAS AÑADIDO UNA NUEVEA SOLICITUD DE COTIZACION !!
	DESCRIPCION:
	%s
		''' % (u.first_name,s.description)
	send_smtp_mail(msj,[u.email])

def waiting(request):
	solicitudes = Solicitud.objects.extra(where=["EXTRACT(EPOCH FROM age(NOW(),created)) < 1200"]).all().filter(enabled=True).order_by('-created')[:10]
	cxt = baseContext(request)
	cxt["right_section"] = "/proyectos/waiting/"
	cxt.update({'solicitudes':solicitudes})
	return render(request,'proyectos/waiting.html',cxt)

def sucessful(request):
	solicitudes = Solicitud.objects.extra(where=["EXTRACT(EPOCH FROM age(NOW(),created)) > 1200"]).all().filter(enabled=True).order_by('-created')[:10]
	cxt = baseContext(request)
	cxt["right_section"] = "/proyectos/sucessful/"
	cxt.update({'solicitudes':solicitudes})
	return render(request,'proyectos/sucessful.html',cxt)


def list(request, user_id):
	pass

def add(request):
	post = request.POST
	if not request.user.is_authenticated():
		u = addClient(post)
	else:
		u = request.user
	if not u.is_active:
		s = addSolicitud(u,post)
		if s:
			sendEmailNewUserNotification(u,s)
	else:
		s = addSolicitud(u,post)
		if s:
			sendEmailNewSolicitudNotification(u,s)

	cxt = baseContext(request)
	cxt.update({'post':request.POST})
	if s:
		if not u.is_authenticated():
			return render(request,'proyectos/sucess.html',cxt)
		else:
			return redirect("/proyectos/waiting/")
	else:
		cxt['right_section'] = "#"
		return render(request,'proyectos/fail.html',cxt)

def activateAccount(request,user_id ,confirm):
	try:
		u = User.objects.get(id=user_id)
		c = Cliente.objects.get(user = u)
	except:
		u = False
	if not u.is_active:
		if c.confirm == confirm:
			if u:
				u.is_active = True
				u.save()
				Solicitud.objects.all().filter(user = u).update(enabled=True,created=datetime.now())
				return redirect('/login/')
	else:
		return redirect("/")

def edit(request, id):
	pass

def delete(request, id):
	pass