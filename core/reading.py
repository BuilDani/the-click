# core/reading.py
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
from .screen import capture_screen
from .utils import ensure_bgr_np
from typing import Union
from loguru import logger

TEMPLATE_MATCH_THRESHOLD = 0.80  # ajusta conforme tua necessidade



def find_button(template_path: Union[Path, str], threshold: float = TEMPLATE_MATCH_THRESHOLD) -> Optional[Tuple[int, int]]:

    """
    Procura o template na tela atual e retorna (center_x, center_y) em coordenadas de tela.
    Retorna None se não achar.
    """
    # normaliza Path/str
    tpl_path = Path(template_path)
    if not tpl_path.exists():
        raise FileNotFoundError(f"Template não existe: {tpl_path}")

    # captura tela (numpy BGR)
    screen_np = ensure_bgr_np(capture_screen())

    # carrega template
    tpl = cv2.imread(str(tpl_path), cv2.IMREAD_COLOR)
    if tpl is None:
        raise RuntimeError(f"Falha ao abrir template: {tpl_path}")

    # template matching
    res = cv2.matchTemplate(screen_np, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        tx, ty = max_loc
        h, w = tpl.shape[:2]
        center_x = tx + w // 2
        center_y = ty + h // 2
        return (center_x, center_y)
    return None

def get_sc_total():
    """
    Extrai o total de Silver Coins (SC) do screenshot salvo.
    Assume que o texto está em formato "SC X.XX" ou similar.
    Usa OCR básico com pytesseract (assumindo instalado).
    """
    try:
        import pytesseract
        from PIL import Image
        # Use the fixed screenshot file
        img_path = "latest_screenshot.png"
        screen_img = Image.open(img_path)
        # Converter para grayscale para melhor OCR
        gray = screen_img.convert('L')
        text = pytesseract.image_to_string(gray)
        # Procurar por padrão SC
        import re
        match = re.search(r'SC\s+([\d,]+\.?\d*)', text)
        if match:
            return float(match.group(1).replace(',', ''))
        return None
    except ImportError:
        logger.warning("pytesseract não instalado. Instale com pip install pytesseract e tesseract-ocr.")
        return None
    except Exception as e:
        logger.error(f"Erro ao extrair SC: {e}")
        return None


def get_gc_total():
    """
    Extrai o total de Gold Coins (GC) do screenshot salvo.
    Assume que o texto está em formato "GC XXX,XXX" ou similar.
    Usa OCR básico com pytesseract.
    """
    try:
        import pytesseract
        from PIL import Image
        # Use the fixed screenshot file
        img_path = "latest_screenshot.png"
        screen_img = Image.open(img_path)
        gray = screen_img.convert('L')
        text = pytesseract.image_to_string(gray)
        import re
        match = re.search(r'GC\s+([\d,]+\.?\d*)', text)
        if match:
            return float(match.group(1).replace(',', ''))
        return None
    except ImportError:
        logger.warning("pytesseract não instalado. Instale com pip install pytesseract e tesseract-ocr.")
        return None
    except Exception as e:
        logger.error(f"Erro ao extrair GC: {e}")
        return None
