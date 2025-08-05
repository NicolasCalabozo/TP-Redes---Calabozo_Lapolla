from fastapi import FastAPI
from fastapi import Query
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from modelos import PeliculaRequest
import servicioServidor as ss
from fastapi import FastAPI, Request, HTTPException, status
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict


security = HTTPBasic()
app = FastAPI()


#OJO: metodo que descargue el archivo en la ruta especificada
#Que se ejecute siempre que no exista el archivo en el servidor

VENTANA = timedelta(seconds=1)   # Ventana de tiempo
MAX_PETICIONES = 10             # Máximo de peticiones dentro de la ventana

cubos_ip: Dict[str, Deque[datetime]] = {}

@app.middleware("http")
async def limitador(request: Request, call_next):
    ip = request.client.host
    ahora = datetime.now()

    cubo = cubos_ip.setdefault(ip, deque())

    # Eliminar timestamps fuera de la ventana
    while cubo and (ahora - cubo[0]) > VENTANA:
        cubo.popleft()

    if len(cubo) >= MAX_PETICIONES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas solicitudes: límite 10 req/s",
        )

    cubo.append(ahora)
    respuesta = await call_next(request)
    return respuesta


@app.get("/allMovies")
def allMovies() -> JSONResponse:
    return ss.get_todos_titulos()


@app.get("/filteredMovies")
def filteredMovies(title: str) -> JSONResponse:
    return ss.get_peliculas_por_titulo(title)


@app.get("/filmography")
def filmography(name: str) -> JSONResponse:
    return ss.get_filmografia(name)


@app.get("/moviesByGender")
def moviesByGender(generos: list[str] = Query(...)) -> JSONResponse:
    return ss.get_peliculas_por_genero(generos)


@app.get("/movieSinopsis")
def sinopsis(title: str) -> JSONResponse:
    return ss.get_sinopsis(title)


@app.get("/moviesByYear")
def moviesByYear(year: int) -> JSONResponse:
    return ss.get_peliculas_por_año(year)


@app.get("/filmographyByGender")
def filmographyByGender(name: str, gender: str) -> JSONResponse:
    return ss.get_filmografia_por_genero(name, gender)


@app.post("/agregarPelicula")
def agregarPelicula(peticion: PeliculaRequest) -> JSONResponse:
    return ss.post_pelicula(peticion.pelicula, peticion.permisos)


@app.get("/obtenerPeliculaPorId")
def obtenerPelicula(titulo: str, año: int):
    return ss.get_pelicula_id(titulo, año)


@app.post("/verificarAcceso")
def verificarAcceso(credentials: HTTPBasicCredentials = Depends(security)):
    permisos = ss.verificar_credenciales(credentials)
    return {"permisos": permisos}


@app.delete("/eliminarPelicula")
def eliminarPelicula(title: str, year: int, credentials: HTTPBasicCredentials = Depends(security)) -> JSONResponse:
    permisos = ss.verificar_credenciales(credentials)
    return ss.eliminar_pelicula_por_titulo_y_año(title, year, permisos)