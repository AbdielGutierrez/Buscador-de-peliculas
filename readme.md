# Buscador de Películas

Script de terminal en Python para buscar y descargar películas del catálogo de **visuales.uclv.cu**, sin necesidad de navegar manualmente por el sitio.

---

## Requisitos

- Python 3.x
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
python main.py
```

El script te guía paso a paso:

1. Ingresa el **año** de la película
2. Elige tu película de la lista
3. Confirma la descarga — el `.mp4`/`.avi`/`.mkv` y el `.srt` se guardan automáticamente en tu carpeta `Downloads`

---

## Estructura

| Archivo            | Descripción                                  |
| ------------------ | -------------------------------------------- |
| `main.py`          | Flujo principal e interacción con el usuario |
| `conection.py`     | Web scraping y descarga de archivos          |
| `requirements.txt` | Dependencias del proyecto                    |

---

## Tecnologías

**Python** · **Requests** · **BeautifulSoup4** · **Pandas**

---

## Autor

**Abdiel Gutiérrez** — [GitHub](https://github.com/AbdielGutierrez)
