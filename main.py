import os
import requests
from conection import conection, conection_files, show_dataf

BASE_URL = "https://visuales.uclv.cu/Peliculas/Extranjeras/"
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")


def obtener_anio():
    """Solicita y valida el año ingresado por el usuario."""
    while True:
        anio = input("Ingrese el año en que salio su pelicula: ").strip()
        if anio.isdigit() and 1900 <= int(anio) <= 2100:
            return anio
        print("[Error] Por favor ingrese un año válido (ej: 2023).")


def seleccionar_pelicula(lista):
    """Solicita y valida el índice de película elegido por el usuario."""
    while True:
        try:
            indice = int(input("Elija su película deseada (número de índice): "))
            if 0 <= indice < len(lista):
                return indice
            print(f"[Error] Ingrese un número entre 0 y {len(lista) - 1}.")
        except ValueError:
            print("[Error] Debe ingresar un número entero.")


def descargar_archivo(url, nombre_archivo, destino):
    """
    Descarga un archivo desde una URL y lo guarda en la carpeta destino.
    Muestra el progreso de la descarga.
    """
    ruta_destino = os.path.join(destino, nombre_archivo)

    # Si el archivo ya existe, preguntar si sobreescribir
    if os.path.exists(ruta_destino):
        respuesta = input(f"'{nombre_archivo}' ya existe en Downloads. ¿Sobreescribir? (s/n): ").strip().lower()
        if respuesta != "s":
            print(f"Descarga de '{nombre_archivo}' omitida.")
            return

    print(f"Descargando: {nombre_archivo}")

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        descargado = 0
        bloque = 1024 * 1024  # 1 MB

        with open(ruta_destino, "wb") as f:
            for chunk in response.iter_content(chunk_size=bloque):
                if chunk:
                    f.write(chunk)
                    descargado += len(chunk)
                    if total:
                        porcentaje = descargado / total * 100
                        print(f"  {porcentaje:.1f}% ({descargado / 1024 / 1024:.1f} MB / {total / 1024 / 1024:.1f} MB)", end="\r")

        print(f"\nArchivo guardado en: {ruta_destino}")

    except requests.exceptions.ConnectionError:
        print(f"\n[Error] Se perdió la conexión al descargar '{nombre_archivo}'.")
    except requests.exceptions.Timeout:
        print(f"\n[Error] La descarga de '{nombre_archivo}' tardó demasiado.")
    except requests.exceptions.HTTPError as e:
        print(f"\n[Error] No se pudo descargar '{nombre_archivo}': {e}")
    except OSError as e:
        print(f"\n[Error] No se pudo guardar el archivo en disco: {e}")


def main():
    print("=" * 50)
    print("       BUSCADOR DE PELICULAS - UCLV")
    print("=" * 50)

    # Paso 1: obtener año
    anio = obtener_anio()
    url_anio = f"{BASE_URL}{anio}/"

    print("Buscando peliculas, espere un momento...")

    # Paso 2: obtener lista de películas
    peliculas = conection(url_anio)
    if peliculas is None:
        return

    show_dataf(peliculas, f"Peliculas disponibles del año {anio}:")

    # Paso 3: seleccionar película
    indice = seleccionar_pelicula(peliculas)
    pelicula = peliculas[indice]
    pelicula_url = pelicula.replace(" ", "%20")
    url_pelicula = f"{url_anio}{pelicula_url}"

    print(f"\nPelicula seleccionada: {pelicula.rstrip('/')}")
    print(f"URL: {url_pelicula}")

    # Paso 4: buscar archivos dentro de la película
    print("\nBuscando archivos de la pelicula...")
    archivos = conection_files(url_pelicula)

    if archivos is None:
        return

    if not archivos["mp4"] and not archivos["srt"]:
        print("[Aviso] No se encontraron archivos .mp4 ni .srt en esta película.")
        print(f"Puede acceder manualmente en: {url_pelicula}")
        return

    # Paso 5: mostrar archivos encontrados y confirmar descarga
    print("\nArchivos encontrados:")
    if archivos["mp4"]:
        print(f"  [mp4] {archivos['mp4']}")
    else:
        print("  [mp4] No encontrado")

    if archivos["srt"]:
        print(f"  [srt] {archivos['srt']}")
    else:
        print("  [srt] No encontrado")

    respuesta = input("\n¿Desea descargar los archivos en su carpeta Downloads? (s/n): ").strip().lower()
    if respuesta != "s":
        print("Descarga cancelada.")
        print(f"Puede acceder a la pelicula en: {url_pelicula}")
        return

    # Paso 6: descargar archivos
    print(f"\nGuardando en: {DOWNLOADS_FOLDER}\n")

    if archivos["mp4"]:
        url_mp4 = f"{url_pelicula}{archivos['mp4'].replace(' ', '%20')}"
        descargar_archivo(url_mp4, archivos["mp4"], DOWNLOADS_FOLDER)

    if archivos["srt"]:
        url_srt = f"{url_pelicula}{archivos['srt'].replace(' ', '%20')}"
        descargar_archivo(url_srt, archivos["srt"], DOWNLOADS_FOLDER)

    print("\nProceso completado.")
    print("=" * 50)


if __name__ == "__main__":
    main()