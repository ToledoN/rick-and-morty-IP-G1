# capa de vista/presentación

from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .layers.services import services


def index_page(request):
    return render(request, 'index.html')

def home(request):
    input_name = request.GET.get('name', '')
    current_page = int(request.GET.get('page', 1))
    
    try:
        context = services.get_home_context(request, input_name, current_page)
        return render(request, 'home.html', context)
    except Exception as e:
        messages.error(request, f"Error cargando datos de la página: {e}")
        return redirect('index')

def register_view(request):
    services.register(request)
    return render(request, 'registration/register.html')

@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list})

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect('home')


@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')
