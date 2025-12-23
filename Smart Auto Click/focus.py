import win32gui
import win32process
import psutil

ROBLOX_PROCESS = "RobloxPlayerBeta.exe"

def roblox_running():
    for p in psutil.process_iter(['name']):
        if p.info['name'] == ROBLOX_PROCESS:
            return True
    return False

def roblox_focused():
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return False
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        return psutil.Process(pid).name() == ROBLOX_PROCESS
    except:
        return False
