# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests

# Definimos la URL base de la API de Rick & Morty
BASE_URL = "https://rickandmortyapi.com/api/character/"

def getAllImages(input=None, page=1):
    """
    Obtiene un listado de datos "crudos" desde la API, usando la URL base.
    Si se pasa un input, filtra los resultados por nombre.
    """
    url = BASE_URL
    params = {'page': page}
    if input:
        params['name'] = input  # Agregar el filtro por nombre

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Verificar si la respuesta fue exitosa
        data = response.json()       # Obtener el JSON de la respuesta

        # Acceder a la lista de personajes y transformar en lista de imágenes
        characters = data.get("results", [])
        total_pages = data.get("info", {}).get("pages", 1)  # Obtener el número total de páginas

    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return [], 1  # Devolver una lista vacía y 1 página si ocurre un error

    # Procesar y devolver los datos en un formato adecuado para el template
    images = [
        {
            "name": char["name"],
            "image": char["image"],
            "status": char["status"],
            "location": char["location"]["name"],
            "first_episode": char["episode"][0]  # Solo el primer episodio
        }
        for char in characters
    ]
    return images, total_pages

# Añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request del template en una Card.
    fav.user = '' # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(fav) # lo guardamos en la base.

# Usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.