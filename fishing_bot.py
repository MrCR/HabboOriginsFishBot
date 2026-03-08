import cv2
import numpy as np
import time
import pyautogui
from mss import mss
from collections import deque
from window_utils import get_client_rect
import keyboard


WINDOW_TITLE = "Habbo Hotel: Origins"

LAKE_OFFSET = {
    "x": 145,
    "y": 270,
    "width": 470,
    "height": 215
}

# HSV da água
LOWER_WATER = np.array([90,60,40])
UPPER_WATER = np.array([130,255,255])


# template do balão
balloon_template = cv2.imread("fish_balloon.png",0)
tw, th = balloon_template.shape[::-1]


client = get_client_rect(WINDOW_TITLE)
sct = mss()

prev_gray = None
motion_history = deque(maxlen=6)

state = "SEARCHING"

target_pos = None

search_start_time = time.time()

# DEBUG
debug_mode = True


def toggle_debug():
    global debug_mode
    debug_mode = not debug_mode

    if not debug_mode:
        cv2.destroyAllWindows()

    print("DEBUG:", debug_mode)


keyboard.add_hotkey("F1", toggle_debug)


def reset_motion():

    global prev_gray, motion_history

    prev_gray = None
    motion_history.clear()


def detect_balloon(frame):

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray,balloon_template,cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= 0.80)

    for pt in zip(*loc[::-1]):
        return True

    return False


def detect_fish(frame):

    global prev_gray

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    water_mask = cv2.inRange(hsv,LOWER_WATER,UPPER_WATER)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    if prev_gray is None:
        prev_gray = gray
        return None

    diff = cv2.absdiff(gray,prev_gray)

    motion = cv2.threshold(diff,8,255,cv2.THRESH_BINARY)[1]
    motion = cv2.bitwise_and(motion,water_mask)

    kernel = np.ones((3,3),np.uint8)
    motion = cv2.dilate(motion,kernel)

    motion_history.append(motion)

    if len(motion_history) < motion_history.maxlen:
        prev_gray = gray
        return None

    accum = np.sum(motion_history,axis=0).astype(np.uint8)

    contours,_ = cv2.findContours(
        accum,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    prev_gray = gray

    for c in contours:

        area = cv2.contourArea(c)

        if 120 < area < 2000:

            x,y,w,h = cv2.boundingRect(c)

            cx = x + w//2
            cy = y + h//2

            return cx,cy

    return None


def click_lake(cx,cy):

    screen_x = client["left"] + LAKE_OFFSET["x"] + cx
    screen_y = client["top"] + LAKE_OFFSET["y"] + cy

    pyautogui.moveTo(screen_x,screen_y,0.2)
    pyautogui.click()



print("Fishing bot iniciado")
print("Pressione F1 para abrir o DEBUG")
# Aguarde 10 segundos para o usuário se preparar
print("Aguardando 10 segundos para preparação...")
time.sleep(10)

while True:

    region = {
        "left": client["left"] + LAKE_OFFSET["x"],
        "top": client["top"] + LAKE_OFFSET["y"],
        "width": LAKE_OFFSET["width"],
        "height": LAKE_OFFSET["height"]
    }

    img = np.array(sct.grab(region))
    frame = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)


    # ---------------- SEARCHING ----------------

    if state == "SEARCHING":

        if time.time() - search_start_time > 20:

            print("20s sem encontrar peixe — resetando busca")

            reset_motion()

            search_start_time = time.time()

            continue


        fish = detect_fish(frame)

        if fish:

            cx,cy = fish
            target_pos = (cx,cy)

            print("Peixe detectado, clicando")

            click_lake(cx,cy)

            state = "MOVING"

            move_time = time.time()

        if debug_mode and fish:
            cv2.circle(frame,(cx,cy),10,(0,255,0),2)


    # ---------------- MOVING ----------------

    elif state == "MOVING":

        if time.time() - move_time > 10:

            print("Segundo clique")

            cx,cy = target_pos

            click_lake(cx,cy)

            state = "WAITING_BITE"

            wait_time = time.time()


    # ---------------- WAITING BITE ----------------

    elif state == "WAITING_BITE":

        if detect_balloon(frame):

            print("Estado: pescando")

            state = "FISHING"

        elif time.time() - wait_time > 25:

            print("Falhou, reiniciando")

            state = "SEARCHING"


    # ---------------- FISHING ----------------

    elif state == "FISHING":

        if detect_balloon(frame):

            if debug_mode:
                cv2.putText(frame,"BALAO DETECTADO",(10,30),
                cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)

        else:

            print("Parou de pescar")

            reset_motion()

            time.sleep(2)

            state = "SEARCHING"
            search_start_time = time.time()


    # ---------------- DEBUG WINDOW ----------------

    if debug_mode:

        cv2.putText(
            frame,
            f"STATE: {state}",
            (10,20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,255),
            2
        )

        cv2.imshow("Fishing Debug",frame)

        cv2.waitKey(1)


    time.sleep(0.03)