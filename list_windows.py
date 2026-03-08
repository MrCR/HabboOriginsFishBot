import pygetwindow as gw

print("JANELAS ABERTAS:")
for w in gw.getAllTitles():
    if w.strip():
        print(w)