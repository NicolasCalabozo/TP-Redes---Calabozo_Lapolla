import requests
from requests.auth import HTTPBasicAuth
from servicioCliente import procesar_respuesta, crear_pelicula
from utils import validar_entero, cadena_mayusculas
from modelos import Permiso

usuario_actual = None
contraseña_actual = None
permisos_usuario = []
sesion_iniciada = False


def menu_general():
    global sesion_iniciada
    while not sesion_iniciada:
        verificar_permisos()

    while True:
        print("--           General             --")
        # Permiso VER, TODO
        print("-    1.  Menú de consultas        -")
        # Permiso CREAR, MODIFICAR,ELIMINAR, TODO
        print("-    2.  Menú de ABM              -")
        print("-    0. Salir                     -")
        print("-----------------------------------")
        opcion = input("Ingrese una opción: ")
        if opcion == '1':
            menu_consultas()
        elif opcion == '2':
            menu_abm()
        elif opcion == '0':
            break
        else:
            print("Opción no válida. Reintente.")
            continue


def menu_abm():
    while True:
        # ABM
        print("--                 Menu ABM                      --")
        # Permiso CREAR
        print("-    1. Agregar película nueva                    -")
        # Permiso EDITAR
        print("-    2. Modificar película                        -")
        # Permiso ELIMINAR
        print("-    3. Eliminar película                         -")
        # Permiso VER
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
    global permisos_usuario
    if not permisos_usuario:
        return
    respuesta = requests.get("http://localhost:8000/allMovies")
    procesar_respuesta(respuesta)


def buscar_por_titulo() -> None:
    global permisos_usuario
    if not permisos_usuario:
        return
    titulo = input("Ingrese un título: ")
    respuesta = requests.get(
        "http://localhost:8000/filteredMovies", params={"title": titulo})
    procesar_respuesta(respuesta)


def buscar_filmografia() -> None:
    global permisos_usuario
    if not permisos_usuario:
        return
    actor = input("Ingrese un actor: ")
    respuesta = requests.get(
        "http://localhost:8000/filmography", params={"name": actor})
    procesar_respuesta(respuesta)


def buscar_por_genero() -> None:
    global permisos_usuario
    if not permisos_usuario:
        return
    i = 0
    generos = []
    while (True):
        i += 1
        generos.append(input(f'Ingrese un género ({i}):'))
        opcion = cadena_mayusculas(input(
            '¿Desea seguir ingresando géneros? (S/N): '))
        if opcion == 'N':
            break
    respuesta = requests.get(
        "http://localhost:8000/moviesByGender", params={"generos": generos})
    procesar_respuesta(respuesta)


def buscar_sinopsis() -> None:
    global permisos_usuario
    if not permisos_usuario:
        return
    titulo = input("Ingrese un título: ")
    respuesta = requests.get(
        "http://localhost:8000/movieSinopsis", params={"title": titulo})
    procesar_respuesta(respuesta)


def buscar_peliculas_año() -> None:
    '''
    Requiere: Input de un año
    Devuelve: Lista de películas de dicho año
    '''
    global permisos_usuario
    if not permisos_usuario:
        return
    año = validar_entero('Ingrese el año de estreno: ',
                            "Error: Ingrese un año válido")
    respuesta = requests.get(
        "http://localhost:8000/moviesByYear", params={"year": año})
    procesar_respuesta(respuesta)


def buscar_filmografia_genero() -> None:
    global permisos_usuario
    if not permisos_usuario:
        return
    actor = input('Ingrese un actor: ')
    genero = input('Ingrese un género: ')
    respuesta = requests.get(
        "http://localhost:8000/filmographyByGender", params={"name": actor, "gender": genero})
    procesar_respuesta(respuesta)


def agregar_pelicula():
    global permisos_usuario
    if not permisos_usuario:
        return
    # Sacamos los magic strings en favor del uso de enums
    if not (Permiso.CREAR in permisos_usuario or Permiso.TODO in permisos_usuario):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    pelicula = crear_pelicula()
    respuesta = requests.post("http://localhost:8000/agregarPelicula",
                              json={"pelicula": pelicula, "permisos": permisos_usuario})
    procesar_respuesta(respuesta)


def modificar_pelicula():
    # PUT
    pass


def borrar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    if not (Permiso.ELIMINAR in permisos_usuario or Permiso.TODO in permisos_usuario):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    titulo = input("Ingrese el título exacto de la película: ").strip()
    año = validar_entero("Ingrese el año de estreno: ", "Error: Ingrese un año válido")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual) # type: ignore
    respuesta = requests.delete(
        "http://localhost:8000/eliminarPelicula",
        params = {"title": titulo, "year": año, "permisos": permisos_usuario},
        auth = auth
    )
    procesar_respuesta(respuesta)


def verificar_permisos():
    usuario = input("Ingrese su usuario: ").strip()
    contraseña = input("Ingrese su contraseña: ").strip()
    # OJO: Agregar funcion de regex para creacion de usuarios y contraseña
    auth = HTTPBasicAuth(usuario, contraseña)
    r = requests.post("http://localhost:8000/verificarAcceso", auth=auth)
    if r.status_code != 200:
        print(f"Acceso denegado: {r.json().get('acceso')}")  # Mensaje de error
    else:
        global permisos_usuario, sesion_iniciada, usuario_actual
        usuario_actual = usuario
        permisos_usuario = r.json()['permisos']
        sesion_iniciada = True
        print("Acceso concedido, bienvenido.")


menu_general()


# OJO: Agregar paginado

