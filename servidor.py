from fastapi import FastAPI
from fastapi import Query
import servicioServidor as ss
app = FastAPI()

@app.get("/allMovies")
def allMovies():
    return ss.getMovieTitles()

@app.get("/filteredMovies")
def filteredMovies(title: str) -> str:
    return ss.getFilteredMoviesByTitle(title)

@app.get("/filmography")
def filmography(name: str) -> str:
    return ss.getFilmography(name)

@app.get("/moviesByGender")
def moviesByGender(generos : list[str] = Query(...)) -> str:
    return ss.getMoviesByGenders(generos)

@app.get("/movieSinopsis")
def sinopsis(title: str) -> str:
    return ss.getSinopsis(title)

@app.get("/moviesByYear")
def moviesByYear(year: int) -> str:
    return ss.getMoviesByYear(year)

@app.get("/filmographyByGender")
def filmographyByGender(name: str, gender: str) -> str:
    return ss.getFilmographyByGender(name, gender)

