import cv2
import numpy as np
from mss import mss
from window_utils import get_client_rect

WINDOW_TITLE = "Habbo Hotel: Origins"

client = get_client_rect(WINDOW_TITLE)

LAKE_OFFSET = {
    "x": 0,
    "y": 185,
    "width": 610,
    "height": 300
}

lake = {
    "left": client["left"] + LAKE_OFFSET["x"],
    "top": client["top"] + LAKE_OFFSET["y"],
    "width": LAKE_OFFSET["width"],
    "height": LAKE_OFFSET["height"]
}

sct = mss()

while True:
    img = np.array(sct.grab(lake))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    cv2.imshow("ROI LAGO (DEVE BATER EXATO)", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()