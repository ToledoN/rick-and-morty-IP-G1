# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config

# comunicación con la REST API.
# este método se encarga de "pegarle" a la API y traer una lista de objetos JSON crudos (raw).
def getAllImages(input, page):
    
    url = config.BASE_URL
    params = {'page': page}
    if input:
        params['name'] = input

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        characters = data.get("results", [])
        total_pages = data.get("info", {}).get("pages", 1)
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return [], 1

    images = []
    
    for object in characters:
        try:
            if 'image' in object:
                images.append(object)
            else:
                print("[transport.py]: se encontró un objeto sin clave 'image', omitiendo...")
        except KeyError: 
            pass

    return images, total_pages