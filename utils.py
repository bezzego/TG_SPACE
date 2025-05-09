from urllib.parse import urlsplit, unquote
import os.path

def get_file_extension(url: str) -> str:
    path = urlsplit(url).path
    path = unquote(path)
    filename = os.path.split(path)[1]
    _, ext = os.path.splitext(filename)
    return ext