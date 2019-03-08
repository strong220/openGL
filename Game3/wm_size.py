##THIS CLASS HANDLES THE CALL TO SIZE THE WINDOW##
##It returns a rectangle an points that describe the window##
from ctypes import *
from ctypes.wintypes import *

def WM_SIZE(cs,hwnd):
    ##Get Rectangle of selected screen
    windll.user32.GetClientRect(hwnd,pointer(cs.variables.Client_window.rcClient))

    ##Translate that Rectangle to usable POINT types
    cs.variables.Client_window.ptClientUL.x=cs.variables.Client_window.rcClient.left
    cs.variables.Client_window.ptClientUL.y=cs.variables.Client_window.rcClient.top
    cs.variables.Client_window.ptClientLR.x=cs.variables.Client_window.rcClient.right
    cs.variables.Client_window.ptClientLR.y=cs.variables.Client_window.rcClient.bottom

    ##Convert Points to reference the upper left hand corner of the screen
    ##instead of the window
    windll.user32.ClientToScreen(hwnd, pointer(cs.variables.Client_window.ptClientUL))
    windll.user32.ClientToScreen(hwnd, pointer(cs.variables.Client_window.ptClientLR))

    ##Convert the rectangle to reference the screen instead of the window
    windll.user32.SetRect(pointer(cs.variables.Client_window.rcClient),cs.variables.Client_window.ptClientUL,
                          cs.variables.Client_window.ptClientLR)

    return
