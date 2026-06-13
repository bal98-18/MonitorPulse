import os
import sys

def path_resource(path_relative):
    try:
        path_base = sys._MEIPASS
    except Exception:
        path_base = os.path.abspath(".")
    return os.path.join(path_base, path_relative)