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

LOWER_WATER = np.array([90, 60, 40])
UPPER_WATER = np.array([130, 255, 255])

# branco (boia)
LOWER_WHITE = np.array([0, 0, 200])
UPPER_WHITE = np.array([180, 40, 255])

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
    white_mask = cv2.inRange(hsv, LOWER_WHITE, UPPER_WHITE)

    contours, _ = cv2.findContours(
        white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    debug = frame.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area < 20 or area > 300:
            continue

        x, y, w, h = cv2.boundingRect(c)
        cx = x + w // 2
        cy = y + h // 2

        # valida se está sobre água
        if cy + 5 < water_mask.shape[0]:
            if water_mask[cy + 5, cx] > 0:
                cv2.rectangle(debug, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(debug, "BOIA", (x, y-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

    cv2.imshow("BOIA (branco + agua)", debug)
    cv2.imshow("MASK BRANCO", white_mask)

    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()