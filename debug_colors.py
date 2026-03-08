import cv2
import numpy as np
from mss import mss

# Ajuste conforme sua tela
ROI = {
    "left": -1376,
    "top": 536,
    "width": 619,
    "height": 6716
}

sct = mss()

# HSV ranges iniciais
BLUE_LOWER = np.array([95, 50, 20])
BLUE_UPPER = np.array([130, 255, 255])

RED_LOWER_1 = np.array([0, 120, 70])
RED_UPPER_1 = np.array([10, 255, 255])
RED_LOWER_2 = np.array([160, 120, 70])
RED_UPPER_2 = np.array([180, 255, 255])

while True:
    img = np.array(sct.grab(ROI))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blue_mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
    red_mask = (
        cv2.inRange(hsv, RED_LOWER_1, RED_UPPER_1) |
        cv2.inRange(hsv, RED_LOWER_2, RED_UPPER_2)
    )

    non_water = cv2.bitwise_not(blue_mask)

    cv2.imshow("Original", frame)
    cv2.imshow("Agua (Azul)", blue_mask)
    cv2.imshow("Vermelho (Boia)", red_mask)
    cv2.imshow("Nao Agua (Possiveis Peixes)", non_water)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()