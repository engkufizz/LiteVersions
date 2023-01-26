import tkinter as tk
import datetime

class AlarmApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alarm App")

        # Current time label
        self.time_label = tk.Label(self.root, font=("Arial", 20))
        self.time_label.pack()

        # Alarm section
        self.alarm_frame = tk.Frame(self.root)
        self.alarm_frame.pack()

        self.alarm_time_label = tk.Label(self.alarm_frame, text="Alarm Time:", font=("Arial", 16))
        self.alarm_time_label.grid(row=0, column=0)

        self.alarm_time_entry = tk.Entry(self.alarm_frame, font=("Arial", 16))
        self.alarm_time_entry.grid(row=0, column=1)

        self.set_alarm_button = tk.Button(self.alarm_frame, text="Set Alarm", font=("Arial", 16), command=self.set_alarm)
        self.set_alarm_button.grid(row=1, column=1)

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
            top = tk.Toplevel(self.root)
            top.wm_attributes("-topmost", 1)
            tk.Label(top, text="Time to take a break!").pack()
            tk.Button(top, text="OK", command=top.destroy).pack()
            width = 300
            height = 70
            x = (top.winfo_screenwidth() // 2) - (width // 2)
            y = (top.winfo_screenheight() // 2) - (height // 2)
            top.geometry(f"{width}x{height}+{x}+{y}")
        else:
            self.root.after(1000, self.set_alarm)


if __name__ == "__main__":
    alarm_app = AlarmApp()
