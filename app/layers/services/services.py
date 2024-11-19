# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from ..transport import transport
from django.contrib.auth import get_user
import requests
from ..utilities import card
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail


def getAllImages(input=None, page=1):
    
    images, total_pages = transport.getAllImages(input, page)
    images = [
    {
        'image': img.url,
        'name': img.name,
        'status': img.status,
        'location': img.last_location,
        'first_episode': img.first_seen,
    }
    for img in images
    ]
    return list(images), total_pages

def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request)
    fav.user = get_user(request)
    return repositories.saveFavourite(fav)

def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(user)
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRepositoryIntoCard(favourite)
            mapped_favourites.append(card)
        return mapped_favourites

def getFavs(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavourites(user)
        return favourite_list

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            send_mail(
                'Registro Exitoso',
                f'Tus credenciales de acceso son:\nUsuario: {username}\nContraseña: {password}',
                'noreply@tuapp.com',
                [email],
                fail_silently=False,
            )
            return messages.success(request, 'Usuario registrado exitosamente. Revisa tu correo electrónico para tus credenciales.')
        messages.error(request, 'Error al registrar.')

    