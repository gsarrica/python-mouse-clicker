import win32api, win32con, ctypes, ctypes.wintypes, threading, sys
from time import sleep
import random, decimal

global shouldClick
shouldClick = False

global clicking_thread
global threadPaused
threadPaused = True

def toggleClick():
    global threadPaused
    threadPaused = not threadPaused
    if threadPaused:
        print ("Toggled Off")
    else:
        print ("Toggled On")
    
HOTKEYS = {
  1 : (win32con.VK_ADD)
}
	
HOTKEY_ACTIONS = {
  1 : toggleClick
}

def click():
    while True:
        if not threadPaused:
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            sleep(.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            sleep(.01)
        else:
            sleep(1.5)

def hotkeys():
    ctypes.windll.user32.RegisterHotKey(None, 1, 0, win32con.VK_ADD)
    try:
        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
            sleep(1)
            if msg.message == win32con.WM_HOTKEY:
                action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
                if action_to_take:
                    action_to_take()
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))
    finally:
        ctypes.windll.user32.UnregisterHotKey(None, 1)
			
print ("Press the + key on your numpad to activate.")
clicking_thread = threading.Thread(target=click)
hot_key_thread = threading.Thread(target=hotkeys)
hot_key_thread.start()
clicking_thread.start()
