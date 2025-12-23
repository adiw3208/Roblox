import customtkinter as ctk
import tkinter as tk
import keyboard
from clicker import SmartClicker
from focus import roblox_running, roblox_focused

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title("Smart AutoClick")
        self.geometry("360x580")
        self.resizable(False, False)

        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        self.clicker = SmartClicker()
        keyboard.add_hotkey("f", self.toggle_clicker)

        # ===== VARIABLES =====
        self.status_rb = ctk.StringVar(value="ROBLOX : NOT RUNNING")
        self.status_focus = ctk.StringVar(value="FOCUS : NO")
        self.status_click = ctk.StringVar(value="AUTOCLICK : IDLE")
        self.coord_text = ctk.StringVar(value=f"LOCK : {self.clicker.lock_pos}")

        # ===== HEADER =====
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=10)

        ctk.CTkLabel(
            header,
            text="Smart AutoClick",
            font=("Segoe UI", 22, "bold")
        ).pack()

        ctk.CTkLabel(
            header,
            text="Developed by STUNT",
            font=("Segoe UI", 11),
            text_color="#888"
        ).pack()

        # ===== STATUS BOX =====
        status_box = ctk.CTkFrame(self, corner_radius=10)
        status_box.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(status_box, text="STATUS", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 4))
        ctk.CTkLabel(status_box, textvariable=self.status_rb).pack(anchor="w", padx=15)
        ctk.CTkLabel(status_box, textvariable=self.status_focus).pack(anchor="w", padx=15)
        ctk.CTkLabel(status_box, textvariable=self.status_click).pack(anchor="w", padx=15, pady=(0, 10))

        # ===== SETTINGS BOX =====
        settings = ctk.CTkFrame(self, corner_radius=10)
        settings.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(settings, text="SETTINGS", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(10, 4))

        self.interval_entry = ctk.CTkEntry(settings, width=120, justify="center")
        self.interval_entry.insert(0, "50")
        self.interval_entry.pack(anchor="w", padx=15, pady=6)
        ctk.CTkLabel(settings, text="Interval (ms)", text_color="#aaa").place(x=160, y=42)

        self.smart_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(settings, text="Smart Pause (Auto pause when unfocused)", variable=self.smart_var).pack(anchor="w", padx=15, pady=4)

        self.lock_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(settings, text="Lock Mouse Position", variable=self.lock_var).pack(anchor="w", padx=15, pady=4)

        ctk.CTkLabel(settings, textvariable=self.coord_text, text_color="#aaa").pack(anchor="w", padx=15, pady=(6, 2))

        ctk.CTkButton(
            settings,
            text="Set Lock Position",
            command=self.pick_position,
            height=32
        ).pack(anchor="w", padx=15, pady=(0, 12))

        # ===== ACTION BUTTONS =====
        action = ctk.CTkFrame(self, fg_color="transparent")
        action.pack(pady=15)

        ctk.CTkButton(
            action,
            text="START",
            width=140,
            height=38,
            fg_color="#2ecc71",
            command=self.start
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            action,
            text="STOP",
            width=140,
            height=38,
            fg_color="#e74c3c",
            command=self.stop
        ).grid(row=0, column=1, padx=10)

        ctk.CTkLabel(
            self,
            text="Hotkey : F",
            text_color="#777"
        ).pack(pady=(0, 10))

        self.after(300, self.update_status)

    # ===== LOGIC =====
    def start(self):
        try:
            self.clicker.interval = int(self.interval_entry.get()) / 1000
        except:
            return
        self.clicker.smart_pause = self.smart_var.get()
        self.clicker.lock_mouse = self.lock_var.get()
        self.clicker.start()
        self.status_click.set("AUTOCLICK : RUNNING")

    def stop(self):
        self.clicker.stop()
        self.status_click.set("AUTOCLICK : STOPPED")

    def toggle_clicker(self):
        if self.clicker.running:
            self.stop()
        else:
            self.start()

    def pick_position(self):
        overlay = tk.Toplevel(self)
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.35)
        overlay.attributes("-topmost", True)
        overlay.configure(bg="white", cursor="crosshair")

        label = tk.Label(
            overlay,
            text="CLICK ANYWHERE TO SET LOCK POSITION\nESC to cancel",
            font=("Segoe UI", 20, "bold"),
            bg="white"
        )
        label.place(relx=0.5, rely=0.12, anchor="center")

        def on_click(e):
            pos = (e.x_root, e.y_root)
            self.clicker.set_lock_position(pos)
            self.coord_text.set(f"LOCK : {pos}")
            overlay.destroy()

        overlay.bind("<Button-1>", on_click)
        overlay.bind("<Escape>", lambda e: overlay.destroy())

    def update_status(self):
        if roblox_running():
            self.status_rb.set("ROBLOX : DETECTED")
            self.status_focus.set("FOCUS : YES" if roblox_focused() else "FOCUS : NO")
        else:
            self.status_rb.set("ROBLOX : NOT RUNNING")
            self.status_focus.set("FOCUS : NO")

        if self.clicker.running and self.smart_var.get() and not roblox_focused():
            self.status_click.set("AUTOCLICK : PAUSED")

        self.after(300, self.update_status)
