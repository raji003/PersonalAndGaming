import cv2
import numpy as np
from ultralytics import YOLO
import pyautogui
from mss import mss
import time
import keyboard  # pip install keyboard

# -----------------------
# CONFIGURATION
# -----------------------
MODEL_PATH = "yolov8n.pt"
TARGET_CLASS = "person"
SMOOTHING = 0.15  # Lower = faster, higher = slower
MONITOR = {"top": 200, "left": 200, "width": 1280, "height": 720}
FPS_CAP = 60
TOGGLE_KEY = "p"

# -----------------------
# INITIALIZATION
# -----------------------
model = YOLO(MODEL_PATH)
sct = mss()

aimbot_enabled = True
prev_target = None
screen_center = (MONITOR["width"] // 2, MONITOR["height"] // 2)

def get_screen():
    """Capture screen region as BGR"""
    sct_img = sct.grab(MONITOR)
    img = np.array(sct_img)
    return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

def get_target_box(results):
    """Return center coordinates of closest target to crosshair"""
    best_dist = float("inf")
    target_center = None
    
    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()
        for i, c in enumerate(classes):
            if model.names[int(c)] == TARGET_CLASS:
                x1, y1, x2, y2 = boxes[i]
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                dist = np.hypot(cx - screen_center[0], cy - screen_center[1])
                if dist < best_dist:
                    best_dist = dist
                    target_center = (cx, cy)
    return target_center

def move_mouse_smooth(target, prev_target):
    """Move mouse with smoothing and simple linear prediction"""
    if target is None:
        return prev_target
    
    current_pos = pyautogui.position()
    dx = target[0] - screen_center[0]
    dy = target[1] - screen_center[1]
    
    # Optional prediction: small multiplier on movement
    if prev_target:
        dx += (target[0] - prev_target[0]) * 0.3
        dy += (target[1] - prev_target[1]) * 0.3
    
    new_x = current_pos[0] + dx * SMOOTHING
    new_y = current_pos[1] + dy * SMOOTHING
    pyautogui.moveTo(new_x, new_y)
    
    return target

# -----------------------
# MAIN LOOP
# -----------------------
while True:
    # Toggle aimbot
    if keyboard.is_pressed(TOGGLE_KEY):
        aimbot_enabled = not aimbot_enabled
        print(f"Aimbot Enabled: {aimbot_enabled}")
        time.sleep(0.3)  # Prevent rapid toggling

    start_time = time.time()
    screen = get_screen()
    results = model.predict(screen, verbose=False)
    
    if aimbot_enabled:
        target = get_target_box(results)
        prev_target = move_mouse_smooth(target, prev_target)
    
    # Debug window
    cv2.imshow("Screen", screen)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    # FPS control
    elapsed = time.time() - start_time
    if elapsed < 1 / FPS_CAP:
        time.sleep((1 / FPS_CAP) - elapsed)

cv2.destroyAllWindows()
