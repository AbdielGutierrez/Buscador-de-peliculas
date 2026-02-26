from conection import conection as conn, show_dataf as df
import pandas as pd


# URL base
year = input("Ingrese el año en que salio su pelicula: ")
print("Buscando peliculas, espere un momento...")
url = f"https://visuales.uclv.cu/Peliculas/Extranjeras/{year}/"
conn1 = conn(url)
df(conn1, f"Estas son las peliculas del año {year}")

# Selección de película
pelicula_deseada = int(input("Elija su película deseada (número de índice): "))
pelicula = conn1[pelicula_deseada]
pelicula_for = pelicula.replace(" ", "%20")
url_pelicula = f"{url}{pelicula_for}"
conn2 = conn(url_pelicula)
print(f"\n Su pelicula elegida es: {pelicula}")
print(f'Aqui tiene el enlace para ver su pelicula: {url_pelicula}')

