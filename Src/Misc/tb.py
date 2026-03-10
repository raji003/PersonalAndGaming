import cv2
import pyautogui
import keyboard
import time
from ultralytics import YOLO
import numpy as np

# Load YOLOv8 model (pretrained)
model = YOLO("yolov8n.pt")  # small, fast model

# Settings
SCREEN_SCALE = 1.0  # downscale for speed
SMOOTHNESS = 1.0    # how smoothly the crosshair moves
CTRL_TOGGLE_KEY = "ctrl"

aimbot_enabled = False

def get_screen():
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # Resize for faster detection
    frame = cv2.resize(frame, (0,0), fx=SCREEN_SCALE, fy=SCREEN_SCALE)
    return frame

def move_mouse_smooth(target_x, target_y):
    current_x, current_y = pyautogui.position()
    # Move fraction of distance to target for smoothness
    new_x = current_x + (target_x - current_x) * SMOOTHNESS
    new_y = current_y + (target_y - current_y) * SMOOTHNESS
    pyautogui.moveTo(new_x, new_y)

print("Aimbot running... Toggle with Ctrl")

while True:
    if keyboard.is_pressed(CTRL_TOGGLE_KEY):
        aimbot_enabled = not aimbot_enabled
        print(f"Aimbot {'enabled' if aimbot_enabled else 'disabled'}")
        time.sleep(0.5)  # debounce toggle

    if not aimbot_enabled:
        time.sleep(0.01)
        continue

    frame = get_screen()
    results = model(frame)[0]  # get first result

    # Find person(s) detected
    persons = []
    for r in results.boxes:
        cls = int(r.cls[0])
        conf = float(r.conf[0])
        # YOLOv8 COCO class 0 = person
        if cls == 0 and conf > 0.5:
            x1, y1, x2, y2 = r.xyxy[0]
            cx = int((x1 + x2)/2 / SCREEN_SCALE)
            cy = int((y1 + y2)/2 / SCREEN_SCALE)
            persons.append((cx, cy))

    if persons:
        # Pick closest to screen center
        screen_w, screen_h = pyautogui.size()
        center_x, center_y = screen_w // 2, screen_h // 2
        target = min(persons, key=lambda p: (p[0]-center_x)**2 + (p[1]-center_y)**2)
        move_mouse_smooth(*target)
        pyautogui.click()  # optional triggerbot click

    time.sleep(0.01)
