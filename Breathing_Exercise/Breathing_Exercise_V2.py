import tkinter as tk

def breathe():
    label.config(text="Breathe In")
    root.after(4000, hold)

def hold():
    label.config(text="Hold")
    root.after(2000, breathe_out)

def breathe_out():
    label.config(text="Breathe Out")
    root.after(4000, breathe)

root = tk.Tk()
root.attributes("-topmost", True)
root.geometry("200x100")
root.title("Breathing Exercises")
label = tk.Label(root, text="Breathe In", font=("Arial", 30))
label.pack()
root.after(0, breathe)
root.mainloop()
