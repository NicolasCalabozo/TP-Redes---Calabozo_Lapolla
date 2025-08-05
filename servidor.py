from fastapi import FastAPI
from fastapi import Query
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from modelos import PeliculaRequest
import servicioServidor as ss
from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


security = HTTPBasic()
app = FastAPI()
limiter = Limiter(key_func = get_remote_address) #toma la IP del cliente
#Viendo y "Si la app tiene autenticación por usuario, 
# podrías usar lambda req: req.user.username para limitar por usuario."
#que capaz va con la lista de diccionarios de usuarios y permisos 
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
#configura el limitador para funcionar por IP del cliente

#Si limitamos las solicitudes de esta forma hay que agregar a los métodos "@limiter.limit("5/second")"
# y las funciones necesitan el parametro request, de tipo request, porque si el endpoint no lo incluye
#FastAPI no puede inyectarlo, y el "decorador" falla o no funciona como debería.


#OJO: metodo que descargue el archivo en la ruta especificada
#Que se ejecute siempre que no exista el archivo en el servidor

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