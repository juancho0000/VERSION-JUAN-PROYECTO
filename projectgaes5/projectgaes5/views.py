from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from index.forms import CustomUserCreationForm 
from django.http import HttpResponse
from django.views import View
from xhtml2pdf import pisa
from django.template.loader import get_template
from index.models import Garantia

def serviceprod(request):
    return render(request, 'serviceprod.html', {})

class ReporteGarantiaPDF(View):
    def get(self, request, *args, **kwargs):
        # Obtener parámetros de filtro desde la solicitud
        fecha_vencimiento = request.GET.get('fecha_vencimiento', None)
        estados = request.GET.get('estados', None)

        # Construir la consulta de base de datos con los filtros aplicados
        queryset = Garantia.objects.all()
        if fecha_vencimiento:
            queryset = queryset.filter(fecha_vencimiento=fecha_vencimiento)
        if estados:
            queryset = queryset.filter(estados=estados)

        # Obtener todas las garantías según los filtros aplicados
        garantias = queryset

        # Cargar la plantilla HTML
        template_path = 'reporte-garantias-pdf.html'  # Asegúrate de que coincida con el nombre de tu template
        template = get_template(template_path)
        context = {'garantias': garantias}

        # Crear el objeto HttpResponse con las cabeceras de PDF adecuadas.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="informe_garantias.pdf"'

        # Generar el PDF utilizando xhtml2pdf
        pisa_status = pisa.CreatePDF(template.render(context), dest=response)

        # Si el PDF se generó correctamente, devuelve la respuesta
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        return response
    
def index(request):
    return render(request, 'index.html', {})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

    return render(request, 'login.html', {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('admin:index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión finalizada')
    return redirect('login')


