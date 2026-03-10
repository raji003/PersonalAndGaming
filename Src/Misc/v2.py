import torch
import cv2
import numpy as np
from mss import mss

# Load your local YOLOv8 model
model = torch.hub.load('ultralytics/yolov8', 'custom', path='roblox_model.pt')  # replace with your .pt file

# Screen capture setup
sct = mss()
monitor = sct.monitors[1]  # full primary monitor

while True:
    # Capture screen
    screen = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)

    # Run detection
    results = model(frame)

    # Draw bounding boxes
    for *xyxy, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, xyxy)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{model.names[int(cls)]} {conf:.2f}', (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow('Roblox Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cv2.destroyAllWindows()
