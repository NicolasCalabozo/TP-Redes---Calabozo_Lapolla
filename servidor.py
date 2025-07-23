from fastapi import FastAPI
import requests
import servicioServidor as serv 
app = FastAPI()
flagDownload = False

@app.get("/download")
def databaseDownload():
    global flagDownload
    url = "https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json"
    response = requests.get(url)
    #OJO: Si el recurso está disponible: Try/Catch
    if flagDownload == False:
        with open("movies.json", "wb") as f:
            f.write(response.content)
            flagDownload = True
    else:
        while(True):
            respuesta = input('¿Desea sobreescribir el archivo movies.json? (S/N):').upper()
            if(respuesta in 'SN'):
                if(respuesta == 'S'):
                    with open("movies.json", "wb") as f:
                        f.write(response.content)
                    print('Archivo sobrescrito correctamente.')
                    break
                else:
                    ##OJO : Sacar mensaje
                    print('No se sobrescribió el archivo.')
                    break
            else:
                print('Entrada incorrecta. Reintente.')

@app.get("/allMovies")
def allMovies():
    return serv.getMovieTitles()

@app.get("/filteredMovies")
def filteredMovies(title: str) -> list[str]:
    return serv.getFilteredMoviesByTitle(title)

@app.get("/filmography")
def filmography(title: str) -> list[str]:
    return serv.getFilmography(title)