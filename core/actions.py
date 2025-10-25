# core/actions.py
import pyautogui
import random
import time
from typing import Tuple
from .utils import bezier_path

# Desativa pausas automáticas do pyautogui
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

def human_click(x: int, y: int, steps: int = 35, min_speed: float = 0.02, max_speed: float = 0.08):
    """
    Move o mouse em uma curva Bezier simulando movimento humano
    e realiza um clique.

    Args:
        x, y: posição de destino
        steps: quantos pontos na curva (mais = mais suave)
        min_speed, max_speed: intervalo de duração entre movimentos
    """
    sx, sy = pyautogui.position()
    p0 = (sx, sy)
    p3 = (x + random.uniform(-3, 3), y + random.uniform(-3, 3))

    dx = abs(p3[0] - p0[0])
    dy = abs(p3[1] - p0[1])

    p1 = (p0[0] + dx * 0.3 + random.uniform(-20, 20), p0[1] + random.uniform(-20, 20))
    p2 = (p0[0] + dx * 0.6 + random.uniform(-20, 20), p0[1] + dy * 0.6 + random.uniform(-20, 20))

    path = bezier_path(p0, p1, p2, p3, steps=steps)

    for (xx, yy) in path:
        duration = random.uniform(min_speed, max_speed)
        try:
            pyautogui.moveTo(int(xx), int(yy), duration=duration)
        except Exception:
            pyautogui.moveTo(int(xx), int(yy))

    # pequena pausa antes e depois do clique (natural)
    time.sleep(random.uniform(0.05, 0.12))
    pyautogui.click()
    time.sleep(random.uniform(0.1, 0.25))
