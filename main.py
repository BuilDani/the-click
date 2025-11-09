from core.reading import find_button, get_sc_total, get_gc_total
from core.sheet import update_sheet
from core.actions import human_click
from loguru import logger
from pathlib import Path
import time, random, threading, sys, mss
import pyautogui

ASSETS_DIR = Path("assets")

# --- Define aqui os passos do bot ---
# --- Define aqui os passos do bot ---
STEPS = [
    {"type":"click", "name": "nsou"},
    {"type":"click", "name": "continue"},
    {"type":"scroll"},
    {"type":"click", "name": "close"},
    {"type":"screenshot", "filename": "step_screenshot.png"},
    {"type":"wait for screenshot", "template": "assets/continue.png", "timeout": 10},
    {"type":"repeat", "steps": [{"type":"click", "name": "nsou"}], "times": 3},

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

        # Sempre tentar extrair moedas e atualizar sheet no início de cada loop
        sc = get_sc_total()
        gc = get_gc_total()
        if sc is not None and gc is not None:
            update_sheet(sc, gc)

        for step in STEPS:
            if stop_event.is_set() or not run_event.is_set():
                break
            if step["type"] == "click":
                target_path = ASSETS_DIR / f"{step['name']}.png"
                pos = find_button(target_path)


                if pos:
                    x, y = pos
                    logger.info(f"[{step['name']}] encontrado em ({x}, {y}) — clicando (modo humano)")
                    human_click(x, y)
                    logger.success(f"Passo '{step['name']} concluído.")
                    time.sleep(LOOP_SLEEP_AFTER_CLICK + random.uniform(0.5, 1.2))
                else:
                    logger.debug(f"[{step['name']}] não encontrado. Tentando novamente...")
                    time.sleep(LOOP_SLEEP_NO_TARGET + random.uniform(0.5, 1.2))

            elif step["type"] == "scroll":
                scroll_amount = random.randint(-600, -400)
                pyautogui.scroll(scroll_amount)
                time.sleep(LOOP_SLEEP_NO_TARGET + random.uniform(0.5, 1.2))

            elif step["type"] == "wait":
                wait_time = step.get("duration", 1.0)
                logger.info(f"Esperando por {wait_time} segundos...")
                time.sleep(wait_time)

            elif step["type"] == "screenshot":
                from core.screen import capture_screen
                filename = "latest_screenshot.png"  # Fixed name, overwrites
                img = capture_screen()
                img.save(filename)
                logger.info(f"Screenshot salvo em {filename}")

            elif step["type"] == "wait for screenshot":
                template = step.get("template")
                timeout = step.get("timeout", 10)
                start_time = time.time()
                while time.time() - start_time < timeout:
                    pos = find_button(template)
                    if pos:
                        logger.info(f"Template {template} encontrado após espera.")
                        break
                    time.sleep(0.5)
                else:
                    logger.warning(f"Timeout esperando por {template}")

            elif step["type"] == "repeat":
                sub_steps = step.get("steps", [])
                times = step.get("times", 1)
                for _ in range(times):
                    for sub_step in sub_steps:
                        # Recursivamente processar sub_step, mas simplificado aqui
                        if sub_step["type"] == "click":
                            target_path = ASSETS_DIR / f"{sub_step['name']}.png"
                            pos = find_button(target_path)
                            if pos:
                                x, y = pos
                                logger.info(f"[repeat {sub_step['name']}] encontrado em ({x}, {y}) — clicando")
                                human_click(x, y)
                                time.sleep(LOOP_SLEEP_AFTER_CLICK + random.uniform(0.5, 1.2))
                            else:
                                logger.debug(f"[repeat {sub_step['name']}] não encontrado")
                                time.sleep(LOOP_SLEEP_NO_TARGET + random.uniform(0.5, 1.2))
                        # Adicionar outros tipos se necessário
                    time.sleep(0.5)  # pausa entre repetições
        sc = get_sc_total()
        gc = get_gc_total()
        if sc is not None and gc is not None:
            update_sheet(sc, gc)


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
