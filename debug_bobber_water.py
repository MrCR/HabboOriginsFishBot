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

# água
LOWER_WATER = np.array([90,60,40])
UPPER_WATER = np.array([130,255,255])

# objeto claro (boia)
LOWER_LIGHT = np.array([0,0,150])
UPPER_LIGHT = np.array([180,80,255])

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
    light_mask = cv2.inRange(hsv, LOWER_LIGHT, UPPER_LIGHT)

    # apenas objetos claros dentro da água
    bobber_mask = cv2.bitwise_and(light_mask, water_mask)

    kernel = np.ones((3,3),np.uint8)
    bobber_mask = cv2.morphologyEx(bobber_mask, cv2.MORPH_OPEN, kernel)

    contours,_ = cv2.findContours(
        bobber_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    debug = frame.copy()

    for c in contours:

        area = cv2.contourArea(c)

        if 8 < area < 120:

            x,y,w,h = cv2.boundingRect(c)

            cv2.rectangle(debug,(x,y),(x+w,y+h),(255,255,255),2)
            cv2.putText(debug,"BOIA",(x,y-4),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,(255,255,255),1)

    cv2.imshow("BOIA DETECTADA",debug)
    cv2.imshow("BOBBER MASK",bobber_mask)

    if cv2.waitKey(30)==27:
        break

cv2.destroyAllWindows()