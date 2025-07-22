from fastapi import FastAPI
import json
app = FastAPI()


@app.get("/allMovies")
def allMovies():
    return getMovieTitles()

@app.get("/filteredMovies")
def filteredMovies(title: str) -> list[str]:
    return getFilteredMovies(title)

@app.get("/filmography")
def filmography(title: str) -> list[str]:
    return getFilmography(title)


def getRawMovies():
    with open('movies.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def getMovieTitles() -> list[str]: 
    data = getRawMovies()
    titles = [movie['title'] for movie in data]
    return titles

def getFilteredMovies(filter_text: str) -> list[str]:
    titles = getMovieTitles()
    filtered_titles = []
    for title in titles:
        if filter_text.upper().strip() in title.upper():
            filtered_titles.append(title)
    return filtered_titles

def getFilmography(name_filter: str):
    data = getRawMovies()
    filmography = []
    for movie in data:
        for cast in movie['cast']:
            if name_filter.upper().strip() in cast.upper():
                filmography.append(movie['title'])
    return filmography