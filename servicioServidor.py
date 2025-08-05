import json
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Any
from modelos import Pelicula
import secrets
from utils import verificar_permisos, validar_entero, cadena_mayusculas
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
        return {"status": status.HTTP_200_OK, "datos": datos}
    except FileNotFoundError:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": "El archivo 'movies.json' no existe"}
    except Exception as e:
        return {"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "error": f"Error inesperado: {str(e)}"}


def get_todos_titulos(permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
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

# OJO: Devolver los datos de la pelicula formateados
# OJO: Crear funcion para formatear peliculas


def get_peliculas_por_titulo(filtro_titulo: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()
    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas_filtradas = []
    for pelicula in peliculas:
        if cadena_mayusculas(filtro_titulo) in cadena_mayusculas(pelicula['title']):
            peliculas_filtradas.append(pelicula)

    cadena_respuesta = f"\nCantidad de resultados: {len(peliculas_filtradas)}\n"
    cadena_respuesta += formatear_titulos(peliculas_filtradas)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_filmografia(filtro_nombre: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
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
            if cadena_mayusculas(filtro_nombre) in cadena_mayusculas(elenco):
                filmografia.append(pelicula)

    cadena_respuesta = f"\nCantidad de resultados: {len(filmografia)}\n"
    cadena_respuesta += formatear_titulos(filmografia)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_peliculas_por_genero(generos: list[str], permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas_filtradas = [
        pelicula for pelicula in peliculas
        if any(cadena_mayusculas(genero) in map(str.upper, pelicula['genres']) for genero in generos)
    ]

    cadena_respuesta = f"\nCantidad de resultados: {len(peliculas_filtradas)}\n"
    cadena_respuesta += formatear_titulos(peliculas_filtradas)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_sinopsis(filtro_titulo: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
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


def get_peliculas_por_año(filtro_año: int, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
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


def get_filmografia_por_genero(filtro_actor: str, filtro_genero: str, permisos: list[Permiso]) -> JSONResponse:
    '''
    A partir de un género y un actor devuelve la filmografía que cumple con lo especificado
    '''
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    filmografia = []
    actor = cadena_mayusculas(filtro_actor)
    genero = cadena_mayusculas(filtro_genero)

    for pelicula in peliculas:
        elenco = map(str.upper, pelicula.get('cast', []))
        generos = map(str.upper, pelicula.get('genres', []))
        if actor in elenco and genero in generos:
            filmografia.append(pelicula)

    cadena_respuesta = f'\nPelículas del actor {filtro_actor.title()} y género {filtro_genero.title()}:\n'
    cadena_respuesta += f"\nCantidad de resultados: {len(filmografia)}\n"
    cadena_respuesta += formatear_titulos(filmografia)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"contenido": cadena_respuesta}
    )


def get_pelicula_id(titulo: str, año: int, permisos: list[Permiso]):
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
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
    verificar_permisos(permisos, [Permiso.CREAR, Permiso.TODO])

    respuesta = get_peliculas()

    if respuesta.get("status") != 200:
        return JSONResponse(
            status_code=respuesta["status"],
            content={"error": respuesta.get("error")}
        )

    peliculas = respuesta["datos"]
    peliculas.append(pelicula.model_dump())

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

# OJO: Metodo para modificar


def put_pelicula(pelicula: Pelicula, id: int, permisos: list[str]):
    pass


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
    verificar_permisos(permisos, [Permiso.ELIMINAR, Permiso.TODO])
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
