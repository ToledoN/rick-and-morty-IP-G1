# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from ..transport import transport
from django.contrib.auth import get_user
from ...config import config
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail


def getAllImages(input=None, page=config.DEFAULT_PAGE):
    
    if page < 1:
        page = config.DEFAULT_PAGE
        
    if input is not None:
        input = input.strip()
        
    try:
        characters, total_pages = transport.getAllImages(input, page)
        imageCards = []
        
        for character in characters:
            try:
                characterCard = translator.fromRequestIntoCard(character)
                imageCards.append(characterCard)
            except KeyError as e:
                print(f"[services.py]: Error al procesar datos del personaje: {e}")
                continue
            
        return imageCards, total_pages
    
    except Exception as e:
            print(f"[services.py]: Error al obtener datos de la API: {e}")
            return [], 0

def get_home_context(request, input_name, current_page):
    images, total_pages = getAllImages(input_name, current_page)
    page_range = range(1, min(total_pages, 10) + 1)
    
    favourite_list = getAllFavourites(request)
    favourite_names = [fav.name for fav in favourite_list]
    
    return {
        'images': images,
        'favourite_list': favourite_names,
        'current_page': current_page,
        'total_pages': total_pages,
        'page_range': page_range,
        'name': input_name,
    }

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

    