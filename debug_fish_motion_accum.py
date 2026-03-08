import cv2
import numpy as np
from mss import mss
from collections import deque
from window_utils import get_client_rect

WINDOW_TITLE = "Habbo Hotel: Origins"

LAKE_OFFSET = {
    "x": 145,
    "y": 335,
    "width": 470,
    "height": 150
}

LOWER_WATER = np.array([90, 60, 40])
UPPER_WATER = np.array([130, 255, 255])

client = get_client_rect(WINDOW_TITLE)
sct = mss()

prev_gray = None
motion_history = deque(maxlen=6)

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

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is None:
        prev_gray = gray
        continue

    diff = cv2.absdiff(gray, prev_gray)

    motion = cv2.threshold(diff, 8, 255, cv2.THRESH_BINARY)[1]
    motion = cv2.bitwise_and(motion, water_mask)

    kernel = np.ones((3,3), np.uint8)
    motion = cv2.morphologyEx(motion, cv2.MORPH_DILATE, kernel)

    motion_history.append(motion)

    if len(motion_history) < motion_history.maxlen:
        prev_gray = gray
        continue

    accum = np.sum(motion_history, axis=0).astype(np.uint8)

    contours, _ = cv2.findContours(
        accum,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    debug = frame.copy()

    for c in contours:

        area = cv2.contourArea(c)

        if 80 < area < 2000:

            x,y,w,h = cv2.boundingRect(c)

            cv2.rectangle(
                debug,
                (x,y),
                (x+w,y+h),
                (0,255,0),
                2
            )

    cv2.imshow("PEIXE (movimento acumulado)", debug)
    cv2.imshow("ACCUM MOTION", accum)

    prev_gray = gray

    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()