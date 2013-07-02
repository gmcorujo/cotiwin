
from django.shortcuts import render, redirect

from app.settings import SMTP_USER, SMTP_PASSWORD, HOST_NAME
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.contrib.auth.models import User
from proyectos.models import *

from app.views import baseContext
from hashlib import md5
# Create your views here.

def hashPassword(email):
	h = md5(email)
	o = h.hexdigest()
	return o[:10]

def addClient(p):
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

		if not user.is_authenticated():
			s.enabled = False
		else:
			s.enabled = True

		s.clean_fields()
		s.clean()
		s.save()
		return s

def send_email_notif(u,s):
	gmail_user = SMTP_USER
	gmail_pwd = SMTP_PASSWORD 
	msj = MIMEMultipart('alternative')
	
	msj['FROM'] = gmail_user
	msj['Subjent'] = "cotiwin"
	c = Cliente.objects.get(user=u)
	m = u"""
FELICITACIONES %s !!!
Te has registrado en CotiWin y has creado una nueva solicitud de cotizacion:
DESCRIPCION:
%s
TU CLAVE: %s
activa tu cuenta yendo al siguiente enlace %sproyectos/activate/%s/%s/
		""" % (u.username,s.description,hashPassword(u.email),HOST_NAME,u.id,c.confirm)
	msj.attach(MIMEText(m, 'html', 'UTF-8'))
	smtpserver = SMTP("smtp.gmail.com",587) 
	smtpserver.ehlo() 
	smtpserver.starttls() 
	smtpserver.ehlo()
	smtpserver.login(gmail_user, gmail_pwd) 
	smtpserver.sendmail(gmail_user, u.email, msj.as_string())
	smtpserver.close()



def waiting(request):
	solicitudes = Solicitud.objects.extra(where=["EXTRACT(EPOCH FROM age(NOW(),created)) < 1200"]).all().filter(enabled=True).order_by('-created')
	cxt = baseContext(request)
	cxt["right_section"] = "/proyectos/waiting/"
	cxt.update({'solicitudes':solicitudes})
	return render(request,'proyectos/waiting.html',cxt)

def sucessful(request):
	solicitudes = Solicitud.objects.extra(where=["EXTRACT(EPOCH FROM age(NOW(),created)) > 1200"]).all().filter(enabled=True).order_by('-created')
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
	if u:
		s = addSolicitud(u,post)
		send_email_notif(u,s)

	cxt = baseContext(request)
	cxt.update({'post':request.POST})
	if not u.is_authenticated():
		return render(request,'proyectos/sucess.html',cxt)
	else:
		return redirect("/proyectos/waiting/")

def activateAccount(request,user_id ,confirm):
	try:
		u = User.objects.get(id=user_id)
		c = Cliente.objects.get(user = u)
	except:
		u = False
	if u:
		if c.confirm == confirm:
			if u:
				u.is_active = True
				u.save()
				Solicitud.objects.all().filter(user = u).update(enabled=True)
				return redirect('/login/')
	else:
		return redirect("/")

def edit(request, id):
	pass

def delete(request, id):
	pass