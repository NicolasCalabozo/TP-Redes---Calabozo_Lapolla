import requests


def menu_general():
        while True:
            #ABM
            print("--           General             --")
            print("-    1.  Menú de consultas        -")
            print("-    2.  Menú de ABM              -")
            print("-    3.  Menu de test             -")
            print("-    0. Salir                     -")
            print("-----------------------------------")
            opcion = input("Ingrese una opción: ")
            if opcion == '1':
                menu_consultas()
            elif opcion == '2':
                menu_abm()
            elif opcion == '3':
                pass
            elif opcion == '0':
                break
            else:
                print("Opción no válida. Reintente.")
                continue
            

def menu_abm():
    while True:
        #ABM
        print("--                 Menu ABM                      --")
        print("-    1. Agregar película nueva                    -")
        print("-    2. Modificar película                        -")
        print("-    3. Eliminar película                         -")
        print("-    4. Consultar ultimas peliculas agregadas     -")
        print("-    0. Salir                                     -")
        print("---------------------------------------------------")
        opcion = input("Ingrese una opción: ")
        if opcion == '1':
            pass
        elif opcion == '2':
            pass
        elif opcion == '3':
            pass
        elif opcion == '4':
            pass
        elif opcion == '0':
                break
        else:
            print("Opción no válida. Reintente.")
            continue
        
def menu_consultas():

    while True:
        print("--                   Menu Consultas              --")
        print("-    1.  Mostrar todas las películas              -")
        print("-    2.  Buscar por título                        -")
        print("-    3.  Buscar filmografía por actor             -")
        print("-    4.  Buscar por género                        -")
        print("-    5.  Buscar sinopsis por titulo               -")
        print("-    6.  Buscar por año                           -")
        print("-    7.  Buscar filmografía por actor y género    -")
        print("-    0.  Salir                                    -")
        print("---------------------------------------------------")

        
        opcion = input("Ingrese una opción: ")
        if opcion == '1':
            consultar_todas()
            
        elif opcion == '2':
            titulo = input("Ingrese un título: ")
            buscar_por_titulo(titulo)
            
        elif opcion == '3':
            actor = input("Ingrese un actor: ")
            buscar_filmografia(actor)
            
        elif opcion == '4':
            i=0
            generos = []
            while(True):
                i += 1
                generos.append(input(f'Ingrese un género ({i}):'))
                opcion = input('¿Desea seguir ingresando géneros? (S/N): ').strip().upper()
                if opcion == 'N':
                    break
            buscar_por_genero(generos)
                    
        elif opcion == '5':
            titulo = input("Ingrese un título: ")
            buscar_sinopsis(titulo)
            
        elif opcion == '6':
            año = int(input("Ingrese un año: "))
            buscar_peliculas_año(año)
            
        elif opcion == '7':
            actor = input('Ingrese un actor: ')
            genero = input('Ingrese un género: ')
            buscar_filmografia_genero(actor,genero)
    
        elif opcion == '0':
            break
        
        else:
            print("Opción no válida. Reintente.")
            continue

#Métodos GET
def consultar_todas():
    respuesta = requests.get("http://localhost:8000/allMovies")
    print(respuesta.json())

def buscar_por_titulo(titulo: str) -> None:
    respuesta = requests.get("http://localhost:8000/filteredMovies", params = {"title": titulo})
    print(respuesta.json())

def buscar_filmografia(actor: str) -> None:
    respuesta = requests.get("http://localhost:8000/filmography", params = {"name": actor})
    print(respuesta.json())

def buscar_por_genero(generos: list[str]) -> None:
    respuesta = requests.get("http://localhost:8000/moviesByGender", params = {"generos": generos})
    print(respuesta.json())

def buscar_sinopsis(titulo: str) -> None:
    respuesta = requests.get("http://localhost:8000/movieSinopsis", params = {"title": titulo})
    print(respuesta.json())

def buscar_peliculas_año(año: int) -> None:
    respuesta = requests.get("http://localhost:8000/moviesByYear", params = {"year": año})
    print(respuesta.json())

def buscar_filmografia_genero(actor: str, genero: str) -> None:
    respuesta = requests.get("http://localhost:8000/filmographyByGender", params = {"name": actor, "gender": genero})
    print(respuesta.json())

#Metodos POST
      
def agregar_pelicula():
    pelicula = crear_pelicula()
    respuesta = requests.post("http://localhost:8000/agregarPelicula",
                            json= pelicula)
    print(respuesta.status_code)

def crear_pelicula() -> dict[str, str|int|list[str]]:
    titulo = input("Ingrese el título de la película: ").strip()
    #Try Catch por si ingresan una letra
    año = int(input("Ingrese el año de estreno: "))
    elenco = []
    opc = input('¿Desea ingresar el elenco? (S/N): ').upper().strip()
    if(validar_opcion(opc) == 'S'):
        cadena_elenco = input(f"Ingrese el/los miembro/s del elenco, separados por coma: ")
        elenco = map(str.strip, cadena_elenco.split(sep=','))
    generos = []
    
    #Titanic
    #Titanic - está en la posicion 10 de lista peliculas[10] = titanic
    #modifico titanic, Titanic 2
    #Lo guardo / piso en la lista en la posicion 10
    
    opc = input("¿Desea ingresar los géneros de la película? (S/N): ")
    if validar_opcion(opc) == 'S':
        generos_cadena = (input(f"Ingrese los generos de la película separados por coma: "))
        generos = map(str.strip, generos_cadena.split(','))
    sinopsis = ""
    opc = input("¿Desea ingresar una sinopsis? (S/N): ")
    if validar_opcion(opc) == 'S':
        sinopsis = input("Ingrese la sinopsis: ")
    pelicula = {
        "title" : titulo,
        "year": año,
        "cast": elenco,
        "genres": generos,
        "extract": sinopsis
    }
    return pelicula
        
def validar_opcion(opc:str):
    while True:
        if(opc != "N" or opc != "S"):
            print("Opción incorrecta. Reintente (S/N).")
        else:
            break
    return opc  

def modificar_pelicula():
    pass

def borrar_pelicula():
    pass

menu_general()


#OJO: Agregar paginado
# i=0 i=5 pagina 1 <- la pagina donde estamos
# i=5 i=10 pagina 2
# ...
#round(len()/5) <- numero de paginas
#round(len()/5)  - i=0+4, i=5+4, elemento[i] 