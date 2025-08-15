from fastapi import FastAPI, Request, HTTPException , Query, Depends, status
import uvicorn
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from modelos import Permiso
from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict
from utils import verificar_permisos_servidor
import servicioServidor as ss
from modelos import Pelicula
from auth import security, obtener_permisos, obtener_rol
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
def allMovies(permisos: list[str] = Depends(obtener_permisos), pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_todos_titulos(permisos, pagina)


@app.get("/filteredMovies")
def filteredMovies(title: str, permisos: list[str] = Depends(obtener_permisos), pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_peliculas_por_titulo(title, permisos, pagina)


@app.get("/filmography")
def filmography(name: str, permisos: list[str] = Depends(obtener_permisos), pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_filmografia(name, permisos, pagina)


@app.get("/moviesByGender")
def moviesByGender(permisos: list[str] = Depends(obtener_permisos), generos: list[str] = Query(...), pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_peliculas_por_genero(generos, permisos, pagina)


@app.get("/movieSinopsis")
def sinopsis(title: str, permisos: list[str] = Depends(obtener_permisos)) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_sinopsis(title, permisos)


@app.get("/moviesByYear")
def moviesByYear(year: int, permisos: list[str] = Depends(obtener_permisos), pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_peliculas_por_año(year, permisos, pagina)


@app.get("/filmographyByGender")
def filmographyByGender(name: str, gender: str, permisos: list[str] = Depends(obtener_permisos), pagina: int = 1) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_filmografia_por_genero(name, gender, permisos,pagina)

@app.get("/obtenerGeneros")
def obtenerGeneros(permisos: list[str] = Depends(obtener_permisos)) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_generos()

@app.get("/obtenerPeliculaPorId")
def obtenerPelicula(titulo: str, año: int, permisos: list[str] = Depends(obtener_permisos)):
    '''Endpoint para obtener una pelicula, con su ID, por año y titulo'''
    verificar_permisos_servidor(permisos, [Permiso.VER, Permiso.TODO])
    return ss.get_pelicula_id(titulo, año, permisos)

@app.post("/agregarPelicula")
def agregarPelicula(pelicula:Pelicula, permisos: list[str] = Depends(obtener_permisos)) -> JSONResponse:
    '''Endpoint de creación de películas'''
    verificar_permisos_servidor(permisos, [Permiso.CREAR, Permiso.TODO])
    return ss.post_pelicula(pelicula, permisos)

@app.post("/verificarAcceso")
def verificarAcceso(credentials: HTTPBasicCredentials = Depends(security)):
    '''Endpoint para la obtencion de permisos del usuario'''
    permisos = obtener_permisos(credentials)
    rol = obtener_rol(credentials)
    return {"permisos": permisos, "rol": rol}

@app.delete("/eliminarPelicula")
def eliminarPelicula(title: str, year: int, permisos: list[str] = Depends(obtener_permisos)) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.ELIMINAR, Permiso.TODO])
    return ss.eliminar_pelicula_por_titulo_y_año(title, year, permisos)

@app.put("/modificarPelicula/{id_pelicula}")
def modificar_pelicula(id_pelicula: int, pelicula: Pelicula, permisos: list[str] = Depends(obtener_permisos)) -> JSONResponse:
    verificar_permisos_servidor(permisos, [Permiso.EDITAR, Permiso.TODO])
    return ss.put_pelicula(pelicula, id_pelicula, permisos)

if __name__ == "__main__":
    ss.descargar_movies_json()
    uvicorn.run("servidor:app", host="0.0.0.0", port=8000, reload=True)