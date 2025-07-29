from fastapi import FastAPI
from fastapi import Query
import servicioServidor as ss
app = FastAPI()

@app.get("/allMovies")
def allMovies():
    return ss.get_titulos()

@app.get("/filteredMovies")
def filteredMovies(title: str) -> str:
    return ss.get_peliculas_por_titulo(title)

@app.get("/filmography")
def filmography(name: str) -> str:
    return ss.get_filmografia(name)

@app.get("/moviesByGender")
def moviesByGender(generos : list[str] = Query(...)) -> str:
    return ss.get_peliculas_por_genero(generos)

@app.get("/movieSinopsis")
def sinopsis(title: str) -> str:
    return ss.get_sinopsis(title)

@app.get("/moviesByYear")
def moviesByYear(year: int) -> str:
    return ss.get_peliculas_por_año(year)

@app.get("/filmographyByGender")
def filmographyByGender(name: str, gender: str) -> str:
    return ss.get_filmografia_por_genero(name, gender)

@app.post("/agregarPelicula")
def agregarPelicula(pelicula : dict[str, str|int|list[str]]):
    ss.post_pelicula(pelicula)
    
