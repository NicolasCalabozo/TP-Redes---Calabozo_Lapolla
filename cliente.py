import requests
from requests.auth import HTTPBasicAuth
from servicioCliente import procesar_respuesta, crear_pelicula
from utils import validar_entero, cadena_mayusculas
from modelos import Permiso

usuario_actual = None
contraseña_actual = None
permisos_usuario = []
sesion_iniciada = False

BASE_URL = "192.168.1.70:8000"

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
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual) # type: ignore
    respuesta = requests.get(f"http://{BASE_URL}/allMovies", auth=auth)
    procesar_respuesta(respuesta)


def buscar_por_titulo() -> None:
    global permisos_usuario
    if not permisos_usuario:
        return
    titulo = input("Ingrese un título: ")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"http://{BASE_URL}/filteredMovies", params={"title": titulo}, auth=auth)
    procesar_respuesta(respuesta)


def buscar_filmografia() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    actor = input("Ingrese un actor: ")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"http://{BASE_URL}/filmography", params={"name": actor}, auth = auth)
    procesar_respuesta(respuesta)


def buscar_por_genero() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
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
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"http://{BASE_URL}/moviesByGender", params={"generos": generos}, auth=auth)
    procesar_respuesta(respuesta)


def buscar_sinopsis() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    titulo = input("Ingrese un título: ")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"http://{BASE_URL}/movieSinopsis", params={"title": titulo}, auth=auth)
    procesar_respuesta(respuesta)


def buscar_peliculas_año() -> None:
    '''
    Requiere: Input de un año
    Devuelve: Lista de películas de dicho año
    '''
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    año = validar_entero('Ingrese el año de estreno: ',
                         "Error: Ingrese un año válido")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"http://{BASE_URL}/moviesByYear", params={"year": año}, auth=auth)
    procesar_respuesta(respuesta)


def buscar_filmografia_genero() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    actor = input('Ingrese un actor: ')
    genero = input('Ingrese un género: ')
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"http://{BASE_URL}/filmographyByGender", params={"name": actor, "gender": genero}, auth=auth)
    procesar_respuesta(respuesta)


def agregar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    # Sacamos los magic strings en favor del uso de enums
    if not (Permiso.CREAR in permisos_usuario or Permiso.TODO in permisos_usuario):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    pelicula = crear_pelicula()
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual) # type: ignore
    respuesta = requests.post(f"http://{BASE_URL}/agregarPelicula",
                              json={"pelicula": pelicula}, auth=auth)
    procesar_respuesta(respuesta)


def modificar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual

    if not permisos_usuario or (Permiso.EDITAR not in permisos_usuario and Permiso.TODO not in permisos_usuario):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return

    titulo = input("Ingrese el título de la película a modificar: ").strip()
    año = validar_entero("Ingrese el año de estreno original: ",
                         "Error: Ingrese un año válido.")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    r = requests.get(
        f"http://{BASE_URL}/obtenerPeliculaPorId",
        params={"titulo": titulo, "año": año},
        auth=auth
    )
    if r.status_code != 200:
        procesar_respuesta(r)
        return
    contenido = r.json()["contenido"]
    pelicula_a_modificar = contenido["pelicula"]
    id_pelicula = contenido["id"]
    pelicula_modificada = pelicula_a_modificar.copy()

    while True:
        print("\n----- Menú de Modificación -----")
        print(f"1. Título actual: {pelicula_modificada.get('title')}")
        print(f"2. Año actual: {pelicula_modificada.get('year')}")
        print(
            f"3. Elenco actual: {', '.join(pelicula_modificada.get('cast', []))}")
        print(
            f"4. Géneros actuales: {', '.join(pelicula_modificada.get('genres', []))}")
        print(
            f"5. Sinopsis actual: {pelicula_modificada.get('extract', 'No disponible')}")
        print("-------------------------------")
        print("6. Guardar cambios y salir")
        print("0. Cancelar y salir")

        opcion = input(
            "Seleccione el campo a modificar (1-5) o una acción (6, 0): ").strip()

        if opcion == '1':
            pelicula_modificada["title"] = input(
                "Ingrese el nuevo título: ").strip()
        elif opcion == '2':
            pelicula_modificada["year"] = validar_entero(
                "Ingrese el nuevo año: ", "Error: Año inválido.")
        elif opcion == '3':
            elenco_str = input("Ingrese el nuevo elenco separado por coma: ")
            pelicula_modificada["cast"] = [a.strip()
                                           for a in elenco_str.split(',')]
        elif opcion == '4':
            generos_str = input(
                "Ingrese los nuevos géneros separados por coma: ")
            pelicula_modificada["genres"] = [g.strip()
                                             for g in generos_str.split(',')]
        elif opcion == '5':
            pelicula_modificada["extract"] = input(
                "Ingrese la nueva sinopsis: ")
        elif opcion == '6':
            respuesta = requests.put(
                f"http://{BASE_URL}/modificarPelicula/{id_pelicula}",
                json=pelicula_modificada,
                auth=auth
            )
            procesar_respuesta(respuesta)
            break
        elif opcion == '0':
            print("Modificación cancelada.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


def borrar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario:
        return
    if not (Permiso.ELIMINAR in permisos_usuario or Permiso.TODO in permisos_usuario):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    titulo = input("Ingrese el título exacto de la película: ").strip()
    año = validar_entero("Ingrese el año de estreno: ",
                         "Error: Ingrese un año válido")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.delete(
        f"http://{BASE_URL}/eliminarPelicula",
        params = {"title": titulo, "year": año},
        auth = auth
    )
    procesar_respuesta(respuesta)


def verificar_permisos():
    usuario = input("Ingrese su usuario: ").strip()
    contraseña = input("Ingrese su contraseña: ").strip()
    # OJO: Agregar funcion de regex para creacion de usuarios y contraseña
    auth = HTTPBasicAuth(usuario, contraseña)
    r = requests.post(f"http://{BASE_URL}/verificarAcceso", auth=auth)
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
