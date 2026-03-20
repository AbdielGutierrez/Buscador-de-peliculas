import requests
from bs4 import BeautifulSoup
import pandas as pd


def conection(url):
    """
    Realiza una petición HTTP a la URL dada y extrae
    las carpetas de películas disponibles.
    Retorna una lista de items o None si falla.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("[Error] No se pudo conectar al servidor. Verifique su conexión a internet.")
        return None
    except requests.exceptions.Timeout:
        print("[Error] La conexión tardó demasiado. Intente de nuevo.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[Error] El servidor respondió con un error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[Error] Ocurrió un problema con la solicitud: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        if not table:
            print("[Error] No se encontró contenido en esa dirección. Verifique el año ingresado.")
            return None

        links = table.find_all("a")
        items = [
            link.text for link in links
            if link.text not in ["Parent Directory"] and link.text.endswith("/")
        ]

        if not items:
            print("[Error] No se encontraron películas para ese año.")
            return None

        return items

    except Exception as e:
        print(f"[Error] No se pudo procesar la respuesta del servidor: {e}")
        return None


def conection_files(url):
    """
    Busca archivos .mp4 y .srt dentro de la URL de una película.
    Retorna un diccionario con las claves 'mp4' y 'srt' (o None si no se encuentra).
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("[Error] No se pudo conectar al servidor.")
        return None
    except requests.exceptions.Timeout:
        print("[Error] La conexión tardó demasiado.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[Error] El servidor respondió con un error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[Error] Ocurrió un problema con la solicitud: {e}")
        return None

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        if not table:
            print("[Error] No se encontró contenido en la página de la película.")
            return None

        links = table.find_all("a")
        archivos = {"mp4": None, "srt": None}

        for link in links:
            nombre = link.text.strip()
            if nombre.lower().endswith(".mp4"):
                archivos["mp4"] = nombre
            elif nombre.lower().endswith(".srt"):
                archivos["srt"] = nombre

        return archivos

    except Exception as e:
        print(f"[Error] No se pudo procesar el contenido de la película: {e}")
        return None


def show_dataf(items, content: str):
    """Muestra la lista de películas como un DataFrame."""
    pd.set_option("display.max_rows", None)
    df = pd.DataFrame(items, columns=["Películas"])
    print(f"\n{content}")
    print(df.to_string())
    print()