import requests
from requests.auth import HTTPBasicAuth
from servicioCliente import procesar_respuesta, crear_pelicula, bombardear
from utils import obtener_ip_local,validar_entero, validar_opcion, verificar_permisos_cliente, limpiar_consola, verificar_rol_cliente
from modelos import Permiso, Rol
import asyncio

usuario_actual :str | None = None
contraseña_actual: str | None = None
permisos_usuario = []
rol_usuario: str | None = None
sesion_iniciada = False

#Completar la URL para testing
BASE_URL = ""


def menu_general():
    global sesion_iniciada, usuario_actual, rol_usuario
    # Inicio de sesión
    while not sesion_iniciada:
        verificar_permisos()
    # Si el usuario no es admin o editor, solo puede hacer consultas
    if verificar_rol_cliente(rol_usuario, [Rol.USUARIO]):
        menu_consultas()
    # Si el usuario es admin o editor, puede acceder al menú general
    if verificar_rol_cliente(rol_usuario, [Rol.ADMIN, Rol.EDITOR]): 
        while True:
            limpiar_consola()
            print("--           General             --")
            print("-    1.  Menú de consultas        -")
            print("-    2.  Menú de ABM              -")
            print("-    0. Salir                     -")
            print("-----------------------------------")
            opcion = input("Ingrese una opción: ")
            if opcion == '1':
                limpiar_consola()
                menu_consultas()
            elif opcion == '2':
                limpiar_consola()
                menu_abm()
            elif opcion == '0':
                print("¡Hasta Luego!")
                break
            else:
                print("Opción no válida, intente nuevamente")
                input("Presione Enter para continuar...")
                limpiar_consola()
                continue


def menu_abm():
    global rol_usuario

    if not verificar_rol_cliente(rol_usuario, [Rol.ADMIN, Rol.EDITOR]):
        print("No posee los permisos suficientes para realizar esta acción")
        return

    while True:
        limpiar_consola()
        print("--                 Menú ABM                      --")
        print("-    1. Agregar película nueva                    -")
        print("-    2. Modificar película                        -")
        if verificar_rol_cliente(rol_usuario, [Rol.ADMIN]):
            print("-    3. Eliminar película                         -")
            print("-    4. Probar límite de peticiones (Stress Test) -")
        print("-    0. Salir                                     -")
        print("---------------------------------------------------")
        opcion = input("Ingrese una opción: ")

        if opcion == '1':
            limpiar_consola()
            agregar_pelicula()
        elif opcion == '2':
            limpiar_consola()
            modificar_pelicula()
        elif opcion == '3' and verificar_rol_cliente(rol_usuario, [Rol.ADMIN]):
            limpiar_consola()
            eliminar_pelicula()
        elif opcion == '4' and verificar_rol_cliente(rol_usuario, [Rol.ADMIN]):
            limpiar_consola()
            probar_limite_peticiones()
        elif opcion == '0':
            return
        else:
            print("Opción no válida, intente nuevamente")
            input("Presione Enter para continuar...")
            limpiar_consola()


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
            limpiar_consola()
            consultar_todas()

        elif opcion == '2':
            limpiar_consola()
            buscar_por_titulo()

        elif opcion == '3':
            limpiar_consola()
            buscar_filmografia()

        elif opcion == '4':
            limpiar_consola()
            buscar_por_genero()

        elif opcion == '5':
            limpiar_consola()
            buscar_sinopsis()

        elif opcion == '6':
            limpiar_consola()
            buscar_peliculas_año()

        elif opcion == '7':
            limpiar_consola()
            buscar_filmografia_genero()

        elif opcion == '0':
            limpiar_consola()
            break

        else:
            print("Opción no válida, intente nuevamente")
            input("Presione Enter para continuar...")
            limpiar_consola()


# Métodos GET

def consultar_todas():
    global permisos_usuario, usuario_actual, contraseña_actual

    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return

    mostrar_peliculas_paginadas("allMovies", params={})


def buscar_por_titulo() -> None:
    global permisos_usuario
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    titulo = input("Ingrese un título: ")
    mostrar_peliculas_paginadas("filteredMovies", {"title": titulo})


def buscar_filmografia() -> None:
    global permisos_usuario
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    actor = input("Ingrese un actor: ")
    mostrar_peliculas_paginadas("filmography", {"name": actor})


def buscar_por_genero() -> None:
    global permisos_usuario
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    generos = []
    i = 0
    while True:
        i += 1
        generos.append(input(f'Ingrese un género ({i}): '))
        if not validar_opcion("¿Desea seguir ingresando generos? (S/N): "):
            break
    mostrar_peliculas_paginadas("moviesByGender", {"generos": generos})


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
    input("Presione Enter para continuar...")
    limpiar_consola()


def buscar_peliculas_año() -> None:
    global permisos_usuario
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    año = validar_entero('Ingrese el año de estreno: ',
                         "Error: Ingrese un año válido")
    mostrar_peliculas_paginadas("moviesByYear", {"year": año})


def buscar_filmografia_genero() -> None:
    global permisos_usuario
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.VER, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    actor = input('Ingrese un actor: ')
    genero = input('Ingrese un género: ')
    mostrar_peliculas_paginadas("filmographyByGender", {
                                "name": actor, "gender": genero})


def agregar_pelicula():
    global permisos_usuario, usuario_actual, contraseña_actual
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.CREAR, Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción.")
        return
    pelicula = crear_pelicula()

    if pelicula is None:
        return

    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    respuesta = requests.post(f"{BASE_URL}/agregarPelicula",
                              json=pelicula.model_dump(),
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
    limpiar_consola()
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
            limpiar_consola()
        elif opcion == '2':
            pelicula_modificada["year"] = validar_entero(
                "Ingrese el nuevo año: ", "Error: Año inválido.")
            limpiar_consola()
        elif opcion == '3':
            elenco_str = input("Ingrese el nuevo elenco separado por coma: ")
            pelicula_modificada["cast"] = [a.strip()
                                           for a in elenco_str.split(',')]
            limpiar_consola()
        elif opcion == '4':
            generos_str = input(
                "Ingrese los nuevos géneros separados por coma: ")
            pelicula_modificada["genres"] = [g.strip()
                                             for g in generos_str.split(',')]
            limpiar_consola()
        elif opcion == '5':
            pelicula_modificada["extract"] = input(
                "Ingrese la nueva sinopsis: ")
            limpiar_consola()
        elif opcion == '6':
            respuesta = requests.put(
                f"{BASE_URL}/modificarPelicula/{id_pelicula}",
                json=pelicula_modificada,
                auth=auth
            )
            procesar_respuesta(respuesta)
            input("Presione Enter para continuar...")
            limpiar_consola()
            break
        elif opcion == '0':
            print("Modificación cancelada.")
            input("Presione Enter para continuar...")
            limpiar_consola()
            break
        else:
            print("Opción inválida. Intente nuevamente.")
            input("Presione Enter para continuar...")
            limpiar_consola()


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
    input("Presione enter para continuar...")


def verificar_permisos():
    global usuario_actual, contraseña_actual, permisos_usuario, sesion_iniciada, rol_usuario
    limpiar_consola()
    print("----             Log In            ---- ")
    usuario = input("Ingrese su usuario: ").strip()
    contraseña = input("Ingrese su contraseña: ").strip()
    auth = HTTPBasicAuth(usuario, contraseña)
    r = requests.post(f"{BASE_URL}/verificarAcceso", auth=auth)
    if r.status_code != 200:
        # Mensaje de error
        print(f"Acceso denegado: Credenciales incorrectas o usuario inexistente.")
        input("Presione Enter para continuar...")
        limpiar_consola()
    else:
        global permisos_usuario, sesion_iniciada, usuario_actual, contraseña_actual, rol_usuario
        usuario_actual = usuario
        contraseña_actual = contraseña
        permisos_usuario = r.json()['permisos']
        rol_usuario = r.json()['rol']
        sesion_iniciada = True
        print(f"Acceso concedido. ¡Bienvenido, {usuario}!")
        input("Presione Enter para continuar...")
        limpiar_consola()


def mostrar_peliculas_paginadas(endpoint: str, params: dict):
    global usuario_actual, contraseña_actual
    auth = HTTPBasicAuth(usuario_actual, contraseña_actual)  # type: ignore
    pagina = 1
    while True:
        limpiar_consola()
        params_pagina = params.copy()
        params_pagina["pagina"] = pagina

        respuesta = requests.get(
            f"{BASE_URL}/{endpoint}", params=params_pagina, auth=auth)

        if respuesta.status_code != 200:
            print("Error al obtener datos:", respuesta.status_code)
            break

        datos = respuesta.json()
        contenido = datos.get("contenido", "")
        total_paginas = datos.get("totalPaginas", 1)
        pagina_actual = datos.get("pagina", 1)
        total_resultados = datos.get("totalResultados", 0)

        if not contenido:
            print("No hay resultados para mostrar.")
            break

        print(
            f"\nPágina {pagina_actual}/{total_paginas} - Total resultados: {total_resultados}")
        print(contenido)

        opciones = []
        if total_paginas > 1:
            if pagina_actual > 1:
                opciones.append("A: Página anterior")
            if pagina_actual < total_paginas:
                opciones.append("D: Página siguiente")
            opciones.append("N° de Página")
        opciones.append("V: Volver")

        print(" | ".join(opciones))
        opcion = input(
            f"Seleccione una opción {'o ingrese número de página: ' if total_paginas > 1 else ': '}").strip().upper()

        if opcion == "D" and pagina_actual < total_paginas:
            pagina += 1
        elif opcion == "A" and pagina_actual > 1:
            pagina -= 1
        elif opcion == "V":
            limpiar_consola()
            break
        elif opcion.isdigit():
            num_pagina = int(opcion)

            if 1 <= num_pagina <= total_paginas:
                pagina = num_pagina
            else:
                print(
                    f"Número de página inválido. Debe estar entre 1 y {total_paginas}.")
                input("Presione Enter para continuar...")
                limpiar_consola()
        else:
            print("Opción no válida, intente nuevamente.")
            input("Presione Enter para continuar...")
            limpiar_consola()


def probar_limite_peticiones():
    """
    Pide al usuario los parámetros para la prueba de estrés
    y ejecuta la función de bombardeo.
    """
    global usuario_actual, contraseña_actual, BASE_URL
    if not permisos_usuario or not verificar_permisos_cliente(permisos_usuario, [Permiso.TODO]):
        print("No tiene los permisos necesarios para realizar esta acción (se requiere permiso de administrador).")
        input("Presione Enter para continuar...")
        return
    print("--- Prueba de Carga del Limitador de la API ---")

    # Pedimos el endpoint a bombardear
    endpoint = input("Ingrese el endpoint a probar (ej. /allMovies): ").strip()
    if not endpoint.startswith('/'):
        endpoint = '/' + endpoint

    url_completa = BASE_URL + endpoint

    # Pedimos los parámetros numéricos usando el validador
    rps = validar_entero(
        "Ingrese las peticiones por segundo (RPS): ", "Error: Debe ser un número entero.")
    duracion = validar_entero(
        "Ingrese la duración de la prueba en segundos: ", "Error: Debe ser un número entero.")

    # Preparamos la tupla de autenticación
    auth = (usuario_actual, contraseña_actual)

    # Ejecutamos la función asíncrona de bombardeo
    try:
        asyncio.run(bombardear(url_completa, rps,
                    duracion, auth))  # type: ignore
    except Exception as e:
        print(f"Ocurrió un error al ejecutar la prueba: {e}")

    input("\nPrueba finalizada. Presione Enter para continuar...")


if __name__ == "__main__":
    ip_local = obtener_ip_local()
    BASE_URL = f"http://{ip_local}:8000"
    menu_general()
