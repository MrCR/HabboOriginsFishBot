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

    # máscara da água
    water_mask = cv2.inRange(hsv, LOWER_WATER, UPPER_WATER)

    # bordas da imagem
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 40, 120)

    # só bordas dentro da água
    fish_edges = cv2.bitwise_and(edges, water_mask)

    # engrossa um pouco as bordas
    kernel = np.ones((3,3), np.uint8)
    fish_edges = cv2.dilate(fish_edges, kernel)

    contours, _ = cv2.findContours(
        fish_edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    debug = frame.copy()

    for c in contours:

        area = cv2.contourArea(c)

        if 40 < area < 400:

            x, y, w, h = cv2.boundingRect(c)

            ratio = w / float(h)

            # peixe tende a ser mais largo que alto
            if 0.5 < ratio < 3:

                cv2.rectangle(
                    debug,
                    (x, y),
                    (x+w, y+h),
                    (0,255,0),
                    2
                )

    cv2.imshow("PEIXES (bordas)", debug)
    cv2.imshow("FISH EDGES", fish_edges)

    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()