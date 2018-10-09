import win32api, win32con
from time import sleep

VKEY = {
    "LMB": 0x01,
    "MMB": 0x04,
    "LSHIFT": 0xA0,
    "d" : 0x44,
    "1" : 0x31,
    "2" : 0x32,
    "3" : 0x33,
    "4" : 0x34,
}

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


def keyIsUp(key):
    keystate = win32api.GetAsyncKeyState( key )
    if (keystate == 0) or (keystate == 1):
        return True
    else:
        return False
def keyIsDown(key):
    keystate = win32api.GetAsyncKeyState( key )
    #GetAsyncKeyState
    if (keystate != 0) and (keystate != 1):
        return True
    else:
        return False

def main():
    
    while(keyIsUp(VKEY['MMB'])):
        sleep(0.1)
        if keyIsDown(VKEY['LMB']):
            pos = win32api.GetCursorPos()
            print(pos)

            win32api.keybd_event(VKEY['d'], 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
            win32api.keybd_event(VKEY['d'], 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)
            
            if keyIsDown(VKEY['LMB']):
                sleep(0.1)

        
        

main()
#click(10,10)
