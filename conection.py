import requests
from bs4 import BeautifulSoup
import pandas as pd

def conection(url):
    # Hacer la petición
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Buscar la tabla y los enlaces
    table = soup.find("table")
    links = table.find_all("a") if table else []
    # Guardar solo las carpetas de películas
    items = [link.text for link in links if link.text not in ["Parent Directory"] and link.text.endswith("/")]
    return items

def show_dataf(items, content: str):
    # Crear DataFrame
    pd.set_option("display.max_rows", None)
    df = pd.DataFrame(items, columns=["Películas"])
    print(content)
    print(df)
