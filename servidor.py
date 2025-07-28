from fastapi import FastAPI
import json
import servicioServidor as ss
app = FastAPI()


@app.get("/allMovies")
def allMovies():
    return ss.getMovieTitles()

@app.get("/filteredMovies")
def filteredMovies(title: str) -> list[str]:
    return ss.getFilteredMovies(title)

@app.get("/filmography")
def filmography(name: str) -> list[str]:
    return ss.getFilmography(name)

@app.get("/moviesByGender")
def moviesByGender(gender1: str, gender2: str, gender3: str) -> list[str]:
    return ss.getMoviesByGenders(gender1, gender2, gender3)

@app.get("/movieSinopsis")
def sinopsis(title: str) -> str:
    return ss.getSinopsis(title)

@app.get("/moviesByYear")
def moviesByYear(year: int) -> list[str]:
    return ss.getMoviesByYear(year)

@app.get("/filmographyByGender")
def filmographyByGender(name: str, gender: str) -> list[str]:
    return ss.getFilmographyByGender(name, gender)