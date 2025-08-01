import json
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Any
import secrets
from modelos import Permiso, Rol
security = HTTPBasic()

usuarios = [{
    "id": "1",
    "username": "admin",
    "password": "admin123",
    "rol": Rol.ADMIN,
    "permisos": [Permiso.TODO]
},
    {
        "id": "2",
        "username": "usuario",
        "password": "usuario123",
        "rol": Rol.USUARIO,
        "permisos": [Permiso.VER]
},
    {
        "id": "3",
        "username": "editor",
        "password": "editor123",
        "rol": Rol.EDITOR,
        "permisos": [Permiso.VER, Permiso.CREAR, Permiso.EDITAR]
}
]


def get_peliculas() -> dict:
    try:
        with open('movies.json', 'r', encoding='utf-8') as json_file:
            datos = json.load(json_file)
        # Devuelve diccionario porque es un método interno que no se va a usar para nada más que
        return {"status": status.HTTP_200_OK, "datos": datos}
    except FileNotFoundError:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": "El archivo 'movies.json' no existe."}
    except Exception as e:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": f"Error inesperado: {str(e)}"}


def get_titulos() -> JSONResponse:
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta["error"]}
        )

    peliculas = respuesta["datos"]
    cadena_respuesta = "\nListado de todas las películas:\n"
    cadena_respuesta += formatear_titulos(peliculas)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_peliculas_por_titulo(filtro_titulo: str) -> JSONResponse:
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas_filtradas = []
    for pelicula in peliculas:
        if filtro_titulo.upper().strip() in pelicula['title'].upper().strip():
            peliculas_filtradas.append(pelicula)

    cadena_respuesta = f"\nCantidad de resultados: {len(peliculas_filtradas)}\n"
    cadena_respuesta += formatear_titulos(peliculas_filtradas)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_filmografia(filtro_nombre: str) -> JSONResponse:
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    filmografia = []
    for pelicula in peliculas:
        for elenco in pelicula['cast']:
            if filtro_nombre.upper().strip() in elenco.upper().strip():
                filmografia.append(pelicula)

    cadena_respuesta = f"\nCantidad de resultados: {len(filmografia)}\n"
    cadena_respuesta += formatear_titulos(filmografia)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_peliculas_por_genero(generos: list[str]) -> JSONResponse:
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas_filtradas = [
        pelicula for pelicula in peliculas
        if any(genero.strip().upper() in map(str.upper, pelicula['genres']) for genero in generos)
    ]

    cadena_respuesta = f"\nCantidad de resultados: {len(peliculas_filtradas)}\n"
    cadena_respuesta += formatear_titulos(peliculas_filtradas)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_sinopsis(filtro_titulo: str) -> JSONResponse:
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    for pelicula in peliculas:
        if pelicula['title'].upper().strip() == filtro_titulo.upper().strip():
            if pelicula.get('extract'):
                cadena_respuesta = f"\nSinopsis: \n{pelicula['extract']}\n"
            else:
                cadena_respuesta = f'\nNo se encontró una sinopsis para la película {filtro_titulo}\n'

            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"contenido": cadena_respuesta}
            )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "mensaje": f"No se encontró una película con el título {filtro_titulo}"}
    )


def get_peliculas_por_año(filtro_año: int) -> JSONResponse:
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas_filtradas = [p for p in peliculas if p.get('year') == filtro_año]

    cadena_respuesta = f'\nPelículas del año {filtro_año}:\n'
    cadena_respuesta += f"\nCantidad de resultados: {len(peliculas_filtradas)}\n"
    cadena_respuesta += formatear_titulos(peliculas_filtradas)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_filmografia_por_genero(filtro_actor: str, filtro_genero: str) -> JSONResponse:
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    filmografia = []
    filtro_actor_upper = filtro_actor.upper().strip()
    filtro_genero_upper = filtro_genero.upper().strip()

    for pelicula in peliculas:
        cast_upper = map(str.upper, pelicula.get('cast', []))
        genres_upper = map(str.upper, pelicula.get('genres', []))
        if filtro_actor_upper in cast_upper and filtro_genero_upper in genres_upper:
            filmografia.append(pelicula)

    cadena_respuesta = f'\nPelículas del actor {filtro_actor.title()} y género {filtro_genero.title()}:\n'
    cadena_respuesta += f"\nCantidad de resultados: {len(filmografia)}\n"
    cadena_respuesta += formatear_titulos(filmografia)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def formatear_titulos(lista_peliculas: list[dict[str, str]]) -> str:
    cadena_formateada = ""
    i = 0
    # OJO: Tal vez ordenar alfabeticamente
    if not len(lista_peliculas):
        return "\nNo hay películas que cumplan con el criterio ingresado\n"
    for pelicula in lista_peliculas:
        i += 1
        cadena_formateada += f"{i}.\t{pelicula['title']}\n"
    return cadena_formateada


def post_pelicula(pelicula: dict[str, str | int | list[str]]) -> JSONResponse:
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas.append(pelicula)

    try:
        with open('movies.json', 'w', encoding='utf-8') as archivo:
            json.dump(peliculas, archivo, ensure_ascii=False, indent=4)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"No se pudo guardar la película: {str(e)}"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"mensaje": "Película agregada con éxito"}
    )


def verificar_credenciales(credenciales: HTTPBasicCredentials = Depends(security),) -> list[str]:
    # Buscar el usuario en la base de datos, extraer la contraseña, comparar
    usuario = buscar_usuario(credenciales.username)
    if (not usuario):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    usuario_correcto = secrets.compare_digest(
        credenciales.username, usuario['username'])
    contraseña_correcta = secrets.compare_digest(
        credenciales.password,  usuario['password'])

    if not (usuario_correcto and contraseña_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    return usuario['permisos']


def buscar_usuario(username: str) -> dict[str, Any] | None:
    for usuario in usuarios:
        if username == usuario['username']:
            return usuario
    return None
