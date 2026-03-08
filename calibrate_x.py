import cv2
import numpy as np
from mss import mss
from window_utils import get_client_rect

WINDOW_TITLE = "Habbo Hotel: Origins"

client = get_client_rect(WINDOW_TITLE)

y = 185          # <- valor que você já calibrou
height = 420     # altura razoável do lago (ajustável)

x = 0
width = 1200     # começa largo de propósito

sct = mss()

print("Controles:")
print("A / D = move X")
print("Q / E = ajusta WIDTH")
print("ESC = sair")

while True:
    region = {
        "left": client["left"] + x,
        "top": client["top"] + y,
        "width": width,
        "height": height
    }

    img = np.array(sct.grab(region))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    cv2.rectangle(frame, (0, 0), (width-1, height-1), (0, 255, 0), 2)

    cv2.putText(
        frame,
        f"x={x}  width={width}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("CALIBRACAO X", frame)

    key = cv2.waitKey(30)

    if key == ord('a'):
        x -= 5
    elif key == ord('d'):
        x += 5
    elif key == ord('q'):
        width -= 10
    elif key == ord('e'):
        width += 10
    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()

print("RESULTADO FINAL:")
print("X =", x)
print("WIDTH =", width)