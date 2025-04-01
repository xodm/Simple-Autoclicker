import pyautogui
import threading
import time
import tkinter as tk
import keyboard

scan_code_to_char = {
    18: '1', 50: '`', 19: '2', 20: '3', 21: '4', 23: '5', 22: '6',
    26: '7', 28: '8', 25: '9', 29: '0', 27: '-', 24: '=',
    12: 'q', 13: 'w', 14: 'e', 15: 'r', 17: 't', 16: 'y', 32: 'u',
    34: 'i', 31: 'o', 35: 'p', 33: '[', 30: ']', 42: '\\',
    1: 's', 2: 'd', 3: 'f', 5: 'g', 4: 'h', 38: 'j', 40: 'k',
    37: 'l', 41: ';', 39: "'", 6: 'z', 7: 'x', 8: 'c', 9: 'v',
    11: 'b', 45: 'n', 46: 'm', 43: ',', 47: '.', 44: '/',
    179: "Fn key"
}

class AutoClickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Autoclicker")
        self.root.geometry("300x400")

        self.clicking = False
        self.start = False
        self.interval = 0.1
        self.toggle_key = None
        self.hotkey_listener = None

        self.interval_var = tk.StringVar(value="0.1")
        self.interval_var.trace_add("write", self.on_interval_change)

        tk.Label(self.root, text="Click interval (sec):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.interval_var).pack(pady=5)

        self.status_label = tk.Label(self.root, text="Clicking: OFF\nInterval: 0.1", fg="black")
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(self.root, text="Enable Autoclicker", command=self.allow_clicking, width=20)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Disable Autoclicker", state="disabled", command=self.deny_clicking, width=20)
        self.stop_button.pack(pady=5)

        self.hotkey_label = tk.Label(self.root, text="Hotkey: None", fg="black")
        self.hotkey_label.pack(pady=5)

        self.set_button = tk.Button(self.root, text="Record Hotkey", command=self.set_hotkey)
        self.set_button.pack(pady=10)

        tk.Button(self.root, text="Exit", command=self.quit_app).pack(pady=5)

        threading.Thread(target=self.click_loop, daemon=True).start()

    def click_loop(self):
        while True:
            if self.clicking and self.start:
                pyautogui.click()
                time.sleep(self.interval)
            else:
                time.sleep(0.1)

    def toggle_clicking(self):
        self.clicking = not self.clicking
        self.status_label.config(text=f"Clicking: {'ON' if self.clicking else 'OFF'}\nInterval: {self.interval}")

    def on_hotkey(self):
        self.toggle_clicking()

    def quit_app(self):
        self.clicking = False
        self.root.destroy()

    def allow_clicking(self):
        self.start = True
        threading.Thread(target=self.click_loop, daemon=True).start()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

    def deny_clicking(self):
        self.start = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def on_interval_change(self, *args):
        try:
            self.interval = float(self.interval_var.get())
        except ValueError:
            pass
        self.status_label.config(text=f"Clicking: {'ON' if self.clicking else 'OFF'}\nInterval: {self.interval}")

    def set_hotkey(self):
        self.set_button.config(text="Press any key...", state="disabled")
        self.hotkey_label.config(text="Waiting for key...")

        def on_key(event):
            if event.event_type != "down":
                return

            self.toggle_key = event.scan_code
            label = scan_code_to_char.get(self.toggle_key, event.name)
            self.hotkey_label.config(text=f"Hotkey set to scan code: {label}")
            self.set_button.config(text="Record Hotkey", state="normal")

            if self.hotkey_listener:
                keyboard.unhook(self.hotkey_listener)

            #So basically when we recieve the key it will call on_hotkey, despite what is actually given
            self.hotkey_listener = keyboard.on_press_key(self.toggle_key, lambda _: self.on_hotkey())
            keyboard.unhook(on_key)

        keyboard.hook(on_key)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AutoClickerApp()
    app.run()
