from fastapi import FastAPI, Request, HTTPException , Query, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from modelos import PeliculaRequest, Permiso
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict
from utils import verificar_permisos
import servicioServidor as ss

security = HTTPBasic()
app = FastAPI()

#OJO: metodo que descargue el archivo en la ruta especificada
#Que se ejecute siempre que no exista el archivo en el servidor

VENTANA = timedelta(seconds = 1)   # Ventana de tiempo
MAX_PETICIONES = 10             # Máximo de peticiones dentro de la ventana

cubos_ip: Dict[str, Deque[datetime]] = {}

@app.middleware("http")
async def limitador(request: Request, call_next):
    ip = request.client.host # type: ignore
    ahora = datetime.now()

    cubo = cubos_ip.setdefault(ip, deque())

    # Eliminar timestamps fuera de la ventana
    while cubo and (ahora - cubo[0]) > VENTANA:
        cubo.popleft()

    if len(cubo) >= MAX_PETICIONES:
        raise HTTPException(
            status_code = status.HTTP_429_TOO_MANY_REQUESTS,
            detail = "Demasiadas solicitudes: límite 10 req/s",
        )

    cubo.append(ahora)
    respuesta = await call_next(request)
    return respuesta


@app.get("/allMovies")
def allMovies(permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_todos_titulos(permisos)


@app.get("/filteredMovies")
def filteredMovies(title: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_peliculas_por_titulo(title, permisos)


@app.get("/filmography")
def filmography(name: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_filmografia(name, permisos)


@app.get("/moviesByGender")
def moviesByGender(permisos: list[Permiso],generos: list[str] = Query(...)) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_peliculas_por_genero(generos, permisos)


@app.get("/movieSinopsis")
def sinopsis(title: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_sinopsis(title, permisos)


@app.get("/moviesByYear")
def moviesByYear(year: int, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_peliculas_por_año(year, permisos)


@app.get("/filmographyByGender")
def filmographyByGender(name: str, gender: str, permisos: list[Permiso]) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_filmografia_por_genero(name, gender, permisos)


@app.post("/agregarPelicula")
def agregarPelicula(peticion: PeliculaRequest) -> JSONResponse:
    '''Endpoint de creación de películas'''
    verificar_permisos(peticion.permisos, [Permiso.CREAR, Permiso.TODO])
    return ss.post_pelicula(peticion.pelicula, peticion.permisos)


@app.get("/obtenerPeliculaPorId")
def obtenerPelicula(titulo: str, año: int, permisos: list[Permiso]):
    '''Endpoint para obtener una pelicula, con su ID, por año y titulo'''
    verificar_permisos(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_pelicula_id(titulo, año, permisos)


@app.post("/verificarAcceso")
def verificarAcceso(credentials: HTTPBasicCredentials = Depends(security)):
    '''Endpoint para la obtencion de permisos del usuario'''
    permisos = ss.obtener_permisos(credentials)
    return {"permisos": permisos}


@app.delete("/eliminarPelicula")
def eliminarPelicula(title: str, year: int, permisos: list[Permiso], credentials: HTTPBasicCredentials = Depends(security)) -> JSONResponse:
    verificar_permisos(permisos, [Permiso.ELIMINAR, Permiso.TODO])
    return ss.eliminar_pelicula_por_titulo_y_año(title, year, permisos)