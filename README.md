# Cumaun Cassino Bot

An image-based automation bot, designed to perform various tasks using keyboard and mouse interactions. It supports both fast and human-like actions, with modular steps for flexibility.

## Features

- **Image Recognition**: Uses OpenCV template matching to detect buttons and elements on screen.
- **Human-Like Actions**: Simulates natural mouse movements with Bezier curves for anti-detection.
- **Modular Steps**: Define custom sequences of actions in a JSON-like structure.
- **Screenshot Capture**: Save screenshots during automation.
- **Coin Extraction**: Automatically reads Silver Coins (SC) and Gold Coins (GC) from the screen using OCR.
- **Google Sheets Integration**: Updates a Google Sheet with coin totals and timestamps, only when values change and on new days.
- **Keyboard Controls**: Pause/Resume with 'P', Stop with 'ESC'.
- **Multi-threading**: Runs automation in a separate thread for responsiveness.

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Install additional OCR library: `pip install pytesseract` and download Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki.
4. Set up Google Sheets API: Place your service account JSON key as `kassbot-476316-158a001cb014.json` in the root directory.
5. Ensure assets (button images) are in the `assets/` folder.

## Usage

Run the bot with: `python main.py`

The bot will start automatically and execute the defined STEPS in a loop. Use 'P' to pause/resume, 'ESC' to stop.

## Step Types

The bot's behavior is defined by a list of STEPS in `main.py`. Each step is a dictionary with a "type" key. Supported types:

### "click"
Clicks on a button detected via image template.

- **Parameters**:
  - `"name"`: (required) Name of the button image file (without .png) in `assets/`.
- **Example**:
  ```python
  {"type": "click", "name": "continue"}
  ```
- **Behavior**: Searches for `assets/continue.png` on screen. If found, performs a human-like click at the center. Retries if not found.

### "scroll"
Scrolls the screen.

- **Parameters**: None (uses random scroll amount).
- **Example**:
  ```python
  {"type": "scroll"}
  ```
- **Behavior**: Scrolls down by a random amount (-600 to -400 pixels) to simulate natural scrolling.

### "wait"
Waits for a specified duration.

- **Parameters**:
  - `"duration"`: (optional) Seconds to wait (default: 1.0).
- **Example**:
  ```python
  {"type": "wait", "duration": 2.5}
  ```
- **Behavior**: Pauses execution for the given time.

### "screenshot"
Captures and saves a screenshot.

- **Parameters**:
  - `"filename"`: (optional) Output filename (default: "screenshot.png").
- **Example**:
  ```python
  {"type": "screenshot", "filename": "step_screenshot.png"}
  ```
- **Behavior**: Captures the full screen and saves as PNG.

### "wait for screenshot"
Waits until a specific template is detected on screen.

- **Parameters**:
  - `"template"`: (required) Path to the template image (e.g., "assets/continue.png").
  - `"timeout"`: (optional) Max seconds to wait (default: 10).
- **Example**:
  ```python
  {"type": "wait for screenshot", "template": "assets/continue.png", "timeout": 15}
  ```
- **Behavior**: Polls the screen every 0.5 seconds for the template. Logs success or timeout warning.

### "repeat"
Repeats a sub-list of steps multiple times.

- **Parameters**:
  - `"steps"`: (required) List of sub-steps to repeat (supports "click", etc.).
  - `"times"`: (required) Number of repetitions.
- **Example**:
  ```python
  {"type": "repeat", "steps": [{"type": "click", "name": "nsou"}], "times": 3}
  ```
- **Behavior**: Executes the sub-steps N times, with a 0.5s pause between repetitions. Currently supports "click" sub-steps.

## Coin Reading and Sheet Update

- **Automatic Extraction**: At the start of each loop, the bot attempts to read SC and GC from the screen using OCR.
- **Sheet Update**: If both values are found, updates Google Sheet only if:
  - Coin values have changed from the last entry.
  - The date is at least 1 day after the last entry.
- **Sheet Columns**: Silver Coins, Gold Coins, Data (mm/dd/yy hh:mm).
- **OCR Requirements**: Requires pytesseract and Tesseract OCR installed. Searches for patterns like "SC 6.25" or "GC 2,850,000".

## Configuration

- **STEPS**: Edit the list in `main.py` to customize actions.
- **Assets**: Place button images in `assets/` (e.g., nsou.png, continue.png).
- **Thresholds**: Adjust `TEMPLATE_MATCH_THRESHOLD` in `core/reading.py` for detection sensitivity.
- **Delays**: Modify `LOOP_SLEEP_*` in `main.py` for timing.

## Dependencies

- opencv-python
- pyautogui
- loguru
- pillow
- mss
- keyboard
- pytesseract
- gspread
- oauth2client

## Notes

- The bot runs in a loop, repeating STEPS indefinitely until stopped.
- Ensure the game window is visible and not obstructed for accurate detection.
- For production, consider running in a virtual environment or VM to avoid interference.
