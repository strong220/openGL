from ctypes import *
from ctypes.wintypes import *
from Rectangle_function1 import *


WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
def MAKEINTRESOURCE(i):
    return "OBM_BTNCORNERS"
##    return str(i)
##    return (LPSTR)((DWORD)((WORD)(i)))
WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000
WM_CREATE=0x01
WM_PAINT=0x0F
WM_NULL=0x00
WM_SIZE=5
WM_MOUSEMOVE = 0x200
RECTANGLE = None
PS_DOT=1

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
class RECT(Structure):
    _fields_=[("hdc",HDC),
              ("left",c_long),
              ("top",c_long),
              ("right",c_long),
              ("bottom",c_long)]
class PAINTSTRUCT(Structure):
    _fields_=[("hdc",HDC),
              ("fErase",c_bool),
              ("rcPaint", RECT),
              ("fRestore",c_bool),
              ("fIncUpdate",c_bool),
              ("rgbReserved[32]", c_byte)]
              

class MSG2(Structure):
    _fields_=[("hwnd",HWND),
              ("message",c_uint),
              ("wParam",WPARAM),
              ("lParam",LPARAM),
              ("time",DWORD),
              ("pt",POINT),
              ("lPrivate",DWORD)]

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
def RGB(b,g,r):
    B=str(b)
    G=str(g)
    R=str(r)
    out=list('0x00bbggrr')
    for i in range(2):
        if len(B)>i:
            out[4+i]=B[i]
        if len(G)>i:
            out[6+i]=G[i]
        if len(R)>i:
            out[8+i]=R[i]
    out="".join(out)
##    return hex(int(out,0))
    return out

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

def draw_rectangle(RECTANGLE,hWnd,paintclass,hdcCompat):
    windll.user32.BeginPaint(hWnd,pointer(paintclass))          #Begin Editing Window
    windll.gdi32.Rectangle(paintclass.hdc,RECTANGLE.left,RECTANGLE.top,RECTANGLE.right,RECTANGLE.bottom)                #Create Rectangle
    windll.gdi32.StretchBlt(paintclass.hdc,RECTANGLE.left+1,RECTANGLE.top+1,(RECTANGLE.right-RECTANGLE.left)-2,(RECTANGLE.bottom-RECTANGLE.top)-2,hdcCompat,0,0,32,32,"SRCCOPY")    #Redraw Rectangle shifted
    windll.user32.EndPaint(hWnd,pointer(paintclass))            #Complete Edits
    print('functionrun')
    return

def main():
    ##CREATE WINDOW##
    WndProc = WNDPROCTYPE(PyWndProcedure)
    hInst = windll.kernel32.GetModuleHandleW(0)
    wclassName = 'My Python Win32 Class'
    wname = 'My test window'

    wndClass=initialize_window(hInst,wclassName)
    regRes = windll.user32.RegisterClassExA(byref(wndClass))                                                                                    #Initialize Window
    hWnd = windll.user32.CreateWindowExA(0,wclassName,wname,WS_OVERLAPPEDWINDOW | WS_CAPTION,CW_USEDEFAULT, CW_USEDEFAULT,400,400,0,0,hInst,0)  #Create Window
    windll.user32.UpdateWindow(hWnd)
    windll.user32.ShowWindow(hWnd, SW_SHOW)                                                                                                     #Display Window
##CREATE RECTANGLE##
    LPARAM=1
    a=MainWndProc(hWnd,WM_CREATE,WPARAM,LPARAM,hInst)
    a.call_back(hWnd,WM_PAINT,WPARAM,LPARAM,hInst)
    a.call_back(hWnd,WM_SIZE,WPARAM,LPARAM,hInst)
####    test="NULL"
##    paintclass=PAINTSTRUCT()                                    #Create Structure for Rectangle
####    hbmp=windll.user32.LoadBitmapA(hInst,None)                  #Create a Bitmap for editing
##    hbmp=windll.user32.LoadImageA(hInst,"box.bmp",IMAGE_BITMAP,34,34,LR_LOADFROMFILE)
##
##    hdc=windll.user32.GetDC(hWnd)                               #Get the Device Context
##    hdcCompat = windll.gdi32.CreateCompatibleDC(hdc)            #Create a compatible device?
##    windll.gdi32.SelectObject(hdcCompat, hbmp)                  #Select the bitmap object?
####
##    crBkgnd = windll.gdi32.GetBkColor(hdc)                      #Obtain the background color
##    hbrBkgnd = windll.gdi32.CreateSolidBrush(crBkgnd)           #Make the Brush the background color
##    windll.user32.ReleaseDC(hWnd, hdc)                          #Release the Device Context
####
##    RECTANGLE=RECT()                                            #Initialize Rectangle
##    RECTANGLE2=RECT()                                            #Initialize Rectangle
##    windll.user32.SetRect(pointer(RECTANGLE),1,1,34,34)       #Rectangle Size
##    windll.user32.SetRect(pointer(RECTANGLE2),10,20,20,20)       #Rectangle Size
####    draw_rectangle(RECTANGLE,hWnd,paintclass,hdcCompat)

    if not hWnd:
        print(GetLastError())
        print('Failed to create window')
        exit(0)
##    print('ShowWindow', windll.user32.ShowWindow(hWnd, SW_SHOW))
##    print('UpdateWindow', windll.user32.UpdateWindow(hWnd))
    msg = MSG()
    msg_out=MSG()
    lpmsg = pointer(msg)
    lpmsg2=pointer(msg_out)
##    windll.user32.UpdateWindow(hWnd)
    print('Entering message loop')
    i=1
    while windll.user32.GetMessageA(lpmsg, hWnd, 0, 0) != 0:
            windll.user32.TranslateMessage(lpmsg)
##            print("dispatch ",windll.user32.DispatchMessageA(lpmsg))
            windll.user32.DispatchMessageA(lpmsg)
##            windll.user32.UpdateWindow(hWnd)
##            input(windll.user32.GetMessageA(lpmsg, hWnd, 0, 0))
##            print(msg.wParam)
            a.call_back(hWnd,msg.message,msg.wParam,msg.lParam,hInst)
##            if msg.message==513:
##            print("lParam" ,msg.lParam)
            if msg.message==WM_NULL:
                return
            
            
##            if i>200:
##                i=0
##            i=i+10
##            RECTANGLE.left=RECTANGLE.left+i
##            draw_rectangle(RECTANGLE,hWnd,paintclass,hdcCompat)
##            windll.user32.UpdateWindow(hWnd)
##            windll.user32.TranslateMessage(lpmsg)
##            windll.user32.DispatchMessageA(lpmsg)
            

    print('done.')
    
    
if __name__ == "__main__":
	print ("Win64 Application in python")
	main()


###AVAILABLE COMMANDS###
#windll.user32.BeginPaint(hWnd,LPPAINTSTRUCT)
