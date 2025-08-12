import json
import os
import requests
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Any
from modelos import Pelicula
import secrets
from utils import verificar_permisos_servidor, cadena_mayusculas
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

RESULTADOS_POR_PAGINA = 10


def get_peliculas() -> dict:
    try:
        with open('movies.json', 'r', encoding='utf-8') as json_file:
            datos = json.load(json_file)
        return {"status": status.HTTP_200_OK, "datos": datos}
    except FileNotFoundError:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": "El archivo 'movies.json' no existe"}
    except Exception as e:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": f"Error inesperado: {str(e)}"}


def get_todos_titulos(permisos: list[Permiso], pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(status_code=respuesta["status"], content={"error": respuesta["error"]})

    peliculas = respuesta["datos"]
    paginado = paginar_resultados(peliculas, pagina)

    cadena_respuesta = formatear_titulos(paginado["resultados"])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "pagina": paginado["pagina"],
            "totalPaginas": paginado["totalPaginas"],
            "totalResultados": paginado["totalResultados"],
            "contenido": cadena_respuesta
        }
    )


# OJO: Devolver los datos de la pelicula formateados
# OJO: Crear funcion para formatear peliculas

def get_peliculas_por_titulo(titulo: str, permisos: list[Permiso], pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(status_code=respuesta["status"], content={"error": respuesta.get("error")})

    # OJO: Mejora filtrar por concidencias cercanas
    peliculas_filtradas = [
        pelicula for pelicula in respuesta["datos"]
        if cadena_mayusculas(titulo) in cadena_mayusculas(pelicula['title'])
    ]
    paginado = paginar_resultados(peliculas_filtradas, pagina)
    cadena_respuesta = "".join(formatear_datos_pelicula(p)
                               for p in paginado["resultados"])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "pagina": paginado["pagina"],
            "totalPaginas": paginado["totalPaginas"],
            "totalResultados": paginado["totalResultados"],
            "contenido": cadena_respuesta
        }
    )


def get_filmografia(nombre: str, permisos: list[Permiso], pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(status_code=respuesta["status"], content={"error": respuesta.get("error")})

    peliculas_filtradas = [
        pelicula for pelicula in respuesta["datos"]
        if cadena_mayusculas(nombre) in cadena_mayusculas(pelicula['director']) or
        cadena_mayusculas(nombre) in cadena_mayusculas(pelicula['cast'])
    ]
    paginado = paginar_resultados(peliculas_filtradas, pagina)
    cadena_respuesta = formatear_titulos(paginado["resultados"])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "pagina": paginado["pagina"],
            "totalPaginas": paginado["totalPaginas"],
            "totalResultados": paginado["totalResultados"],
            "contenido": cadena_respuesta
        }
    )


def get_peliculas_por_genero(generos: list[str], permisos: list[Permiso], pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(status_code=respuesta["status"], content={"error": respuesta.get("error")})

    peliculas_filtradas = [
        pelicula for pelicula in respuesta["datos"]
        if all(genero in pelicula['genres'] for genero in generos)
    ]
    paginado = paginar_resultados(peliculas_filtradas, pagina)
    cadena_respuesta = formatear_titulos(paginado["resultados"])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "pagina": paginado["pagina"],
            "totalPaginas": paginado["totalPaginas"],
            "totalResultados": paginado["totalResultados"],
            "contenido": cadena_respuesta
        }
    )


def get_sinopsis(filtro_titulo: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    for pelicula in peliculas:
        if cadena_mayusculas(pelicula['title']) == cadena_mayusculas(filtro_titulo):
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


def get_peliculas_por_año(year: int, permisos: list[Permiso], pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(status_code=respuesta["status"], content={"error": respuesta.get("error")})

    peliculas_filtradas = [
        pelicula for pelicula in respuesta["datos"]
        if pelicula['year'] == year
    ]
    paginado = paginar_resultados(peliculas_filtradas, pagina)
    cadena_respuesta = formatear_titulos(paginado["resultados"])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "pagina": paginado["pagina"],
            "totalPaginas": paginado["totalPaginas"],
            "totalResultados": paginado["totalResultados"],
            "contenido": cadena_respuesta
        }
    )


def get_filmografia_por_genero(filtro_actor: str, filtro_genero: str, permisos: list[Permiso], pagina: int = 1) -> JSONResponse:
    """
    A partir de un género y un actor devuelve la filmografía que cumple con lo especificado.
    Incluye paginado y conteo total de resultados.
    """
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]

    actor = cadena_mayusculas(filtro_actor)
    genero = cadena_mayusculas(filtro_genero)

    filmografia = [
        pelicula for pelicula in peliculas
        if actor in map(str.upper, pelicula.get('cast', []))
        and genero in map(str.upper, pelicula.get('genres', []))
    ]

    paginado = paginar_resultados(filmografia, pagina)
    cadena_respuesta = (
        f"\nPelículas del actor {filtro_actor.title()} y género {filtro_genero.title()}:\n"
        f"\nCantidad de resultados: {paginado['totalResultados']}\n"
        + formatear_titulos(paginado["resultados"])
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "pagina": paginado["pagina"],
            "totalPaginas": paginado["totalPaginas"],
            "totalResultados": paginado["totalResultados"],
            "contenido": cadena_respuesta
        }
    )


def get_pelicula_id(titulo: str, año: int, permisos: list[Permiso]):
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )
    peliculas = respuesta['datos']
    id = None
    pelicula_encontrada = None
    for i, pelicula in enumerate(peliculas):
        if cadena_mayusculas(pelicula['title']) == cadena_mayusculas(titulo) and pelicula['year'] == año:
            id = i
            pelicula_encontrada = pelicula
            break

    if id is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'error': f'No se encontró la pelicula solicitada - {titulo} ({año})'}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": {"id": id, "pelicula": pelicula_encontrada}}
    )


def formatear_titulos(lista_peliculas: list[dict[str, str]]) -> str:
    '''Stringbuilder que permite concatenar títulos con un formato fijo'''
    cadena_formateada = ""
    i = 0
    # OJO: Tal vez ordenar alfabeticamente
    if not len(lista_peliculas):
        return "\nNo hay películas que cumplan con el criterio ingresado\n"
    for pelicula in lista_peliculas:
        i += 1
        cadena_formateada += f"{i}.\t{pelicula['title']}\n"
    return cadena_formateada


def post_pelicula(pelicula: Pelicula, permisos: list[Permiso]) -> JSONResponse:
    '''
    Método que permite persistir una película en el archivo 'movies.json'
    '''
    verificar_permisos_servidor(permisos, [Permiso.CREAR, Permiso.TODO])

    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas.append(pelicula.model_dump())
    # OJO: Testing
    print(pelicula.model_dump())
    try:
        with open('movies.json', 'w', encoding='utf-8') as archivo:
            json.dump(peliculas, archivo, ensure_ascii=False, indent=4)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"No se pudo guardar la película: {str(e)}"}
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"contenido": "Película agregada con éxito"}
    )


def obtener_permisos(credenciales: HTTPBasicCredentials = Depends(security)) -> list[Permiso]:
    '''
    Método que permite la obtención de los permisos del usuario según sus credenciales de login
    '''
    usuario = buscar_usuario(credenciales.username)
    if (not usuario):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    contraseña_correcta = secrets.compare_digest(
        credenciales.password,  usuario['password'])

    if not (usuario and contraseña_correcta):
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


def eliminar_pelicula_por_titulo_y_año(titulo: str, año: int, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.ELIMINAR, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )
    peliculas = respuesta["datos"]
    titulo = cadena_mayusculas(titulo)
    nueva_lista = [p for p in peliculas if not (
        cadena_mayusculas(p["title"]) == titulo and p.get("year") == año)]
    if len(nueva_lista) == len(peliculas):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"No se encontró la película '{titulo}' del año {año}"}
        )
    try:
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(nueva_lista, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"No se pudo eliminar la película: {str(e)}"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "contenido": f"Película '{titulo}' ({año}) eliminada correctamente"}
    )


def put_pelicula(pelicula_actualizada: Pelicula, id_pelicula: int, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.EDITAR, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )
    peliculas = respuesta["datos"]
    if id_pelicula < 0 or id_pelicula >= len(peliculas):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": f"No se encontró una película con el ID {id_pelicula}"}
        )
    peliculas[id_pelicula] = pelicula_actualizada.model_dump()
    try:
        with open('movies.json', 'w', encoding='utf-8') as archivo:
            json.dump(peliculas, archivo, ensure_ascii=False, indent=4)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"No se pudo modificar la película: {str(e)}"}
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "contenido": f"Película '{pelicula_actualizada.titulo}' modificada con éxito"}
    )


def get_generos() -> JSONResponse:
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )
    generos = {}
    peliculas = respuesta['datos']
    for pelicula in peliculas:
        for genero in pelicula['genres']:
            if genero in generos:
                generos[genero] += 1
            else:
                generos[genero] = 1
    # OJO: Testing
    print(f'-- Generos obtenidos -- ')
    print(generos)
    return JSONResponse(status_code=status.HTTP_200_OK, content=generos)


def paginar_resultados(peliculas, pagina: int, tamaño_pagina: int = RESULTADOS_POR_PAGINA):
    """
    Aplica paginación a una lista de resultados.
    Retorna un diccionario con metadatos y la página solicitada.
    """
    total_peliculas = len(peliculas)
    total_paginas = (total_peliculas + tamaño_pagina - 1) // tamaño_pagina

    if pagina < 1:
        pagina = 1
    elif pagina > total_paginas:
        pagina = total_paginas if total_paginas > 0 else 1

    inicio = (pagina - 1) * tamaño_pagina
    final = inicio + tamaño_pagina
    resultados = peliculas[inicio:final]

    # OJO: Para testing:
    print("-- Resultados del paginado -- ")
    print(f'Pagina: {pagina}')
    print(f'Inicio: {inicio}')
    print(f'Final: {final}')
    print(f'{resultados}')
    # OJO: Borrar antes de entregar

    return {
        "totalPaginas": total_paginas,
        "pagina": pagina,
        "resultados": resultados,
        "totalResultados": total_peliculas
    }


def formatear_datos_pelicula(pelicula: dict) -> str:
    return (
        f"Título: {pelicula.get('title', 'N/A')}\n"
        f"Año: {pelicula.get('year', 'N/A')}\n"
        f"Elenco: {', '.join(pelicula.get('cast', []))}\n"
        f"Géneros: {', '.join(pelicula.get('genres', []))}\n"
        f"Sinopsis: {pelicula.get('extract', 'Sin sinopsis disponible')}\n"
    )


def descargar_movies_json() -> None:
    ruta: str = "movies.json"
    url: str = "https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json"
    if os.path.exists(ruta):
        print(f"El archivo '{ruta}' ya existe. No se descargará nuevamente.")
        return
    print(f"Descargando archivo '{ruta}'")
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        with open(ruta, "wb") as f:
            f.write(respuesta.content)
        print(f"Archivo '{ruta}' descargado correctamente.")
    else:
        print(f"Error al descargar el archivo: HTTP {respuesta.status_code}")
