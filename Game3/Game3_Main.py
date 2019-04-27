##THIS GAME IS BASED ON A CLASSIC BOARD GAME AND SO IMAGES HAVE NOT
##BEEN INCLUDED DUE TO POTENTIAL COPYRIGHT VIOLATIONS. THIS CODE IS MENT FOR
##ILLUSTRATION PURPOSES ONLY

##Import functions##
from ctypes import *
from ctypes.wintypes import *
import time
from Game3_update import *
import winsound
##file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\Sounds\\Trial.wma"
##winsound.PlaySound(file_path_main,winsound.SND_FILENAME)

##Define Constants
WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000
WM_CREATE=0x01
WM_PAINT=0x0F
WM_NULL=0x00
WM_QUIT=0x12
WM_SIZE=5
WM_MOUSEMOVE = 0x200
RECTANGLE = None
PS_DOT=1
PM_NOREMOVE=0x0000
PM_REMOVE=0x0001

SW_SHOWNORMAL = 1
SW_SHOW = 5

CS_HREDRAW = 2
CS_VREDRAW = 1
CS_OWNDC = 0x0020

CW_USEDEFAULT = 0x80000000

WM_DESTROY = 2

IMAGE_BITMAP=0
LR_LOADFROMFILE=0x00000010

WHITE_BRUSH = 0
BLACK_BRUSH = 4

##Define Structures##
class WNDCLASSEX(Structure):
    _fields_ = [("cbSize", c_uint),
                ("style", c_uint),
                ("lpfnWndProc", WNDPROCTYPE),
                ("cbClsExtra", c_int),
                ("cbWndExtra", c_int),
                ("hInstance", HANDLE),
                ("hIcon", HANDLE),
                ("hCursor", HANDLE),
                ("hBrush", HANDLE),
                ("lpszMenuName", LPCWSTR),
                ("lpszClassName", LPCWSTR),
                ("hIconSm", HANDLE)]

##Define functions##
def PyWndProcedure(hWnd, Msg, wParam, lParam):
    if Msg == WM_DESTROY:
        windll.user32.PostQuitMessage(0)
    else:
        return windll.user32.DefWindowProcW(hWnd, Msg, wParam, lParam)
    return 0

def initialize_window(hInst,wclassName):
    WndProc = WNDPROCTYPE(PyWndProcedure)
    wndClass = WNDCLASSEX()
    wndClass.cbSize = sizeof(WNDCLASSEX)
    wndClass.style = CS_HREDRAW | CS_VREDRAW | CS_OWNDC
    wndClass.lpfnWndProc = WndProc
    wndClass.cbClsExtra = 0
    wndClass.cbWndExtra = 0
    wndClass.hInstance = hInst
    wndClass.hIcon = 0
    wndClass.hCursor = 0
    wndClass.hBrush = windll.gdi32.GetStockObject(WHITE_BRUSH)
    wndClass.lpszMenuName = 0
    wndClass.lpszClassName = wclassName
    wndClass.hIconSm = 0

    return wndClass

def main():
    ##CREATE PLAYER WINDOWS##
    WndProc = WNDPROCTYPE(PyWndProcedure)
    hInst = windll.kernel32.GetModuleHandleW(0)
    wclassName = 'My Python Win32 Class'
    wname = 'Player1 window'

    wndClass=initialize_window(hInst,wclassName)
    regRes = windll.user32.RegisterClassExA(byref(wndClass))                                                                                    #Initialize Window)                                                                                    #Initialize Window
    hWnd = windll.user32.CreateWindowExA(0,wclassName,wname,WS_OVERLAPPEDWINDOW | WS_CAPTION,CW_USEDEFAULT, CW_USEDEFAULT,1600,800,0,0,hInst,0)  #Create Window
    if not hWnd:
        print(GetLastError())
        print('Failed to create window')
        exit(0)
    windll.user32.UpdateWindow(hWnd)
    windll.user32.ShowWindow(hWnd, SW_SHOW)
    ##INITIALIZE MAP
    Game_main=MainWndProc(hWnd,WM_CREATE,WPARAM,0,hInst)
    Game_main.call_back(hWnd,WM_SIZE,WPARAM,0,hInst)
    Game_main.call_back(hWnd,WM_PAINT,WPARAM,0,hInst)
    ##INITIALIZE MESSAGELOOP
    msg = MSG()
    lpmsg = pointer(msg)
##    input("pause")
    ##MESSAGELOOP
    message=1
    start_time=time.process_time()
    while message!=0:
##        message=windll.user32.GetMessageA(lpmsg, hWnd, 0, 0)
##        windll.user32.TranslateMessage(lpmsg)
##        windll.user32.DispatchMessageA(lpmsg)
        while windll.user32.PeekMessageA(lpmsg,None,0,0,PM_REMOVE)!=0:
            #PROCESS MESSAGE IF THERE IS AN INPUT#
##            print("test")
##            if msg.message!=512:
##                print(msg.message)
##            print("in loop")
##                if msg.wParam==83:
##                    print("match")
##            print(msg.wParam)
##            print(msg.wParam)
            Game_main.call_back(hWnd,msg.message,msg.wParam,msg.lParam,hInst)
            if msg.message==WM_QUIT:
                return
            windll.user32.TranslateMessage(lpmsg)
            windll.user32.DispatchMessageA(lpmsg)
##        current_time=time.process_time()
##        time.sleep(current_time%(1/60))
##        input("pause")
####        prcurrent_time)
##        if current_time>start_time+.01:
##            start_time=time.process_time()
        temp=(1/80)-Game_main.ANIMATE()             ##Determine goal refresh rate##
        if temp>0:
            time.sleep(temp)
##        if temp>.16:
##            print(temp)
##        print(msg.message)
            #UPDATE FRAMES#
##        else:
##            Game_main.call_back(hWnd,msg.message,msg.wParam,msg.lParam,hInst)
##            print("start",start_time)
        ##CLEAN UP###
####        print(msg.message)
##        ##UPDATE FROM PLAYERS INTERACTION
####        PyWndProcedure(hWnd1, msg, wParam, lParam)
##        if msg.message==WM_NULL:
##            return


if __name__ == "__main__":
	print ("Win64 Application in python")
	main()

