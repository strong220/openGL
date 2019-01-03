from ctypes import *
from ctypes.wintypes import *


WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
def MAKEINTRESOURCE(i):
    return "OBM_BTNCORNERS"
##    return str(i)
##    return (LPSTR)((DWORD)((WORD)(i)))
WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000

RECTANGLE = None
PS_DOT=1

SW_SHOWNORMAL = 1
SW_SHOW = 5

CS_HREDRAW = 2
CS_VREDRAW = 1
CS_OWNDC = 0x0020

CW_USEDEFAULT = 0x80000000

WM_DESTROY = 2

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
  


def main():
    ##CREATE WINDOW##
    WndProc = WNDPROCTYPE(PyWndProcedure)
    hInst = windll.kernel32.GetModuleHandleW(0)
    wclassName = 'My Python Win32 Class'
    wname = 'My test window'
    
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
    regRes = windll.user32.RegisterClassExA(byref(wndClass))
    hWnd = windll.user32.CreateWindowExA(0,wclassName,wname,WS_OVERLAPPEDWINDOW | WS_CAPTION,CW_USEDEFAULT, CW_USEDEFAULT,600,300,0,0,hInst,0)
    print('ShowWindow', windll.user32.ShowWindow(hWnd, SW_SHOW))
##CREATE RECTANGLE##
    test="NULL"
    paintclass=PAINTSTRUCT()
    hbmp=windll.user32.LoadBitmapA(hInst,MAKEINTRESOURCE(1))
    input('pause')
    hdc=windll.user32.GetDC(hWnd)
    hdcCompat = windll.gdi32.CreateCompatibleDC(hdc)
    windll.gdi32.SelectObject(hdcCompat, hbmp)
##
    crBkgnd = windll.gdi32.GetBkColor(hdc)
    hbrBkgnd = windll.gdi32.CreateSolidBrush(crBkgnd)
    windll.user32.ReleaseDC(hWnd, hdc)
##
    RECTANGLE=RECT()
    hpenDot = windll.gdi32.CreatePen(PS_DOT, 1, RGB(0,0,0))
    windll.user32.SetRect(pointer(RECTANGLE),10,10,20,20)
####    paintclass.hdc=windll.user32.GetDC(hWnd)
####    paintclass.fErace=1
####    paintclass.rcPaint=rectclass
    windll.user32.BeginPaint(hWnd,pointer(paintclass))
##    input(RECTANGLE.top)
##    input(paintclass.hdc)
    windll.gdi32.Rectangle(paintclass.hdc,RECTANGLE.left,RECTANGLE.top,RECTANGLE.right,RECTANGLE.bottom)
    windll.gdi32.StretchBlt(paintclass.hdc,RECTANGLE.left+1,RECTANGLE.top+1,(RECTANGLE.right-RECTANGLE.left)-2,(RECTANGLE.bottom-RECTANGLE.top)-2,hdcCompat,0,0,32,32,"SRCCOPY")

    windll.user32.EndPaint(hWnd,pointer(paintclass))
##    windll.user32.ReleaseDC(hWnd,test)
    print("paint",test, " ",paintclass.hdc)
    if not hWnd:
        print(GetLastError())
        print('Failed to create window')
        exit(0)
##    print('ShowWindow', windll.user32.ShowWindow(hWnd, SW_SHOW))
##    print('UpdateWindow', windll.user32.UpdateWindow(hWnd))
    msg = MSG()
    lpmsg = pointer(msg)

    print('Entering message loop')
##    printf=cdll.msvcrt.printf
##    printf('hello')
        
    while windll.user32.GetMessageA(lpmsg, 0, 0, 0) != 0:
            windll.user32.TranslateMessage(lpmsg)
            windll.user32.DispatchMessageA(lpmsg)

    print('done.')
    
    
if __name__ == "__main__":
	print ("Win64 Application in python")
	main()


###AVAILABLE COMMANDS###
#windll.user32.BeginPaint(hWnd,LPPAINTSTRUCT)
