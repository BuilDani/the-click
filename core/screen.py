# core/screen.py
from PIL import Image
import numpy as np
import mss

def capture_screen() -> Image.Image:
    """
    Retorna um PIL.Image com a captura da tela (monitor principal).
    """
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # monitor 1 = primary
        raw = sct.grab(monitor)
        img = Image.frombytes("RGB", raw.size, raw.rgb)
        return img
