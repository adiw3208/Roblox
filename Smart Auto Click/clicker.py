import time
import win32api
import win32con
import ctypes
from focus import roblox_focused

class SmartClicker:
    def __init__(self):
        self.running = False
        self.interval = 0.05
        self.smart_pause = True
        self.lock_mouse = True

        screen_x = ctypes.windll.user32.GetSystemMetrics(0)
        screen_y = ctypes.windll.user32.GetSystemMetrics(1)
        self.lock_pos = (screen_x // 2, screen_y // 2)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def set_lock_position(self, pos):
        self.lock_pos = pos

    def click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def loop(self):
        while True:
            if self.running:
                if not self.smart_pause or roblox_focused():
                    if self.lock_mouse and self.lock_pos:
                        win32api.SetCursorPos(self.lock_pos)
                    self.click()
            time.sleep(self.interval)
