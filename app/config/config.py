# archivo de configuración del sistema.

# versión del TP.
VERSION = 'Trabajo práctico - 2° C. 2024 - Grupo 1'

# Rick & Morty REST API para capturar imágenes de la galería
DEFAULT_PAGE = '1'
DEFAULT_REST_API_URL = 'https://rickandmortyapi.com/api/character?page=' + DEFAULT_PAGE
BASE_URL = "https://rickandmortyapi.com/api/character/"


# Palabra buscada por defecto.
DEFAULT_NAME_QUERY_PARAM = '&name='
DEFAULT_REST_API_SEARCH = DEFAULT_REST_API_URL + DEFAULT_NAME_QUERY_PARAM # https://rickandmortyapi.com/api/character?page=1&name=?