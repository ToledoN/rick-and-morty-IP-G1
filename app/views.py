# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services.services import getAllImages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .layers.services import services


def index_page(request):
    return render(request, 'index.html')

def home(request):
    input_name = request.GET.get('name', '')
    current_page = int(request.GET.get('page', 1))
    
    images, total_pages = getAllImages(input_name, current_page)
    page_range = range(1, min(total_pages, 10) + 1)

    favourite_list = services.getFavs(request)
    favourite_names = [fav['name'] for fav in favourite_list]
    
    context = {
        'images': images,
        'favourite_list': favourite_names,
        'current_page': current_page,
        'total_pages': total_pages,
        'page_range': page_range,
        'name': input_name,
    }
    return render(request, 'home.html', context)

def register_view(request):
    services.register(request)
    
    return render(request, 'registration/register.html')

def search(request):
    search_msg = request.POST.get('query', '')

    if search_msg != '':
        return redirect('home')
    else:
        return redirect('home')

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
