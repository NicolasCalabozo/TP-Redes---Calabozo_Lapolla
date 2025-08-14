import requests
from fastapi import status
from utils import validar_opcion, validar_entero, cadena_mayusculas, salir
from modelos import Pelicula

import asyncio
import time
import httpx

def crear_pelicula():

    pelicula_nueva = {
        "title": "",
        "year": 0,  # Se inicializa en 0 para consistencia de tipo
        "cast": [],
        "genres": [],
        "extract": ""
    }

    # Bucle de menú interactivo
    while True:
        print("\n----- Menú de Creación de Película -----")
        print(f"1. Título: {pelicula_nueva.get('title') or 'No ingresado'}")
        print(f"2. Año: {pelicula_nueva.get('year') or 'No ingresado'}")
        print(f"3. Elenco: {', '.join(pelicula_nueva.get('cast', [])) or 'No ingresado'}")
        print(f"4. Géneros: {', '.join(pelicula_nueva.get('genres', [])) or 'No ingresado'}")
        print(f"5. Sinopsis: {pelicula_nueva.get('extract') or 'No ingresada'}")
        print("---------------------------------------")
        print("6. Guardar película")
        print("0. Cancelar y salir")

        opcion = input("Seleccione el campo a ingresar/modificar (1-5) o una acción (6, 0): ").strip()

        if opcion == '1':
            pelicula_nueva["title"] = input("Ingrese el nuevo título: ").strip()
        elif opcion == '2':
            pelicula_nueva["year"] = validar_entero("Ingrese el nuevo año: ", "Error: Año inválido.")
        elif opcion == '3':
            elenco_str = input("Ingrese el nuevo elenco separado por coma: ")
            pelicula_nueva["cast"] = [a.strip() for a in elenco_str.split(',')]
        elif opcion == '4':
            generos_str = input("Ingrese los nuevos géneros separados por coma: ")
            pelicula_nueva["genres"] = [g.strip() for g in generos_str.split(',')]
        elif opcion == '5':
            pelicula_nueva["extract"] = input("Ingrese la nueva sinopsis: ")
        elif opcion == '6':
            if not pelicula_nueva["title"] or not pelicula_nueva["year"]:
                print("\n¡Error! El título y el año son campos obligatorios para guardar.")
                input("Presione Enter para continuar...")
                continue
            
            pelicula_a_crear = Pelicula(**pelicula_nueva)
            print("Datos de la película listos para ser guardados.")
            return pelicula_a_crear
        elif opcion == '0':
            print("Creación cancelada.")
            return None
        else:
            print("Opción inválida. Intente nuevamente.")

# OJO: Completar método de modificar

def modificar_pelicula():
    # pelicula['title'] = nuevo nombre
    pass

def procesar_respuesta(respuesta: requests.Response) -> None:
    datos = respuesta.json()
    if respuesta.status_code != requests.codes.ok:
        print(
            f"Error HTTP {respuesta.status_code}: {datos.get('error', 'Error desconocido')}")
        return
    print(datos.get("contenido"))

# OJO: Agregar metodo para retornar la pelicula con indice

def devolver_pelicula_con_indice() -> int:
    return 0


def seleccionar_generos(lista_generos: list[str]) -> list[str]:
    seleccionados = set()
    while True:
        print("\nSeleccione los géneros deseados (S para Salir):")
        
        for i in range(0, len(lista_generos), 5):
            fila = lista_generos[i:i+5]
            fila_marcada = []
            for j, genero in enumerate(fila, start=i+1):
                marcado = "(X)" if genero in seleccionados else "   "
                fila_marcada.append(f"{j}) {genero} {marcado}")
            print("\t".join(fila_marcada))

        opcion = input("Seleccione número: ").strip()
        
        if salir(opcion):
            break

        if not opcion.isdigit() or not (1 <= int(opcion) <= len(lista_generos)):
            print("Opción inválida, intente nuevamente.")
            continue

        id = int(opcion) - 1
        genero = lista_generos[id]

        if genero in seleccionados:
            seleccionados.remove(genero)
        else:
            seleccionados.add(genero)

    return list(seleccionados)

async def bombardear(url: str, rps: int, duracion: int, auth: tuple[str, str]):
    """
    Envía ráfagas de peticiones a una URL para probar el limitador de la API.

    Args:
        url (str): La URL completa del endpoint a probar.
        rps (int): El número de peticiones por segundo a enviar.
        duracion (int): El tiempo total en segundos que durará la prueba.
        auth (Tuple[str, str]): Una tupla con (usuario, contraseña) para la autenticación.
    """
    intervalo = 1.0 / rps
    print(f"\nIniciando bombardeo a {url}...")
    print(f"Configuración: {rps} peticiones/segundo durante {duracion} segundos.")
    
    async with httpx.AsyncClient() as cliente:
        fin_prueba = time.perf_counter() + duracion
        enviadas = exitosas = errores_cliente = errores_servidor = 0

        while time.perf_counter() < fin_prueba:
            inicio_peticion = time.perf_counter()
            try:
                # Se incluye la autenticación en la petición
                resp = await cliente.get(url, auth=auth, timeout=10)
                if resp.status_code == 429: # Error "Too Many Requests"
                    errores_servidor += 1
                elif resp.status_code >= 400:
                    errores_cliente += 1
                else:
                    exitosas += 1
            except Exception as e:
                errores_cliente += 1
            
            enviadas += 1
            transcurrido = time.perf_counter() - inicio_peticion
            
            # Espera el tiempo restante para mantener la tasa de RPS
            await asyncio.sleep(max(0, intervalo - transcurrido))

    print("\n--- Resultados del Bombardeo ---")
    print(f"Peticiones totales enviadas: {enviadas}")
    print(f"Respuestas exitosas (2xx): {exitosas}")
    print(f"Errores del limitador (429): {errores_servidor}")
    print(f"Otros errores (cliente/timeout): {errores_cliente}")
    print("---------------------------------")