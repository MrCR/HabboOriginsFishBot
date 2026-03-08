import cv2
import numpy as np
from mss import mss
from window_utils import get_client_rect

WINDOW_TITLE = "Habbo Hotel: Origins"

client = get_client_rect(WINDOW_TITLE)

TEST_HEIGHT = 300
TEST_WIDTH = 1200

sct = mss()

y = 0  # começamos do topo REAL do jogo

while True:
    region = {
        "left": client["left"],
        "top": client["top"] + y,
        "width": TEST_WIDTH,
        "height": TEST_HEIGHT
    }

    img = np.array(sct.grab(region))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    cv2.putText(
        frame,
        f"y offset = {y}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("CALIBRACAO Y", frame)

    key = cv2.waitKey(30)

    if key == ord('w'):
        y -= 5
    elif key == ord('s'):
        y += 5
    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()
print("Y FINAL =", y)