import cv2
import numpy as np
from mss import mss
from window_utils import get_client_rect

WINDOW_TITLE = "Habbo Hotel: Origins"

template = cv2.imread("fish_balloon.png", 0)
tw, th = template.shape[::-1]

client = get_client_rect(WINDOW_TITLE)
sct = mss()

while True:

    region = {
        "left": client["left"],
        "top": client["top"],
        "width": client["width"],
        "height": client["height"]
    }

    img = np.array(sct.grab(region))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= 0.8)

    debug = frame.copy()

    for pt in zip(*loc[::-1]):

        cv2.rectangle(
            debug,
            pt,
            (pt[0] + tw, pt[1] + th),
            (0,255,0),
            2
        )

        cv2.putText(
            debug,
            "PESCANDO",
            (pt[0], pt[1]-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,0),
            1
        )

    cv2.imshow("BALAO DETECTADO", debug)

    if cv2.waitKey(30) == 27:
        break

cv2.destroyAllWindows()