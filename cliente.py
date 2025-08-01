import requests
from requests.auth import HTTPBasicAuth
import servicioCliente as sc
from modelos import Permiso, Rol
# credenciales = HTTPBasicAuth <- variable global
# permisos_usuario = [...]
# USUARIO
# {
#     "id":1,
#     "usuario": "pepe",
#     "contraseña": "pepe2",
#     "permisos": ["crear", "ver", "modificar", "editar", "todo"]
# }


def menu_general():
    # Ingresar usuario y contraseña / consultar, crear, modificar y eliminar
    while True:
        # ABM
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
        # ABM
        print("--                 Menu ABM                      --")
        print("-    1. Agregar película nueva                    -")
        print("-    2. Modificar película                        -")
        print("-    3. Eliminar película                         -")
        print("-    4. Consultar ultimas peliculas agregadas     -")
        print("-    0. Salir                                     -")
        print("---------------------------------------------------")
        opcion = input("Ingrese una opción: ")
        if opcion == '1':
            agregar_pelicula()
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
            buscar_por_titulo()

        elif opcion == '3':
            buscar_filmografia()

        elif opcion == '4':
            buscar_por_genero()

        elif opcion == '5':
            buscar_sinopsis()

        elif opcion == '6':
            buscar_peliculas_año()

        elif opcion == '7':
            buscar_filmografia_genero()

        elif opcion == '0':
            break

        else:
            print("Opción no válida. Reintente.")
            continue

# Métodos GET


def consultar_todas():
    respuesta = requests.get("http://localhost:8000/allMovies")
    sc.procesar_respuesta(respuesta)


def buscar_por_titulo() -> None:
    titulo = input("Ingrese un título: ")
    respuesta = requests.get(
        "http://localhost:8000/filteredMovies", params={"title": titulo})
    sc.procesar_respuesta(respuesta)


def buscar_filmografia() -> None:
    actor = input("Ingrese un actor: ")
    respuesta = requests.get(
        "http://localhost:8000/filmography", params={"name": actor})
    sc.procesar_respuesta(respuesta)


def buscar_por_genero() -> None:
    i = 0
    generos = []
    while (True):
        i += 1
        generos.append(input(f'Ingrese un género ({i}):'))
        opcion = input(
            '¿Desea seguir ingresando géneros? (S/N): ').strip().upper()
        if opcion == 'N':
            break
    respuesta = requests.get(
        "http://localhost:8000/moviesByGender", params={"generos": generos})
    sc.procesar_respuesta(respuesta)


def buscar_sinopsis() -> None:
    titulo = input("Ingrese un título: ")
    respuesta = requests.get(
        "http://localhost:8000/movieSinopsis", params={"title": titulo})
    sc.procesar_respuesta(respuesta)


def buscar_peliculas_año() -> None:
    '''
    Requiere: Input de un año
    Devuelve: Lista de películas de dicho año
    '''
    año = sc.validar_entero('Ingrese el año de estreno: ',
                            "Error: Ingrese un año válido")
    respuesta = requests.get(
        "http://localhost:8000/moviesByYear", params={"year": año})
    sc.procesar_respuesta(respuesta)


def buscar_filmografia_genero() -> None:
    actor = input('Ingrese un actor: ')
    genero = input('Ingrese un género: ')
    respuesta = requests.get(
        "http://localhost:8000/filmographyByGender", params={"name": actor, "gender": genero})
    sc.procesar_respuesta(respuesta)

# Metodos POST
# |-----------------------------------------------------------------------|
# | En los POST y DELETE como parámetro de los métodos hay que agregar:   |
# | "credentials: HTTPBasicCredentials = Depends(verificar_credenciales)" |
# | para que si las credenciales son correctas pueda usar los métodos y   |
# | si no entonces no se ejecutan                                         |
# |-----------------------------------------------------------------------|

# FastAPI interpreta cada parámetro con Depends() como una dependencia que se debe ejecutar antes de procesar el endpoint. Es como un filtro previo


def agregar_pelicula():
    permisos = verificar_permisos()
    if not permisos:
        return
    # Sacamos los magic strings en favor del uso de enums
    if not (Permiso.CREAR in permisos or Permiso.TODO in permisos):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    pelicula = sc.crear_pelicula()
    respuesta = requests.post("http://localhost:8000/agregarPelicula",
                              json=pelicula)
    sc.procesar_respuesta(respuesta)


def modificar_pelicula():
    pass


def borrar_pelicula():
    pass


def verificar_permisos() -> list[str]:
    usuario = input("Ingrese su usuario: ").strip()
    contraseña = input("Ingrese su contraseña: ").strip()
    # OJO: Agregar funcion de regex para creacion de usuarios y contraseña
    auth = HTTPBasicAuth(usuario, contraseña)
    r = requests.get("http://localhost:8000/verificarAcceso", auth=auth)
    if r.status_code != 200:
        print(f"Acceso denegado: {r.json().get('acceso')}")  # Mensaje de error
        return []  # Permite verificar si el usuario existe o las credenciales ingresadas son correctas
    else:
        print("Acceso concedido, bienvenido.")
        return r.json()


menu_general()


# OJO: Agregar paginado
# i=0 i=5 pagina 1 <- la pagina donde estamos
# i=5 i=10 pagina 2
# ...
# round(len()/5) <- numero de paginas
# round(len()/5)  - i=0+4, i=5+4, elemento[i]
