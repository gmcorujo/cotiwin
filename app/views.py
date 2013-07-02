from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from proyectos.models import Pais, Categoria

def s(url, display):
	return {"url":url,"display":display}
	
def baseContext(request):
	base = {
	'menu':[
			s("/","home"),
			s("/plataforma/","plataforma"),
			s("/proyectos/mi/","mis cotizaciones")
			],
	'section':"/",
	"right_column_menu":[
						s("/","Nueva Cotizacion"),
						s("/proyectos/waiting/","Cotizaciones en Espera"),
						s("/proyectos/sucessful/","Cotizaciones Exitosas")
						],
	"right_section":"/",
	}
	return base.copy()

def loginUser(request):
	cxt = baseContext(request)
	cxt["right_section"] = None
	if not request.user.is_authenticated():
		if request.POST:
			p = request.POST
			has_fields = (p.has_key("email"),p.has_key('password'))
			if not False in has_fields:
				user = authenticate(username=p['email'],password=p['password'])
				if user.is_active:
					login(request, user)
				return redirect("/")
			else:
				return render(request,'app/login.html',cxt)	
		else:
			return render(request,'app/login.html',cxt)
	else:
		return redirect("/")

def logoutUser(request):
	if request.user.is_authenticated():
		logout(request)
	return redirect("/")

def home(request):
	paises = Pais.objects.all()
	categorias = Categoria.objects.all()
	cxt = baseContext(request)
	cxt.update({'paises':paises, 'categorias': categorias })
	return render(request,"app/home.html",cxt)