##THIS FILE CONSISTS OF THE CLASS THAT HANDLES COMMANDS AND READS
##THE IMAGE
from ctypes import *
from ctypes.wintypes import *
##from Points import *
import cv2
import random
import math
import time

##DEFINE CONSTANTS
PW_CLIENTONLY=1
PS_DOT=1
SRCCOPY=0xCC0020
R2_NOTXORPEN=10
IMAGE_BITMAP=0
LR_LOADFROMFILE=0x00000010
LR_DEFAULTSIZE=0x00000040
LR_LOADTRANSPARENT=0x00000020
BI_RGB=0x0000
DIB_RGB_COLORS=0x00
R2_XORPEN=0x0007
R2_COPYPEN=0x000D
WHITENESS=0x00FF0062
CAPTUREBLT=1073741824
SRCERASE=0x00440328
SRCAND=0x008800C6
ALTERNATE=0x0001
R2_MASKPEN=0x0009
WINDING = 0x0002
MWT_IDENTITY = 0x01
MWT_LEFTMULTIPLY = 0x02
MWT_RIGHTMULTIPLY = 0x03
MWT_SET = 0x04
GM_COMPATIBLE = 0x00000001
GM_ADVANCED = 0x00000002
DCX_PARENTCLIP = 0x00000020

##DEFINE STRUCTURES##
class BITMAP(Structure):
    _fields_=[("bmType",c_long),
              ("bmWidth",c_long),
              ("bmHeight",c_long),
              ("bmWidthBytes",c_long),
              ("bmPlanes",WORD),
              ("bmBitsPixel",WORD),
              ("bmBits",POINTER(BYTE))]#LPVOID)]#*1000)]#POINTER(BYTE))]#BYTE*1)]POINTER(BYTE*1))]#L

class RGBQUAD(Structure):
    _fields_=[('rgbBlue',BYTE),
             ('rgbGreen',BYTE),
             ('rgbRed',BYTE),
             ('rgbReserved',BYTE)]
    
class PALETTEENTRY(Structure):
    _fields_=[("peRed",BYTE),
              ("peGreen",BYTE),
              ("peBlue",BYTE),
              ("peFlags",BYTE)]

class LOGPALETTE(Structure):
    _fields_=[("palVersion",WORD),
              ("palNumEntries",WORD),
              ("palPalEntry",PALETTEENTRY*256)]
    
class DIBSection(Structure):
    _fields_=[("hMemDC",HDC),
              ("hOldBitmap",HBITMAP),
              ("rgb",RGBQUAD*256),
              ("pLogPal",LOGPALETTE),#POINTER(LOGPALETTE)),
              ('i',WORD)]

class LPARAMS(Structure):
    _fields_=[("x",c_int),
              ("y",c_int)]

class BITMAPINFOHEADER(Structure):
    _fields_=[("biSize",DWORD),
              ("biWidth",c_long),
              ("biHeight",c_long),
              ("biPlanes",WORD),
              ("biBitCount",WORD),
              ("biCompression",DWORD),
              ("biSizeImage",DWORD),
              ("biXPelsPerMeter",c_long),
              ("biClrUsed",DWORD),
              ("biClrImortant",DWORD)]
class BITMAPINFO(Structure):
    _fields_=[("bmiHeader",BITMAPINFOHEADER),
             ("bmiColors",RGBQUAD*256)]

class MainWndProc_var(Structure):
    _fields_=[("hdc",HDC),                      ##device context(DC) for window
              ("rcTmp",RECT),                   ##temporary rectangle
##              ("ps",PAINTSTRUCT),               ##paint data for BeginPaint and End Paint
              ("ptClientUL",POINT),             ##client area upper left corner
              ("ptClientLR",POINT),             ##client area lower right corner
              ("hdcCompat_main",HDC),           ##DC for copying main map bitmap
              ("hdcCompat_gray",HDC),           ##DC for copying gray map bitmap
              ("hdcCompat_token",HDC*2),          ##DC for copying blue and red token pieces
              ("hdcCompat_card",HDC*3),          ##DC for copying blue and red token pieces
              ("pt",POINT),                     ##x and y coordinates of cursor
              ("rcBmp",RECT),                   ##rectangle that encloses bitmap
              ("rcSelect",RECT*2),              ##rectangle for selecting armies
              ("rcTarget",RECT),                ##rectangle containing game
              ("rcClient",RECT),                ##client-area rectangle
              ("bm",BITMAP)]
##DEFINE FUNCTIONS
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

##DEFINE CLASS##
class MainWndRead:
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
        self.color=DIBSection()
    def call_back(self,hwnd,uMsg,wParam,lparam,hInst):
        self.hwnd=hwnd
        self.uMsg=uMsg
        self.wParam=wParam
        self.hinst=hInst
        if lparam>0:
            temp=Longsplit(lparam)
            self.lParam.x=temp[0]
            self.lParam.y=temp[1]
        ##DICTIONARY FOR MESSAGE##
        inputs={1: "WM_CREATE",2: "WM_DESTROY",3:"WM_MOVE",5: "WM_SIZE",15: "WM_PAINT",
                160:"WM_NCMOUSEMOVE",161:"WM_NCLBUTTONDOWN",513: "WM_LBUTTONDOWN", 514:"WM_LBUTTONUP", 512: "WM_MOUSEMOVE"}
        ##TRANSLATE MESSAGE##
        Message=inputs.get(self.uMsg,"Invalid")
        ##CALL FUNCTION RELATED TO MESSAGE##
        method=getattr(self,Message,lambda:"Invalid message")
        return method()
    def WM_LBUTTONDOWN(self):
        self.vwin.pt.x=self.lParam.x
        self.vwin.pt.y=self.lParam.y
    def WM_LBUTTONUP(self):
        print("x: ",self.vwin.pt.x,"y: ",self.vwin.pt.y)
    def Find_window(self):
        ##scroll all the way up
        windll.user32.keybd_event(0x21,0,0,0)
        time.sleep(0.01)
        windll.user32.keybd_event(0x21,0,0x0002,0)
        ##scroll 8 arrows down
        for i in range(8):
            time.sleep(.01)
            windll.user32.keybd_event(0x28,0,0,0)
            time.sleep(0.01)
            windll.user32.keybd_event(0x28,0,0x0002,0)
        windll.user32.GetClientRect(self.hwnd,pointer(self.vwin.rcClient))
        self.vwin.ptClientUL.x=self.vwin.rcClient.left
        self.vwin.ptClientUL.y=self.vwin.rcClient.top
        self.vwin.ptClientLR.x=self.vwin.rcClient.right
        self.vwin.ptClientLR.y=self.vwin.rcClient.bottom
        windll.user32.ClientToScreen(self.hwnd,pointer(self.vwin.ptClientUL))   ##Get Upper Left point of window
        windll.user32.ClientToScreen(self.hwnd,pointer(self.vwin.ptClientLR))   ##Get Lower Right point of window
        windll.user32.SetRect(pointer(self.vwin.rcClient),self.vwin.ptClientUL.x,
                              self.vwin.ptClientUL.y,
                              self.vwin.ptClientLR.x,self.vwin.ptClientLR.y)
        self.vwin.ptClientLR.x=self.vwin.ptClientUL.x+660
        self.vwin.ptClientLR.y=self.vwin.ptClientUL.y+784
        self.vwin.ptClientUL.x=self.vwin.ptClientUL.x+20
        self.vwin.ptClientUL.y=self.vwin.ptClientUL.y+208
        windll.user32.SetRect(pointer(self.vwin.rcTarget),self.vwin.ptClientUL.x,
                              self.vwin.ptClientUL.y,
                              self.vwin.ptClientLR.x,self.vwin.ptClientLR.y)
        
        return
    def Stick_mouse(self):
        windll.user32.ClipCursor(pointer(self.vwin.rcTarget))
        ##SELECT DESIRED WINDOW##
        dx=int(65535.0/1600*(self.vwin.ptClientLR.x+self.vwin.ptClientUL.x)/2)
        dy=int(65535.0/900*(self.vwin.ptClientLR.y+self.vwin.ptClientUL.y)/2)
        windll.user32.mouse_event(0x0001|0x8000|0x0002,dx,dy,0,0)
        time.sleep(0.01)
        windll.user32.mouse_event(0x0001|0x8000|0x0004,dx,dy,0,0)
        
    def READ_image(self):
        Region=windll.gdi32.CreateRectRgn(0,0,self.vwin.rcClient.right-self.vwin.rcClient.left,self.vwin.rcClient.bottom-self.vwin.rcClient.top)
        self.vwin.hdc=windll.user32.GetDCEx(self.hwnd,Region,DCX_PARENTCLIP)
##        temp=windll.gdi32.GetPixel(raw_hdc,100,100)
##        print(temp)
##        self.vwin.hdc=windll.gdi32.CreateCompatibleDC(raw_hdc)
##        hbmp=windll.gdi32.CreateCompatibleBitmap(self.vwin.hdc,
##                                                  self.vwin.rcClient.right-self.vwin.rcClient.left,
##                                                  self.vwin.rcClient.bottom-self.vwin.rcClient.top)
##        hbmp2=windll.gdi32.CreateCompatibleBitmap(raw_hdc,
##                                                  self.vwin.rcClient.right-self.vwin.rcClient.left,
##                                                  self.vwin.rcClient.bottom-self.vwin.rcClient.top)
##        windll.gdi32.SelectObject(self.vwin.hdc,hbmp)
##        temp=windll.gdi32.GetPixel(self.vwin.hdc,10,10)
##        print(temp)
##        input("pause")
##        windll.gdi32.SelectObject(raw_hdc,hbmp2)
##        windll.gdi32.SelectClipRgn(raw_hdc,None)
##        print(self.hwnd)
##        print(raw_hdc)
##        print(self.vwin.hdc)
##        print(hbmp)
##        print("hdc raw",windll.gdi32.GetPixel(raw_hdc,10,10))
        ##COPY DATA INTO MEMORY DC
##        windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
##        print(windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.rcClient.right-self.vwin.rcClient.left,self.vwin.rcClient.bottom-self.vwin.rcClient.top,
##                            raw_hdc,0,0,WHITENESS))#CAPTUREBLT))   
        horizontal=int((self.vwin.ptClientLR.x-self.vwin.ptClientUL.x)/4)
        vertical=int((self.vwin.ptClientLR.y-self.vwin.ptClientUL.y)/4)
        black_bars=0
        first=0
        ##CHECH MESSAGE BOX##
        offsetx=self.vwin.ptClientUL.x-self.vwin.rcClient.left
        offsety=self.vwin.ptClientUL.y-self.vwin.rcClient.top
        main_top=[[2,36,0],
                [3,36,0xFFFFFF],
                [4,36,0]]
        main_bottom=[[2,116,0],
                    [3,116,0xFFFFFF],
                    [4,116,0]]
        flag=True
        for i in range(3):
            print(windll.gdi32.GetPixel(self.vwin.hdc,int(main_top[i][0]*4+offsetx),int(main_top[i][1]*4+offsety)))
            print(main_top[i][0],main_top[i][1])
            print(windll.gdi32.GetPixel(self.vwin.hdc,i,i))
            if main_top[i][2]!=windll.gdi32.GetPixel(self.vwin.hdc,main_top[i][0]*4+offsetx,main_top[i][1]*4+offsety):
                flag=False
                break
##        if flag==True:
##            windll.user32.keybd_event(0x44,0,0,0)   ##D
##            time.sleep(0.1)
##            windll.user32.keybd_event(0x44,0,0x0002,0)   ##D
##            windll.gdi32.DeleteDC(self.vwin.hdc)
##            windll.gdi32.DeleteObject(hbmp)
##            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
##            return
##        flag=True
##        print("hdc raw",windll.gdi32.GetPixel(raw_hdc,offsetx,offsety))
##        input("pause")
        print("copied hdc",windll.gdi32.GetPixel(self.vwin.hdc,0,0))
        input("pause")
##        for i in range(3):
####            input("pause1")
##            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
##            x=main_bottom[i][0]*4+offsetx
##            y=main_bottom[i][1]*4+offsety
##            if main_bottom[i][2]!=windll.gdi32.GetPixel(self.vwin.hdc,int(x),int(y)):
##                flag=False
##                break
##            
##        if flag==True:
##            windll.user32.keybd_event(0x44,0,0,0)   ##D
##            time.sleep(0.1)
##            windll.user32.keybd_event(0x44,0,0x0002,0)   ##D
##            windll.gdi32.DeleteDC(self.vwin.hdc)
##            windll.gdi32.DeleteObject(hbmp)
##            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
##            return
##        input("pause")        
        for i in range(horizontal):
            count_black=0
            j=0
            while j<vertical:
                x=i*4+offsetx#self.vwin.ptClientUL.x-self.vwin.rcClient.left
                y=j*4+offsety#self.vwin.ptClientUL.y-self.vwin.rcClient.top
##                print(x,y)
                temp=windll.gdi32.GetPixel(self.vwin.hdc,x,y)
##                print(temp)
##                input("pause")
##                if temp!=-1 and temp!=0xFFFFFF:
                if temp==0:
                    count_black=count_black+1
##                    print(x,y)
##                    print(i,j)
##                    print(temp)
##                    input("pause")
                    j=j+1
                else:
                    print(temp,i,j)
                    input("pause")
                    cout_black=0
                    j=j+1
            if count_black>28 and (first==0 or i==first+2):
                first=i
                print("First",first)
                black_bars=black_bars+1
                print("Black_bars")
                if black_bars==2:
                    break
##            print("Vertical Line: ",i,count_black)
##            input("pause")
##        print("LOGPIXELX",windll.gdi32.GetDeviceCaps(self.vwin.hdc,4))
##        print("LOGPIXELY",windll.gdi32.GetDeviceCaps(self.vwin.hdc,6))
        print("XLENGTH",self.vwin.ptClientLR.x-self.vwin.ptClientUL.x)
        print("YLENGTH",self.vwin.ptClientLR.y-self.vwin.ptClientUL.y)
##        windll.user32.keybd_event(0x22,0,0,0) ##PAGE DOWN
##        windll.user32.keybd_event(0x26,0,0,0)   ##UP
##        windll.user32.keybd_event(0x28,0,0,0)   ##DOWN
##        windll.user32.keybd_event(0x25,0,0,0)   ##LEFT
##        windll.user32.keybd_event(0x27,0,0,0)   ##RIGHT
##        windll.user32.keybd_event(0x53,0,0,0)   ##S
##        windll.user32.keybd_event(0x44,0,0,0)   ##D
##        windll.user32.keybd_event(0x0D,0,0,0)   ##ENTER
##        windll.user32.keybd_event(0x20,0,0,0)   ##SPACE
##        windll.gdi32.DeleteDC(self.vwin.hdc)
##        windll.gdi32.DeleteDC(hdc_compact)
##        windll.gdi32.DeleteObject(hbmp)
        windll.user32.ReleaseDC(self.hwnd,raw_hdc)
        windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
##        windll.user32.ReleaseDC(self.hwnd,self.vwin.temp_Hdc)
        ##MESSAGE BOX##
        if black_bars==2:
            print("key press")
            windll.user32.keybd_event(0x44,0,0,0)   ##D
            time.sleep(0.1)
            windll.user32.keybd_event(0x44,0,0x0002,0)   ##D            
        return
