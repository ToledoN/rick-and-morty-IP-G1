# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services.services import getAllImages  # Asegúrate de importar correctamente
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
#Esto es para la paginacion
def home(request):
    input_name = request.GET.get('name', '')  # Obtener el término de búsqueda si existe
    page = int(request.GET.get('page', 1))    # Obtener el número de página desde la URL, o por defecto 1

    images, page_info = getAllImages(input_name, page)  # Obtener imágenes y paginación

    # Generar la lista de páginas basándonos en el total de páginas
    total_pages = page_info.get('pages', 1)
    pages = list(range(1, total_pages + 1))

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': [],  # Aquí podrías agregar lógica para favoritos si fuera necesario
        'pages': pages,         # Lista de páginas
        'current_page': page,   # Página actual
        'input_name': input_name  # Término de búsqueda para conservar en el paginador
    })
















def index_page(request):
    return render(request, 'index.html')

# Esta función obtiene los listados de imágenes de la API y los usa para dibujar el template.
def home(request):
    input_name = request.GET.get('name', '')  # Obtener el nombre desde el query string
    current_page = int(request.GET.get('page', 1))  # Obtener el número de página, con valor predeterminado 1
    
    # Llama a la función para obtener las imágenes y total de páginas
    images, total_pages = getAllImages(input_name, current_page)
    
    # Genera el rango de páginas (esto es solo para mostrar un máximo de 10 páginas en el paginador)
    page_range = range(1, min(total_pages, 10) + 1)

    # Crear una lista vacía para los favoritos (esto se puede actualizar según la lógica de favoritos)
    favourite_list = []  # Aquí puedes agregar la lógica para obtener favoritos si lo deseas

    # Pasar las variables necesarias al template
    context = {
        'images': images,
        'favourite_list': favourite_list,
        'current_page': current_page,
        'total_pages': total_pages,
        'page_range': page_range,
        'name': input_name,
    }

    return render(request, 'home.html', context)

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            
            # Enviar correo de bienvenida
            send_mail(
                'Registro Exitoso',
                f'Tus credenciales de acceso son:\nUsuario: {username}\nContraseña: {password}',
                'noreply@tuapp.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Usuario registrado exitosamente. Revisa tu correo electrónico para tus credenciales.')
            return redirect('login')
    
    return render(request, 'registration/register.html')

def search(request):
    search_msg = request.POST.get('query', '')

    if search_msg != '':
        # Aquí puedes implementar la lógica para buscar imágenes si lo deseas.
        # Por ahora, redirigimos a la vista home con el query como parámetro.
        return redirect('home')  # Cambia esto para que incluya el nombre en la URL
    else:
        return redirect('home')

# Funciones que se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')
