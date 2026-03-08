import win32gui

def get_client_rect(title):
    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        raise Exception("Janela não encontrada")

    # retângulo da área cliente (0,0 até w,h)
    left, top, right, bottom = win32gui.GetClientRect(hwnd)

    # converte para coordenadas de tela
    tl = win32gui.ClientToScreen(hwnd, (left, top))
    br = win32gui.ClientToScreen(hwnd, (right, bottom))

    return {
        "left": tl[0],
        "top": tl[1],
        "width": br[0] - tl[0],
        "height": br[1] - tl[1]
    }