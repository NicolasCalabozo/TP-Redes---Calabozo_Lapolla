import requests
from requests.auth import HTTPBasicAuth
from servicioCliente import procesar_respuesta, crear_pelicula
from utils import validar_entero, cadena_mayusculas, verificar_permisos_cliente
from modelos import Permiso, Rol

usuario_actual = None
contraseña_actual = None
permisos_usuario = []
usuario_rol = None
sesion_iniciada = False

BASE_URL = "http://192.168.1.70:8000"


def menu_general():
    global sesion_iniciada, usuario_actual, usuario_rol
    # Inicio de sesión
    while not sesion_iniciada:
        verificar_permisos()
    # Si el usuario no es admin o editor, solo puede hacer consultas
    if usuario_rol not in [Rol.ADMIN, Rol.EDITOR]:
        menu_consultas()
    # Si el usuario es admin o editor, puede acceder al menú general
    if usuario_rol in [Rol.ADMIN, Rol.EDITOR]:
        while True:
            print("--           General             --")
            print("-    1.  Menú de consultas        -")
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
    global usuario_rol

    if usuario_rol not in [Rol.ADMIN, Rol.EDITOR]:
        print("No posee los permisos suficientes para realizar esta acción")
        return

    while True:
        print("--                 Menú ABM                      --")
        print("-    1. Agregar película nueva                    -")
        print("-    2. Modificar película                        -")
        print("-    3. Eliminar película                         -")
        print("-    4. Consultar últimas películas agregadas     -")
        print("-    0. Salir                                     -")
        print("---------------------------------------------------")
        opcion = input("Ingrese una opción: ")

        if opcion == '1':
            agregar_pelicula()
        elif opcion == '2':
            modificar_pelicula()
        elif opcion == '3':
            eliminar_pelicula()
        elif opcion == '4':
            pass
            #OJO: Agregar un consultar_ultimas_peliculas()
        elif opcion == '0':
            return
        else:
            print("Opción no válida. Reintente.")

def menu_consultas():
    # Todas estas acciones son accesibles por todos los roles que tengan el permiso 'ver'
    # Asumimos que el permiso 'ver' es el por defecto al crear un usuario ya que es la funcionalidad principal
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
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(f"{BASE_URL}/allMovies", auth=auth)
    procesar_respuesta(respuesta)


def buscar_por_titulo() -> None:
    global permisos_usuario
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    titulo = input("Ingrese un título: ")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"{BASE_URL}/filteredMovies", params={"title": titulo}, auth=auth)
    procesar_respuesta(respuesta)

def buscar_filmografia() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    actor = input("Ingrese un actor: ")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"{BASE_URL}/filmography", params={"name": actor}, auth=auth)
    procesar_respuesta(respuesta)

def buscar_por_genero() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
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
        f"{BASE_URL}/moviesByGender", params={"generos": generos}, auth=auth)
    procesar_respuesta(respuesta)


def buscar_sinopsis() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    titulo = input("Ingrese un título: ")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"{BASE_URL}/movieSinopsis", params={"title": titulo}, auth=auth)
    procesar_respuesta(respuesta)


def buscar_peliculas_año() -> None:
    '''
    Requiere: Input de un año
    Devuelve: Lista de películas de dicho año
    '''
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    año = validar_entero('Ingrese el año de estreno: ',
                         "Error: Ingrese un año válido")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"{BASE_URL}/moviesByYear", params={"year": año}, auth=auth)
    procesar_respuesta(respuesta)


def buscar_filmografia_genero() -> None:
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return

    actor = input('Ingrese un actor: ')
    genero = input('Ingrese un género: ')
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.get(
        f"{BASE_URL}/filmographyByGender", params={"name": actor, "gender": genero}, auth=auth)
    procesar_respuesta(respuesta)


def agregar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.CREAR, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return

    pelicula = crear_pelicula()
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore

    # CORRECCIÓN: Se envía el diccionario de la película directamente, no un objeto anidado
    respuesta = requests.post(f"{BASE_URL}/agregarPelicula",
                              json=pelicula,
                              auth=auth)
    procesar_respuesta(respuesta)


def modificar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual

    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.EDITAR, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return

    titulo = input("Ingrese el título de la película a modificar: ").strip()
    año = validar_entero("Ingrese el año de estreno original: ",
                         "Error: Ingrese un año válido.")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    r = requests.get(
        f"{BASE_URL}/obtenerPeliculaPorId",
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
                f"{BASE_URL}/modificarPelicula/{id_pelicula}",
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


def eliminar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual

    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.ELIMINAR, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return

    titulo = input("Ingrese el título exacto de la película: ").strip()
    año = validar_entero("Ingrese el año de estreno: ",
                         "Error: Ingrese un año válido")
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.delete(
        f"{BASE_URL}/eliminarPelicula",
        params={"title": titulo, "year": año},
        auth=auth
    )
    procesar_respuesta(respuesta)


def verificar_permisos():
    global usuario_actual, contraseña_actual, permisos_usuario, sesion_iniciada, usuario_rol
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
        usuario_rol = r.json()['rol']
        permisos_usuario = r.json()['permisos']
        sesion_iniciada = True
        print("Acceso concedido, bienvenido.")

#mostrar_peliculas_paginadas("peliculasPorAño", {"titulo": "pepe", año: 2010})

def mostrar_peliculas_paginadas(endpoint: str, params: dict):
    global usuario_actual, contraseña_actual
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    pagina = 1
    while True:
        params_pagina = params.copy()
        params_pagina["pagina"] = pagina

        respuesta = requests.get(
            f"{BASE_URL}/{endpoint}", params=params_pagina, auth=auth)

        if respuesta.status_code != 200:
            print("Error al obtener datos:", respuesta.status_code)
            break

        datos = respuesta.json()
        resultados = datos.get("resultados", [])
        total_paginas = datos.get("totalPaginas", 1)
        pagina_actual = datos.get("pagina", 1)
        total_resultados = datos.get("totalResultados", 0)

        if not resultados:
            print("No hay resultados para mostrar.")
            break

        print(
            f"\nPágina {pagina_actual}/{total_paginas} - Total resultados: {total_resultados}")
        for id, pelicula in enumerate(resultados, start=1 + (pagina_actual - 1)*len(resultados)):
            print(f"{id}. {pelicula}")

        opciones = []
        if pagina_actual > 1:
            opciones.append("A: Página anterior")
        if pagina_actual < total_paginas:
            opciones.append("D: Página siguiente")
        opciones.append("S: Salir")
        opciones.append("N° de Página")

        print(" | ".join(opciones))
        opcion = cadena_mayusculas(input(
            "Seleccione una opción o ingrese número de página: "))

        if opcion == "D" and pagina_actual < total_paginas:
            pagina += 1
        elif opcion == "A" and pagina_actual > 1:
            pagina -= 1
        elif opcion == "S":
            break
        elif opcion.isdigit():
            num_pagina = int(opcion)
            if 1 <= num_pagina <= total_paginas:
                pagina = num_pagina
            else:
                print(
                    f"Número de página inválido. Debe estar entre 1 y {total_paginas}.")
        else:
            print("Opción no válida, intente nuevamente.")


if __name__ == "__main__":
    menu_general()
