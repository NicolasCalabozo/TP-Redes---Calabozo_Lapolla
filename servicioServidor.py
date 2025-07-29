import json

def getRawMovies():
    with open('movies.json', 'r', encoding='utf-8') as json_file:
        datos = json.load(json_file)
    return datos

def getMovieTitles():
    peliculas = getRawMovies()
    cadena_respuesta = "\nListado de todas las películas:\n"
    cadena_respuesta += formatear_texto(peliculas)
    return cadena_respuesta

def getFilteredMoviesByTitle(filtro_titulo: str) -> str:
    peliculas = getRawMovies()
    peliculas_filtradas = []
    cadena_respuesta = ""
    for pelicula in peliculas:
        if filtro_titulo.upper().strip() in pelicula['title'].upper().strip():
            peliculas_filtradas.append(pelicula)
    cadena_respuesta = formatear_texto(peliculas_filtradas)
    return cadena_respuesta

def getFilmography(filtro_nombre: str) -> str:
    peliculas = getRawMovies()
    cadena_respuesta = f"\nPelículas del actor {filtro_nombre}:\n"
    filmografia = []
    for pelicula in peliculas:
        for elenco in pelicula['cast']:
            if filtro_nombre.upper().strip() in elenco.upper():
                filmografia.append(pelicula)
    cadena_respuesta += formatear_texto(filmografia)  
    return cadena_respuesta

def getMoviesByGenders(generos: list[str]) -> str:
    peliculas = getRawMovies()
    peliculas_filtradas = [
        pelicula for pelicula in peliculas if any(genero.strip().upper() in map(str.upper,pelicula['genres']) for genero in generos)
    ]
    cadena_respuesta = f"\nCantidad de resultados: {len(peliculas_filtradas)}\n" 
    cadena_respuesta += formatear_texto(peliculas_filtradas)
    return cadena_respuesta

def getSinopsis(filtro_titulo: str) -> str:
    peliculas = getRawMovies()
    for pelicula in peliculas:
        if pelicula['title'].upper().strip() == filtro_titulo.upper().strip():
            if pelicula.get('extract', False):
                cadena_respuesta = f"\nSinopsis: \n{pelicula['extract']}\n"
            else:
                cadena_respuesta = f'\nNo se encontró una sinopsis para la película {filtro_titulo}\n'
            return cadena_respuesta
    return "\nNo se encontró una película con ese título\n"

def getMoviesByYear(filtro_año: int) -> str:
    peliculas = getRawMovies()
    peliculas_filtradas = []
    cadena_respuesta = f'\nPelículas del año {filtro_año}:\n'
    for pelicula in peliculas:
        if pelicula['year'] == filtro_año:
            peliculas_filtradas.append(pelicula)
    cadena_respuesta += f"\nCantidad de resultados: {len(peliculas_filtradas)}\n"   
    cadena_respuesta += formatear_texto(peliculas_filtradas)        
    return cadena_respuesta

def getFilmographyByGender(filtro_actor: str, filtro_genero: str) -> str:
    peliculas = getRawMovies()
    filmografia = []
    cadena_respuesta = f'\nPelículas del actor {filtro_actor.title()} y género {filtro_genero.title()}:\n'
    for pelicula in peliculas:
        if filtro_actor.upper().strip() in map(str.upper, pelicula['cast']) and filtro_genero.upper().strip() in map(str.upper,pelicula['genres']):
            filmografia.append(pelicula)
    cadena_respuesta += f"\nCantidad de resultados: {len(filmografia)}\n"   
    cadena_respuesta += formatear_texto(filmografia)
    return cadena_respuesta

def formatear_texto(lista_peliculas : list[dict[str,str]])-> str:
    cadena_formateada = ""
    i=0
    #OJO: Tal vez ordenar alfabeticamente
    if not len(lista_peliculas):
        return "\nNo hay películas que cumplan con el criterio ingresado\n"
    for pelicula in lista_peliculas:
        i+=1
        cadena_formateada += f"{i}.\t{pelicula['title']}\n"
        
    return cadena_formateada