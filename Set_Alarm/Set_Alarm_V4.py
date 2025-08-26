import tkinter as tk
import datetime
import threading
import sys

try:
    import pystray
    from PIL import Image, ImageDraw
except ImportError:
    print("Please install: pip install pystray pillow")
    sys.exit(1)

class AlarmApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alarm App")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_to_tray)

        self.tray_icon = None
        self.tray_thread = None
        self.is_hidden = False

        # Current time label (unchanged)
        self.time_label = tk.Label(self.root, font=("Arial", 20))
        self.time_label.pack()

        # Alarm section (unchanged)
        self.alarm_frame = tk.Frame(self.root)
        self.alarm_frame.pack()

        self.alarm_time_label = tk.Label(self.alarm_frame, text="Alarm Time:", font=("Arial", 16))
        self.alarm_time_label.grid(row=0, column=0)

        self.alarm_time_entry = tk.Entry(self.alarm_frame, font=("Arial", 16))
        self.alarm_time_entry.grid(row=0, column=1)

        self.message_label = tk.Label(self.alarm_frame, text="Message:", font=("Arial", 16))
        self.message_label.grid(row=1, column=0)

        self.message_entry = tk.Entry(self.alarm_frame, font=("Arial", 16))
        self.message_entry.grid(row=1, column=1)

        self.set_alarm_button = tk.Button(self.alarm_frame, text="Set Alarm", font=("Arial", 16), command=self.set_alarm)
        self.set_alarm_button.grid(row=2, column=1)

        self.update_time()
        self.root.mainloop()

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def set_alarm(self):
        alarm_time = self.alarm_time_entry.get()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if alarm_time == current_time:
            message = self.message_entry.get()
            if self.is_hidden:
                self.show_from_tray()
            top = tk.Toplevel(self.root)
            top.wm_attributes("-topmost", 1)
            tk.Label(top, text=message).pack()
            tk.Button(top, text="OK", command=top.destroy).pack()
            width = 300
            height = 70
            x = (top.winfo_screenwidth() // 2) - (width // 2)
            y = (top.winfo_screenheight() // 2) - (height // 2)
            top.geometry(f"{width}x{height}+{x}+{y}")
        else:
            self.root.after(1000, self.set_alarm)

    # ---- Tray helpers ----
    def _tray_image(self):
        img = Image.new("RGBA", (64, 64), (255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        d.ellipse((8, 8, 56, 56), outline=(60, 60, 60, 255), width=3)
        d.rectangle((30, 54, 34, 60), fill=(60, 60, 60, 255))
        return img

    def hide_to_tray(self):
        if self.is_hidden:
            return
        self.is_hidden = True
        self.root.withdraw()
        image = self._tray_image()
        menu = pystray.Menu(
            pystray.MenuItem("Show", lambda: self.root.after(0, self.show_from_tray)),
            pystray.MenuItem("Quit", lambda: self.root.after(0, self.quit_app))
        )
        self.tray_icon = pystray.Icon("alarm_app", image, "Alarm App", menu)
        self.tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
        self.tray_thread.start()

    def show_from_tray(self):
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
            self.tray_icon = None
            self.tray_thread = None
        self.is_hidden = False
        self.root.deiconify()
        try:
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.after(200, lambda: self.root.attributes("-topmost", False))
        except Exception:
            pass

    def quit_app(self):
        if self.tray_icon:
            try:
                self.tray_icon.stop()
            except Exception:
                pass
            self.tray_icon = None
        self.root.destroy()

if __name__ == "__main__":
    alarm_app = AlarmApp()
