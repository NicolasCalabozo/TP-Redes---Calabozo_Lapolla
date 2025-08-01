from fastapi import FastAPI
from fastapi import Query
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import servicioServidor as ss

security = HTTPBasic()
app = FastAPI()

@app.get("/allMovies")
def allMovies() -> JSONResponse:
    return ss.get_titulos()

@app.get("/filteredMovies")
def filteredMovies(title: str) -> JSONResponse:
    return ss.get_peliculas_por_titulo(title)

@app.get("/filmography")
def filmography(name: str) -> JSONResponse:
    return ss.get_filmografia(name)

@app.get("/moviesByGender")
def moviesByGender(generos : list[str] = Query(...)) -> JSONResponse:
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
def agregarPelicula(pelicula : dict[str, str|int|list[str]]):
    return ss.post_pelicula(pelicula)

@app.get("/verificarAcceso")
def verificarAcceso(credentials: HTTPBasicCredentials = Depends(security)):
    permisos = ss.verificar_credenciales(credentials)
    return {"permisos": permisos}
    
