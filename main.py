from core.reading import find_button
from core.actions import human_click
from loguru import logger
from pathlib import Path
import time, random, threading, sys

ASSETS_DIR = Path("assets")

# --- Define aqui os passos do bot ---
STEPS = [
    "target_button",
    "retry_button",
    
]

# flags e timers
run_event = threading.Event()
stop_event = threading.Event()

LOOP_SLEEP_NO_TARGET = 0.5
LOOP_SLEEP_AFTER_CLICK = 1.0

import keyboard

def keyboard_listener():
    paused = False
    while not stop_event.is_set():
        if keyboard.is_pressed("esc"):
            stop_event.set()
            logger.warning("Encerrando por tecla ESC...")
            break

        if keyboard.is_pressed("p"):
            if paused:
                run_event.set()
                logger.info("Bot retomado (P pressionado).")
            else:
                run_event.clear()
                logger.info("Bot pausado (P pressionado).")
            paused = not paused
            time.sleep(0.5)  # evita múltiplos triggers

# --- adiciona essa thread ---
keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
keyboard_thread.start()

def worker_loop():
    logger.info("Worker rodando... Pressione ESC para parar.")
    while not stop_event.is_set():
        if not run_event.is_set():
            time.sleep(0.2)
            continue

        for step_name in STEPS:
            target_path = ASSETS_DIR / f"{step_name}.png"
            pos = find_button(target_path)

            if pos:
                x, y = pos
                logger.info(f"[{step_name}] encontrado em ({x}, {y}) — clicando (modo humano)")
                human_click(x, y)
                logger.success(f"Passo '{step_name}' concluído.")
                time.sleep(LOOP_SLEEP_AFTER_CLICK + random.uniform(0.5, 1.2))
            else:
                logger.debug(f"[{step_name}] não encontrado. Tentando novamente...")
                time.sleep(LOOP_SLEEP_NO_TARGET + random.uniform(0.5, 1.2))

    logger.info("Worker finalizado.")


if __name__ == "__main__":
    logger.info("Inicializando...")
    run_event.set()  # executa automaticamente
    worker = threading.Thread(target=worker_loop, daemon=True)
    worker.start()

    try:
        while not stop_event.is_set():
            time.sleep(0.3)
    except KeyboardInterrupt:
        logger.warning("Encerrando...")
        stop_event.set()

    worker.join(timeout=2)
    logger.info("Programa finalizado.")
