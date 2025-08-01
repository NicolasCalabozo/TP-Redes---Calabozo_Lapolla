from fastapi import FastAPI
from fastapi import Query
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from modelos import PeliculaRequest
import servicioServidor as ss

security = HTTPBasic()
app = FastAPI()

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
