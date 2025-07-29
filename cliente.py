import requests

def consultar_todas():
    respuesta = requests.get("http://localhost:8000/allMovies")
    print(respuesta.json())

def buscar_por_titulo(titulo: str) -> list[str]:
    respuesta = requests.get("http://localhost:8000/filteredMovies", params = {"title": titulo})
    print(respuesta.json())

def buscar_filmografia(actor: str) -> list[str]:
    respuesta = requests.get("http://localhost:8000/filmography", params = {"name": actor})
    print(respuesta.json())

def buscar_por_genero(genero1: str, genero2: str, genero3: str) -> list[str]:
    respuesta = requests.get("http://localhost:8000/moviesByGender", params = {"gender1": genero1, "gender2": genero2, "gender3": genero3})
    print(respuesta.json())

def buscar_sinopsis(titulo: str) -> str:
    respuesta = requests.get("http://localhost:8000/movieSinopsis", params = {"title": titulo})
    print(respuesta.json())

def buscar_peliculas_año(año: int) -> list[str]:
    respuesta = requests.get("http://localhost:8000/moviesByYear", params = {"year": año})
    print(respuesta.json())

def buscar_filmografia_genero(actor: str, genero: str) -> list[str]:
    respuesta = requests.get("http://localhost:8000/filmographyByGender", params = {"name": actor, "gender": genero})
    print(respuesta.json())
