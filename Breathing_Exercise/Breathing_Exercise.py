import tkinter as tk
from time import sleep

def breathe():
    while True:
        label.config(text="Breathe In")
        root.update()
        sleep(4)
        label.config(text="Hold")
        root.update()
        sleep(2)
        label.config(text="Breathe Out")
        root.update()
        sleep(4)

root = tk.Tk()
root.attributes("-topmost", True)
root.geometry("200x100")
root.title("Breathing Exercises")
label = tk.Label(root, text="Breathe In", font=("Arial", 30))
label.pack()
root.after(0, breathe)
root.mainloop()
