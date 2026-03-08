import pyautogui
import time

print("=== POSICAO DO MOUSE ===")
print("Mova o mouse. Ctrl+C para sair.")

try:
    while True:
        x, y = pyautogui.position()
        print(f"X={x:4d}  Y={y:4d}", end="\r")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\nSaindo...")