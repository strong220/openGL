###This file is designed to translate the Using Rectangles code from C++
##to python
from ctypes import *
from ctypes.wintypes import *
import cv2

PS_DOT=1
SRCCOPY=0xCC
R2_NOTXORPEN=10
IMAGE_BITMAP=0
LR_LOADFROMFILE=0x00000010
LR_DEFAULTSIZE=0x00000040
def Longsplit(number):
    combined=list(bin(number))
    ##MAKE COMBINED A COMPLETE WORD##
    while len(combined)<34:
        combined.insert(2,'0')
    low=list(range(16))
    high=list(range(16))
    ##SPLIT WORD##
    for i in range(32):
        if i<len(combined)-2:
            if i<16:
                low[i]=combined[i+2]
            else:
                high[i-16]=combined[i+2]
    ##Make words##
    high.insert(0,"b")
    high.insert(0,"0")
    low.insert(0,"b")
    low.insert(0,"0")
    high="".join(high)
    low="".join(low)
    return [int(high,0),int(low,0)]
class RECT(Structure):
    _fields_=[#("hdc",HDC),
              ("left",c_long),
              ("top",c_long),
              ("right",c_long),
              ("bottom",c_long)]
class POINT(Structure):
    _fields_=[("x",c_int),
              ("y",c_int)]
    

class PAINTSTRUCT(Structure):
    _fields_=[("hdc",HDC),
              ("fErase",c_bool),
              ("rcPaint", RECT),
              ("fRestore",c_bool),
              ("fIncUpdate",c_bool),
              ("rgbReserved[32]", c_byte)]
def MAKEINTRESOURCE(i):
    return None#i

def RGB(b,g,r):
    #Returns the int equivalent to the hexidecimal "0x00bbggrr"
    zeroword='00'
    blue=hex(b)[2:]
    if len(blue)<2:
        blue='0'+blue
    green=hex(g)[2:]
    if len(green)<2:
        green='0'+green
    red=hex(r)[2:]
    if len(red)<2:
        red='0'+red
    out="0x"+zeroword+blue+green+red
    out=int(out,0)
    return out

class LPARAMS(Structure):
    _fields_=[("x",c_int),
              ("y",c_int)]

class MainWndProc_var(Structure):
    _fields_=[("hdc",HDC),                      ##device context(DC) for window
              ("rcTmp",RECT),                   ##temporary rectangle
              ("ps",PAINTSTRUCT),               ##paint data for BeginPaint and End Paint
              ("ptClientUL",POINT),             ##client area upper left corner
              ("ptClientLR",POINT),             ##client area lower right corner
              ("hdcCompat",HDC),                ##DC for copying bitmap
              ("pt",POINT),                     ##x and y coordinates of cursor
              ("rcBmp",RECT),                   ##rectangle that encloses bitmap
              ("rcTarget",RECT),                ##rectangle to receive bitmap
              ("rcClient",RECT),                ##client-area rectangle
              ("fDragRect",c_bool),             ##TRUE if bitmap rect. is dragged
              ("hbmp",HBITMAP),                 ##handle of bitmap to display
              ("hbrBkgnd",HBRUSH),              ##handle of background-color brush
              ("crBkgnd",COLORREF),             ##color of client-area background
              ("hpenDot",HPEN)]                 ##handle of dotted pen
class hInstance(Structure):
    _fields_=[('hInstance',HANDLE)]

class MainWndProc:
    def __init__(self,hwnd,uMsg,wParam,lparam,hInst):
        self.hwnd=hwnd
        self.uMsg=uMsg
        self.wParam=wParam
        self.lParam=LPARAMS()
        temp=Longsplit(lparam)
        self.lParam.x=temp[0]
        self.lParam.y=temp[1]
        self.hinst=hInst
        self.vwin=MainWndProc_var()
        self.tried=0
        self.call_back(hwnd,uMsg,wParam,lparam,hInst)
    def call_back(self,hwnd,uMsg,wParam,lparam,hInst):
        self.hwnd=hwnd
        self.uMsg=uMsg
        self.wParam=wParam
        self.hinst=hInst
        if lparam>0:
            temp=Longsplit(lparam)
            self.lParam.x=temp[0]
            self.lParam.y=temp[1]
        inputs={1: "WM_CREATE",2: "WM_DESTROY",3:"WM_MOVE",5: "WM_SIZE",15: "WM_PAINT",
                513: "WM_LBUTTONDOWN", 514:"WM_LBUTTONUP", 512: "WM_MOUSEMOVE"}
        Message=inputs.get(self.uMsg,"Invalid")
##        print('success',Message, " ", self.uMsg)
        method=getattr(self,Message,lambda:"Invalid message")
        return method()

    def WM_CREATE(self):
        ##Load the bitmap resource
##        self.vwin.hbmp=windll.user32.LoadBitmapA(self.hinst, MAKEINTRESOURCE(1))
        
        file_path="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\box2.bmp"
        file_pointer=LPCWSTR(file_path)
        print(file_pointer)
##        t=cv2.imread(file_path,1)
##        cv2.imshow('image',t)
##        cv2.waitKey(0)

##        file_path="box_24.bmp"
##        file_path="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\box_24.bmp\0"
##        file_pointer=c_wchar_p(file_path)
        h=hInstance()
        LoadImage=windll.user32.LoadImageW
        LoadImage.restype=HBITMAP
        LoadImage.argtypes = [HINSTANCE, LPCWSTR, UINT, c_int, c_int, UINT]
##        LoadImage.errcheck=errcheck()
##        self.vwin.hbmp=LoadImage(h.hInstance,file_pointer,IMAGE_BITMAP,0,0,LR_LOADFROMFILE)#8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        self.vwin.hbmp=LoadImage(c_void_p(),file_pointer,IMAGE_BITMAP,0,0,LR_DEFAULTSIZE|LR_LOADFROMFILE)#LR_DEFAULTSIZE|c_void_p()
        print(GetLastError())
        print(self.vwin.hbmp)
        ##Create a device context (DC) to hold the bitmap
        ##The bitmap is copied from this DC to the window's DC
        ##whenever it must be drawn
        self.vwin.hdc=windll.user32.GetDC(self.hwnd)
        self.vwin.hdcCompat=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        windll.gdi32.SelectObject(self.vwin.hdcCompat,self.vwin.hbmp)
##        windll.gdi32.SelectObject(self.vwin.hbmp,self.vwin.hdcCompat)
        ##Create a brush of the same color as the background
        ##of the client area. The brush is used later to erase
        ##the old bitmap before copying the bitmap into the
        ##target rectangle
        self.vwin.crBkgnd=windll.gdi32.GetBkColor(self.vwin.hdc)
        self.vwin.hbrBkgnd=windll.gdi32.CreateSolidBrush(self.vwin.crBkgnd)
        windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        ##Create a dotted pen. The pen is used to draw the
        ##bitmap rectangle as the user drags it.
        self.vwin.hpenDot=windll.gdi32.CreatePen(PS_DOT,2,RGB(150,0,0))
        ##Set the initial rectangle for the bitmap. Note that
        ##this aplication supports only a 32- by 32 pixel
        ##bitmap. The rectangle is slightly larger than the
        ##bitmap
        windll.user32.SetRect(pointer(self.vwin.rcBmp),1,1,34,34)
        return 0
    def WM_PAINT(self):
        ##Draw the bitmap rectangle and copy the bitmap into
        ##it. The 32-pixel by 32-pixel bitmap is centered in
        ##the rectangle by adding 1 to the left and top
        ##coordinates of the bitmap rectangle, and subtracting 2
        ##from the right and bottom coordinates.
        windll.user32.BeginPaint(self.hwnd,pointer(self.vwin.ps))
        windll.gdi32.Rectangle(self.vwin.ps.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
                               self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)
        windll.gdi32.StretchBlt(self.vwin.ps.hdc,self.vwin.rcBmp.left+1,self.vwin.rcBmp.top+1,
                                 (self.vwin.rcBmp.right-self.vwin.rcBmp.left)-2,
                                 (self.vwin.rcBmp.bottom-self.vwin.rcBmp.top)-2,
                                 self.vwin.hdcCompat,0,0,32,32,SRCCOPY)
        windll.user32.EndPaint(self.hwnd,pointer(self.vwin.ps))
        return
    def WM_MOVE(self):
        return
    def WM_SIZE(self):
        ##Convert the client coordinates of the client-area
        ##rectangle to screen coordinates and save them in a
        ##a rectangle. The rectangle is passed to the ClipCursor
        ##function during WM_LBUTTONDOWN processing
        windll.user32.GetClientRect(self.hwnd,pointer(self.vwin.rcClient))
        self.vwin.ptClientUL.x=self.vwin.rcClient.left
        self.vwin.ptClientUL.y=self.vwin.rcClient.top
        self.vwin.ptClientLR.x=self.vwin.rcClient.right
        self.vwin.ptClientLR.y=self.vwin.rcClient.bottom
        windll.user32.ClientToScreen(self.hwnd, pointer(self.vwin.ptClientUL))
        windll.user32.ClientToScreen(self.hwnd, pointer(self.vwin.ptClientLR))
        windll.user32.SetRect(pointer(self.vwin.rcClient),self.vwin.ptClientUL.x,self.vwin.ptClientUL.y,
                              self.vwin.ptClientLR.x,self.vwin.ptClientLR.y)
        return 0
    def WM_LBUTTONDOWN(self):
        ##Restrict the mouse cursor to the client area. This
        ##ensures that the window recieves a matching
        ##WM_LBUTTONUP message
        windll.user32.ClipCursor(pointer(self.vwin.rcClient))

        ##Save the coordinates of the mouse cursor

        self.vwin.pt.x=self.lParam.x
        self.vwin.pt.y=self.lParam.y

        ##If the user has clicked the bitmap rectangle, redraw
        ##it using the dotted pen. Set the fDragRect flag to indicate
        ##that the user is about to drag the rectangle
        if (windll.user32.PtInRect(pointer(self.vwin.rcBmp),self.vwin.pt)):
            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            ##Remove previous Bitmap
            windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcBmp),self.vwin.hbrBkgnd)
            windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot)
            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
                                   self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)
            self.vwin.fDragRect=True
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        return 0
    def WM_MOUSEMOVE(self):
        inputs={1:"MK_LBUTTON"}
        MK_LBUTTON=inputs.get(self.wParam,False)
        ##Draw a target rectangle or drag the bitmap rectangle,
        ##Depending on the status of the fDragRect flag

        if((self.wParam and MK_LBUTTON) and self.vwin.fDragRect==False):
            ##Set the mix mode so that the pen color is the
            ##inverse of the background color. The previous
            ##rectangle can then be erased by drawing
            ##another rectrangle on top of it.

            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)

            ##If a previous target rectangle exists, erase
            ##it by drawing another rectangle on top of it

            if(windll.user32.IsRectEmpty(pointer(self.vwin.rcTarget))==True):
                windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot)
                windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcTarget.left,self.vwin.rcTarget.top,self.vwin.rcTarget.right,self.vwin.rcTarget.bottom)

            ##Save the coordinates of the target rectangle. Avoid
            ##invalid rectangles by ensuring that the value of
            ##the left coordinate is lesser than the
            ##right coordinate, and that the value of the top
            ##coordinate is lesser than the bottom coordinate.

            if ((self.vwin.pt.x<self.lParam.x) and (self.vwin.pt.y<self.lParam.y)):
                windll.user32.SetRect(pointer(self.vwin.rcTarget),self.vwin.pt.x,self.lParam.y,self.lParam.x,self.vwin.pt.y)

            elif ((self.vwin.pt.x>self.lParam.x) and (self.vwin.pt.y<self.lParam.y)):
                windll.user32.SetRect(pointer(self.vwin.rcTarget),self.lParam.x,self.lParam.y,
                                      self.vwin.pt.x,self.vwin.pt.y)
            elif ((self.vwin.pt.x>self.lParam.x) and (self.vwin.pt.y>self.lParam.y)):
                windll.user32.SetRect(pointer(self.vwin.rcTarget),self.lParam.x,self.vwin.pt.y,
                                      self.vwin.pt.x,self.lParam.y)
            else:
                windll.user32.SetRect(pointer(self.vwin.rcTarget),self.vwin.pt.x,self.vwin.pt.y,
                                      self.lParam.x,self.lParam.y)
            ##Draw the new target rectangle.
            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcTarget.left,self.vwin.rcTarget.top,
                       self.vwin.rcTarget.right,self.vwin.rcTarget.bottom)
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        elif((self.wParam and MK_LBUTTON) and self.vwin.fDragRect==True):
            ##Set the mix mode so that the pen color is the
            ##inverse of the background color
            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
            ##Select the dotted pen into the DC and erase
            ##the previous bitmap rectangle by drawing
            ##another rectangle on top of it.
            windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot)
            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
                                   self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)
            ##Set the new coordinates of the bitmap rectangle,
            ##then redraw it.
            windll.user32.OffsetRect(pointer(self.vwin.rcBmp),self.lParam.x-self.vwin.pt.x,
                                     self.lParam.y-self.vwin.pt.y)

            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
                                   self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)

            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)

            ##Save the coordinates of the mouse cursor.

            self.vwin.pt.x=self.lParam.x
            self.vwin.pt.y=self.lParam.y
        return 0
    def WM_LBUTTONUP(self):
        ##If the bitmap rectangle and target rectangle
        ##intersect, copy the bitmap into the target
        ##rectangle. Otherwise, copy the bitmap into the
        ##rectangle bitmap at its new location.
        if (windll.user32.IntersectRect(pointer(self.vwin.rcTmp),pointer(self.vwin.rcBmp),pointer(self.vwin.rcTarget))==True):
            ##Erase the bitmap rectangle by filling it with
            ##the background color.
            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcBmp),self.vwin.hbrBkgnd)
            ##Redraw the target rectangle because the part
            ##that intersected with the bitmap rectangle was
            ##erased by the call to FillRect.
            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcTarget.left,self.vwin.rcTarget.top,
                                   self.vwin.rcTarget.right,self.vwin.rcTarget.bottom)
            ##Copy the bitmap into the target rectangle.
            windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcTarget.left+1,self.vwin.rcTarget.top+1,
                                 (self.vwin.rcTarget.right-self.vwin.rcTarget.left)-2,
                                 (self.vwin.rcTarget.bottom-self.vwin.rcTarget.top)-2,
                                 self.vwin.hdcCompat,0,0,32,32,SRCCOPY)

            ##Copy the target rectangle to the bitmap
            ##rectangle, set the coordinates of the target
            ##rectangle to 0, then reset the fDragRect flag.

            windll.user32.CopyRect(pointer(self.vwin.rcBmp),pointer(self.vwin.rcTarget))
            windll.user32.SetRectEmpty(pointer(self.vwin.rcTarget))
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
            self.vwin.fDragRect=False
        elif(self.vwin.fDragRect==True):
            ##Draw the bitmap rectangle,copy the bitmap into
            ##it, and reset the fDragRect flag
            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
                                   self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)
            windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcBmp.left+1,self.vwin.rcBmp.top+1,
                                 (self.vwin.rcBmp.right-self.vwin.rcBmp.left)-2,
                                 (self.vwin.rcBmp.bottom-self.vwin.rcBmp.top)-2,
                                 self.vwin.hdcCompat,0,0,32,32,SRCCOPY)
            
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
            self.vwin.fDragRect=False

            ##Release the mouse cursor.
            windll.user32.ClipCursor(pointer(self.vwin.rcClient))#pointer(RECT()))
        return 0
    def WM_DESTROY(self):
        ##Destry the background brush, compatible bitmap,
        ##and the bitmap
        windll.gdi32.DeleteObject(self.vwin.hbrBkgnd)
        windll.gdi32.DeleteDC(self.vwin.hdcCompat)
        windll.gdi32.DeleteObject(self.vwin.hbmp)
        windll.user32.PostQuitMessage(0)
        return
        
        
##a=MainWndProc(1234,"WM_CREATE",12,0)
##print(a.call_back("WM_CREATE"))
##a=Switcher()
##print(a.numbers_to_months(1))

