import json
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

def getMoviesByGenders(gender_1 = None, gender_2 = None, gender_3 = None) -> list[str]:
    data = getRawMovies()
    movies = []
    for movie in data:
        if gender_1 and gender_2 and gender_3:
            if gender_1 in movie['genres'] and gender_2 in movie['genres'] and gender_3 in movie['genres']:
                movies.append(movie['title'])
        elif gender_1 and gender_2:
            if gender_1 in movie['genres'] and gender_2 in movie['genres']:
                movies.append(movie['title'])
        elif gender_1 and gender_3:
            if gender_1 in movie['genres'] and gender_3 in movie['genres']:
                movies.append(movie['title'])
        elif gender_2 and gender_3:
            if gender_2 in movie['genres'] and gender_3 in movie['genres']:
                movies.append(movie['title'])
        else:
            raise ValueError("No hay pelicula con esos generos")
    return movies

def getSinopsis(filter_text: str) -> str:
    data = getRawMovies()
    for movie in data:
        if movie['title'] == filter_text:
            return movie['extract']

def getMoviesByYear(filter_year: int) -> list[str]:
    data = getRawMovies()
    movies = []
    for movie in data:
        if movie['year'] == filter_year:
            movies.append(movie['title'])
    return movies

def getFilmographyByGender(name_filter: str, gender_filter) -> list[str]:
    data = getRawMovies()
    filmography = []
    for movie in data:
        if name_filter in movie['cast'] and gender_filter in movie['genres']:
            filmography.append(movie['title'])
    return filmography
