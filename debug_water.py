import cv2
import numpy as np
from mss import mss
from window_utils import get_client_rect

WINDOW_TITLE = "Habbo Hotel: Origins"

LAKE_OFFSET = {
    "x": 145,
    "y": 335,
    "width": 470,
    "height": 150
}

# HSV da água (ajustável depois)
LOWER_WATER = np.array([90, 60, 40])
UPPER_WATER = np.array([130, 255, 255])

client = get_client_rect(WINDOW_TITLE)
sct = mss()

while True:
    region = {
        "left": client["left"] + LAKE_OFFSET["x"],
        "top": client["top"] + LAKE_OFFSET["y"],
        "width": LAKE_OFFSET["width"],
        "height": LAKE_OFFSET["height"]
    }

    img = np.array(sct.grab(region))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    water_mask = cv2.inRange(hsv, LOWER_WATER, UPPER_WATER)

    overlay = frame.copy()
    overlay[water_mask > 0] = (255, 0, 0)  # azul artificial

    cv2.imshow("AGUA (overlay azul)", overlay)
    cv2.imshow("MASK AGUA", water_mask)

    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()