# core/utils.py
from typing import Tuple, List
import numpy as np
from PIL import Image

def bezier_path(p0: Tuple[float,float], p1: Tuple[float,float], p2: Tuple[float,float], p3: Tuple[float,float], steps: int = 30) -> List[Tuple[float,float]]:
    path = []
    for i in range(steps):
        t = i / (steps - 1)
        x = (1 - t)**3 * p0[0] + 3*(1 - t)**2 * t * p1[0] + 3*(1 - t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1 - t)**3 * p0[1] + 3*(1 - t)**2 * t * p1[1] + 3*(1 - t) * t**2 * p2[1] + t**3 * p3[1]
        path.append((x, y))
    return path

def ensure_bgr_np(img) -> np.ndarray:
    """
    Aceita PIL.Image ou numpy array. Retorna numpy BGR (OpenCV padrão).
    """
    if isinstance(img, Image.Image):
        arr = np.array(img.convert("RGB"))
        # PIL -> numpy cria RGB; OpenCV usa BGR
        arr = arr[:, :, ::-1].copy()
        return arr
    elif isinstance(img, np.ndarray):
        # assumir já em BGR
        return img
    else:
        raise TypeError("img deve ser PIL.Image ou numpy.ndarray")
