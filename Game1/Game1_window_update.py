###This file is designed to translate the Using Rectangles code from C++
##to python
from ctypes import *
from ctypes.wintypes import *
from Points import *
import cv2
import random

##DEFINE CONSTANTS
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
WHITENESS=0x00FF0062
SRCERASE=0x00440328
SRCAND=0x008800C6
ALTERNATE=0x0001
WINDING = 0x0002

##DEFINE STRUCTURES
class RGBQUAD(Structure):
    _fields_=[('rgbBlue',BYTE),
             ('rgbGreen',BYTE),
             ('rgbRed',BYTE),
             ('rgbReserved',BYTE)]
    
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

class LOGBRUSH(Structure):
    _fields_=[("lbStyle",c_uint),
              ("lbColor",COLORREF),
              ("lbHatch",POINTER(c_ulong))]
    

class RECT(Structure):
    _fields_=[#("hdc",HDC),
              ("left",c_long),
              ("top",c_long),
              ("right",c_long),
              ("bottom",c_long)]
class POINT(Structure):
    _fields_=[("x",c_int),
              ("y",c_int)]
class POINT_ARRAY(Structure):
    _fields_=[("array",POINT*17)]
class BITMAP(Structure):
    _fields_=[("bmType",c_long),
              ("bmWidth",c_long),
              ("bmHeight",c_long),
              ("bmWidthBytes",c_long),
              ("bmPlanes",WORD),
              ("bmBitsPixel",WORD),
              ("bmBits",LPVOID)]#POINTER(BYTE))]#BYTE*1)]POINTER(BYTE*1))]#L
    

class PAINTSTRUCT(Structure):
    _fields_=[("hdc",HDC),
              ("fErase",c_bool),
              ("rcPaint", RECT),
              ("fRestore",c_bool),
              ("fIncUpdate",c_bool),
              ("rgbReserved", BYTE*32)]
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

class COUNTRY(Structure):
    _fields_=[("Team",c_int),                   ##Who currently occupies a country
              ("Num_armies",c_int),
              ("Token_point",POINT),
              ("region",HRGN)]

class PLAYER(Structure):
    _fields_=[("Team",c_int),
              ("Num_countries",c_int),
              ("Num_armies",c_int)]              ##Number of armies in hand

class MainWndProc_var(Structure):
    _fields_=[("hdc",HDC),                      ##device context(DC) for window
              ("rcTmp",RECT),                   ##temporary rectangle
              ("ps",PAINTSTRUCT),               ##paint data for BeginPaint and End Paint
              ("ptClientUL",POINT),             ##client area upper left corner
              ("ptClientLR",POINT),             ##client area lower right corner
              ("hdcCompat_main",HDC),           ##DC for copying main map bitmap
              ("hdcCompat_gray",HDC),           ##DC for copying gray map bitmap
              ("hdcCompat_token",HDC*2),          ##DC for copying blue and red token pieces
              ("pt",POINT),                     ##x and y coordinates of cursor
              ("rcBmp",RECT),                   ##rectangle that encloses bitmap
              ("rcSelect",RECT*2),              ##rectangle for selecting armies
              ("rcTarget",RECT),                ##rectangle to receive bitmap
              ("rcClient",RECT),                ##client-area rectangle
              ("fDragRect",c_bool),             ##TRUE if bitmap rect. is dragged
              ("hbmp_main",HBITMAP),            ##handle of bitmap to main map
              ("hbmp_gray",HBITMAP),            ##handle of bitmap to gray map
              ("hbmp_token",HBITMAP*2),         ##handle of bitmap to blue token and red tokens
              ("hbrBkgnd",HBRUSH),              ##handle of background-color brush
              ("Bkgnd_token",COLORREF*2),      ##handle of background-color brush for tokens
              ("crBkgnd",COLORREF),             ##color of client-area background
              ("hpenDot",HPEN),                 ##handle of dotted pen
              ("hpenDot_player",HPEN*2),                 ##handle of dotted pen              
              ("hPalette",HPALETTE),            ##Palette
              ("hOldPalette",HPALETTE),         ##Old Palette
              ("hOldBitmap",HBITMAP),
              ("region",HRGN*43),               ##Regions for the countries
              ("token_region",HRGN),             ##Region for the tokens
              ("SelectedRgn",c_int),            ##Region currently selected
              ("SelectedRgn_ATTACK",c_int),            ##Region currently selected
              ("SelectedRgn_DEFEND",c_int),            ##Region currently selected
              ("hbmp_Next_button",HBITMAP*2),
              ("hdcCompat_Next_button",HDC*2),
              ("hbmp_Confirm_button",HBITMAP*2),
              ("hdcCompat_Confirm_button",HDC*2),
              ("rcConfirm_button",RECT),               ##Box for Confirm
              ("toggle_Next_button",c_bool),
              ("toggle_Confirm_button",c_int),  ##0-hide, 1-Unselected, 2-Selected
              ("rcNext_button",RECT),
              ("rcMessage_box",RECT),
              ("bitmapheader",BITMAPINFOHEADER),##BITMAPINFOHEADER for creating a compatible bitmap
              ("bitmapinfo",BITMAPINFO),
              ("test",BYTE*1115136),#836352),
              ("temp2",POINTER(BYTE*1115136)),
              ("test2",BYTE*836352),
              ("t",c_ulong*278784),#BYTE*1115136),
              ("Countries",COUNTRY*42),
              ("bm",BITMAP),
              ("place",c_bool),                 ##For selecting the number of armies
              ("num_adding",c_int),             ##Number of armies to be added
              ("num_attacking",c_int),             ##Number of armies to attack with
              ("Phase",c_int),                  ##What phase of the turn
              ("Player",c_int),                 ##Which players turn is it
              ("windowmove",c_bool),
              ("All_Players",PLAYER*2),
              ("bm_token",BITMAP)]                    ##Bitmap tracker
class hInstance(Structure):
    _fields_=[('hInstance',HANDLE)]

##DEFINE FUNCTIONS
def REGION(reg):
    points=REGION_POINTS(reg)
    Rgn=POINT*len(points)
    temp=[]
    for i in range(len(points)):
        temp.append(POINT(points[i][0],points[i][1]))
    out=Rgn(*temp)
    return out

def TOKEN_REGION(x,y):
    points=TOKEN_POINTS(x,y)
    Rgn=POINT*len(points)
    temp=[]
    for i in range(len(points)):
        temp.append(POINT(points[i][0],points[i][1]))
    out=Rgn(*temp)
    return out

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

def DICE_ROLL():
    return int(random.random()*7)

def FAST_DICE(num_attacking,num_defending):
    attacking=num_attacking
    defending=num_defending
    diceA=[0,0,0]
    diceD=[0,0]
    while(attacking>0 and defending>0):
        num_att=min([3,attacking])
        num_def=min([2,defending])
        for i in range(3):
            if i<num_att:
                diceA[i]=DICE_ROLL()
            if i<num_def:
                diceD[i]=DICE_ROLL()
        diceA.sort(reverse=True)
        diceD.sort(reverse=True)
        ##COMPARE##
        if diceA[0]>diceD[0]:
            defending=defending-1
            if min([num_att,num_def])==2:
                if diceA[1]>diceD[1]:
                    defending=defending-1
                else:
                    attacking=attacking-1
        else:
            attacking=attacking-1
            if min([num_att,num_def])==2:
                if diceA[1]>diceD[1]:
                    defending=defending-1
                else:
                    attacking=attacking-1
    return [attacking,defending]      
            
##DEFINE CLASS##

class MainWndProc:
    def __init__(self,hwnd,uMsg,wParam,lparam,hInst):
        self.hwnd=hwnd
        ps=PAINTSTRUCT()
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
                160:"WM_NCMOUSEMOVE",161:"WM_NCLBUTTONDOWN",513: "WM_LBUTTONDOWN", 514:"WM_LBUTTONUP", 512: "WM_MOUSEMOVE"}
        Message=inputs.get(self.uMsg,"Invalid")
##        print('success',Message, " ", self.uMsg)
        method=getattr(self,Message,lambda:"Invalid message")
        return method()

    def WM_CREATE(self):
        ##LOAD MAIN MAP##
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Risk_game_map_plain.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        LoadImage=windll.user32.LoadImageW
        LoadImage.restype=HBITMAP
        LoadImage.argtypes = [HINSTANCE, LPCWSTR, UINT, c_int, c_int, UINT]
        self.vwin.hbmp_main=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)#LR_DEFAULTSIZE|c_void_p()8192|
        ##LOAD MAIN MAP GRAY##
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Risk_game_map_gray.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_gray=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        ##LOAD TOKENS##
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\red_token.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_token[0]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\blue_token.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_token[1]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        ##LOAD BUTTONS##
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Next_button_up.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_Next_button[0]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Next_button_down.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_Next_button[1]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Confirm_box.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_Confirm_button[0]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Confirmed_box.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_Confirm_button[1]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        ##GET DC FROM WINDOW INSURE ITS COLOR##
        self.vwin.hdc=windll.user32.GetDC(self.hwnd)
        windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
        windll.gdi32.GetObjectA(self.vwin.hbmp_main,ctypes.sizeof(BITMAP),pointer(self.vwin.bm))
        windll.gdi32.GetObjectA(self.vwin.hbmp_token[0],ctypes.sizeof(BITMAP),pointer(self.vwin.bm_token))
        ##CREATE MEMORY DCS FOR EACH OBJECT AND ADD THE BITMAPS##
        self.vwin.hdcCompat_main=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_gray=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_token[0]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_token[1]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_Next_button[0]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_Next_button[1]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_Confirm_button[0]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_Confirm_button[1]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        windll.gdi32.SelectObject(self.vwin.hdcCompat_main,self.vwin.hbmp_main)
        windll.gdi32.SelectObject(self.vwin.hdcCompat_gray,self.vwin.hbmp_gray)
        windll.gdi32.SelectObject(self.vwin.hdcCompat_token[0],self.vwin.hbmp_token[0])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_token[1],self.vwin.hbmp_token[1])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Next_button[0],self.vwin.hbmp_Next_button[0])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Next_button[1],self.vwin.hbmp_Next_button[1])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Confirm_button[0],self.vwin.hbmp_Confirm_button[0])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Confirm_button[1],self.vwin.hbmp_Confirm_button[1])
        ##CREATE REGIONS FOR EACH COUNTRY AND INITIALIZE TOKEN POINTS##
        self.vwin.SelectedRgn=0
        CreatePolygonRgn=windll.gdi32.CreatePolygonRgn
        for i in range(42):
            Points=REGION(i+1)
            Points_place=COUNTRY_POINTS(i+1)
            self.vwin.Countries[i].region=CreatePolygonRgn(Points,len(Points),WINDING)
            self.vwin.Countries[i].Token_point.x=Points_place[0]
            self.vwin.Countries[i].Token_point.y=Points_place[1]
            self.vwin.Countries[i].Team=i%2
            self.vwin.All_Players[i%2].Num_countries=self.vwin.All_Players[i%2].Num_countries+1
            self.vwin.Countries[i].Num_armies=i
        ##GET TOKEN INFO##
        windll.gdi32.SelectObject(self.vwin.ps.hdc,self.vwin.token_region)
        ##ASSIGN PHASE AND PLAYER##
        self.vwin.Phase=0
        self.vwin.Player=0
        ##INITIALIZE PLAYERS
        for i in range(len(self.vwin.All_Players)):
            self.vwin.All_Players[i].Team=i
            self.vwin.All_Players[i].Num_armies=-1
        self.vwin.place=False
        ##Select the background color, the default is white
        ##Create a brush of the same color as the background
        ##of the client area. The brush is used later to erase
        ##the old bitmap before copying the bitmap into the
        ##target rectangle
        windll.gdi32.SetBkColor(self.vwin.hdc,RGB(150,150,150))
        self.vwin.Bkgnd_token[0]=windll.gdi32.GetPixel(self.vwin.hdcCompat_token[0],10,10)
        self.vwin.Bkgnd_token[1]=windll.gdi32.GetPixel(self.vwin.hdcCompat_token[1],10,10)
        self.vwin.crBkgnd=windll.gdi32.GetBkColor(self.vwin.hdc)
        self.vwin.hbrBkgnd=windll.gdi32.CreateSolidBrush(self.vwin.crBkgnd)
        windll.gdi32.SelectObject(self.vwin.hdcCompat_main,self.vwin.hbrBkgnd)
        windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        ##Create a dotted pen. The pen is used to draw the
        ##bitmap rectangle as the user drags it.
        self.vwin.hpenDot=windll.gdi32.CreatePen(PS_DOT,2,RGB(150,0,0))
        self.vwin.hpenDot_player[0]=windll.gdi32.CreatePen(PS_DOT,2,RGB(0,0,150))
        self.vwin.hpenDot_player[1]=windll.gdi32.CreatePen(PS_DOT,2,RGB(150,0,0))
        ##Set the initial rectangle for the bitmap. Note that
        ##this aplication supports only a 32- by 32 pixel
        ##bitmap. The rectangle is slightly larger than the
        ##bitmap
        windll.user32.SetRect(pointer(self.vwin.rcBmp),1,1,34,34)
        windll.user32.SetRect(pointer(self.vwin.rcNext_button),500,700,500+160,700+35)
        windll.user32.SetRect(pointer(self.vwin.rcMessage_box),1,501,1+160,501+250)
        windll.user32.SetRect(pointer(self.vwin.rcSelect[0]),5,600,155,600+10)
        windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
        windll.user32.SetRect(pointer(self.vwin.rcConfirm_button),1,700,1+160,700+35)
        return 0
    def WM_PAINT(self):
        ##Draw the bitmap rectangle and copy the bitmap into
        ##it. The 32-pixel by 32-pixel bitmap is centered in
        ##the rectangle by adding 1 to the left and top
        ##coordinates of the bitmap rectangle, and subtracting 2
        ##from the right and bottom coordinates.
        windll.user32.BeginPaint(self.hwnd,pointer(self.vwin.ps))
        if (self.vwin.ps.rcPaint.bottom-self.vwin.ps.rcPaint.bottom)==0:
            windll.user32.EndPaint(self.hwnd,pointer(self.vwin.ps))
            self.vwin.ps.hdc=windll.user32.GetDC(self.hwnd)
        ##FILL OUT MAINMAP##
        windll.gdi32.SelectObject(self.vwin.ps.hdc,None)
        windll.gdi32.Rectangle(self.vwin.ps.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
                               self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)
        windll.gdi32.BitBlt(self.vwin.ps.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
        windll.gdi32.StretchBlt(self.vwin.ps.hdc,self.vwin.rcNext_button.left,self.vwin.rcNext_button.top,
                                (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                self.vwin.hdcCompat_Next_button[0],0,0,
                                (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                SRCCOPY)
        self.vwin.toggle_Next_button=False
        self.vwin.toggle_Confirm_button=0
        windll.gdi32.SelectObject(self.vwin.ps.hdc,windll.gdi32.CreatePen(PS_DOT,2,RGB(0,0,0)))
        windll.gdi32.Rectangle(self.vwin.ps.hdc,self.vwin.rcMessage_box.left-1,self.vwin.rcMessage_box.top-1,
                               self.vwin.rcMessage_box.right+1,self.vwin.rcMessage_box.bottom+1)
        windll.user32.FillRect(self.vwin.ps.hdc,pointer(self.vwin.rcMessage_box),self.vwin.hbrBkgnd)
        for i in range(42):
            player=self.vwin.Countries[i].Team
            if player>-1:
                windll.gdi32.SetBkColor(self.vwin.ps.hdc,self.vwin.Bkgnd_token[player])
                point=self.vwin.Countries[i].Token_point
                Points=TOKEN_REGION(point.x,point.y)
                soldiers=self.vwin.Countries[i].Num_armies
                windll.gdi32.SelectClipRgn(self.vwin.ps.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                windll.gdi32.StretchBlt(self.vwin.ps.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                    int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                    0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                      point.y+int(self.vwin.bm_token.bmHeight*.05),
                                      point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                windll.user32.DrawTextW(self.vwin.ps.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
        ##CREATE BORDER##
        windll.gdi32.SelectClipRgn(self.vwin.ps.hdc,None)
        windll.gdi32.SelectObject(self.vwin.ps.hdc,self.vwin.hpenDot_player[self.vwin.Player])
        windll.gdi32.Rectangle(self.vwin.ps.hdc,1,1,
                               self.vwin.rcClient.right-self.vwin.rcClient.left,self.vwin.rcClient.bottom-self.vwin.rcClient.top)
        
        if (self.vwin.ps.rcPaint.bottom-self.vwin.ps.rcPaint.bottom)==0:
            windll.user32.ReleaseDC(self.hwnd,self.vwin.ps.hdc)
        else:
            windll.user32.EndPaint(self.hwnd,pointer(self.vwin.ps))
        return
    def WM_NCLBUTTONDOWN(self):
        self.vwin.windowmove=True
        return
    def WM_NCMOUSEMOVE(self):
        if self.vwin.windowmove==True:
            self.WM_SIZE()
            self.vwin.windowmove=False
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
        print('('+str(int(self.vwin.pt.x*1)+int(1227*0))+','+str(int(self.vwin.pt.y*1)+int(628*0))+'),')
        ##Temp variables
        temp=None
        temp2=None
        self.vwin.place=False
        ##PLACE ARMIES PHASE1##
        if self.vwin.Phase==0:
            ##GAIN ARMIES##
            if self.vwin.All_Players[self.vwin.Player].Num_armies==-1:
                self.vwin.All_Players[self.vwin.Player].Num_armies=int(self.vwin.All_Players[self.vwin.Player].Num_countries/3)
                ##MINIMUM REINFORCEMENTS##
                if self.vwin.All_Players[self.vwin.Player].Num_armies<3:
                    self.vwin.All_Players[self.vwin.Player].Num_armies=3
                ##CONTINENT BONUS##
                NA=SA=EU=AF=AS=AU=0
                Bonus=0
                for i in range(42):
                    if self.vwin.Player==self.vwin.Countries[i].Team:
                        if i<9:
                            NA=NA+1
                        elif i<13:
                            SA=SA+1
                        elif i<20:
                            EU=EU+1
                        elif i<26:
                            AF=AF+1
                        elif i<38:
                            AS=AS+1
                        else:
                            AU=AU+1
                if NA==9:
                    Bonus=Bonus+5
                if SA==4:
                    Bonus=Bonus+2
                if EU==7:
                    Bonus=Bonus+5
                if AF==6:
                    Bonus=Bonus+3
                if AS==12:
                    Bonus=Bonus+7
                if AU==4:
                    Bonus=Bonus+2
                self.vwin.All_Players[self.vwin.Player].Num_armies=self.vwin.All_Players[self.vwin.Player].Num_armies+Bonus
                            
            ##SELECT COUNTRY TO PLACE ARMIES##
            previous_SelectedRgn=self.vwin.SelectedRgn
            if windll.user32.PtInRect(pointer(self.vwin.rcMessage_box),self.vwin.pt)==False:
                self.vwin.SelectedRgn=0
                self.vwin.toggle_Confirm_button=0
            ##Determine selected region##
                self.vwin.hdc=windll.user32.GetDC(self.hwnd)
                for i in range(42):
                    if windll.gdi32.PtInRegion(self.vwin.Countries[i].region,self.vwin.pt.x,self.vwin.pt.y):
                        temp=self.vwin.Countries[i].region
                        self.vwin.SelectedRgn=i+1
                        break
                ##Remove previously highlighted region and replace token
                if previous_SelectedRgn!=0 and self.vwin.place==False:
                    temp2=self.vwin.Countries[previous_SelectedRgn-1].region
                    windll.gdi32.SelectClipRgn(self.vwin.hdc,temp2)
                    windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
                    player=self.vwin.Countries[previous_SelectedRgn-1].Team
                    if player>-1:
                        windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.Bkgnd_token[player])
                        point=self.vwin.Countries[previous_SelectedRgn-1].Token_point
                        Points=TOKEN_REGION(point.x,point.y)
                        soldiers=self.vwin.Countries[previous_SelectedRgn-1].Num_armies
                        windll.gdi32.SelectClipRgn(self.vwin.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                        windll.gdi32.StretchBlt(self.vwin.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                            int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                            0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                        windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                              point.y+int(self.vwin.bm_token.bmHeight*.05),
                                              point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                        windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
                        

                ##Highlight Region##
                if temp!=None:
                    windll.gdi32.SelectClipRgn(self.vwin.hdc,temp)
                    windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_gray,0,0,SRCCOPY)
                    windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
            ##CHOOSE NUMBER OF ARMIES TO PLACE##
            if self.vwin.SelectedRgn>0:
                if self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player:
                    if windll.user32.PtInRect(pointer(self.vwin.rcSelect[1]),self.vwin.pt):
                        self.vwin.place=True
                        self.vwin.num_adding=0
                        self.vwin.toggle_Confirm_button=1
                    elif windll.user32.PtInRect(pointer(self.vwin.rcConfirm_button),self.vwin.pt) and self.vwin.toggle_Confirm_button==1:
                        windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcConfirm_button.left,self.vwin.rcConfirm_button.top,
                        (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                        self.vwin.hdcCompat_Confirm_button[1],0,0,
                        (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                        SRCCOPY)
                        self.vwin.toggle_Confirm_button=2
                        self.vwin.Countries[self.vwin.SelectedRgn-1].Num_armies=self.vwin.Countries[self.vwin.SelectedRgn-1].Num_armies+self.vwin.num_adding
                        self.vwin.All_Players[self.vwin.Player].Num_armies=self.vwin.All_Players[self.vwin.Player].Num_armies-self.vwin.num_adding
                        ##REINITIALIZE ARMY SELECTOR##
                        self.vwin.num_adding=0
                        windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        ##ATTACK PHASE2##
        elif self.vwin.Phase==1:
            self.vwin.All_Players[self.vwin.Player].Num_armies=-1
            ##SELECT COUNTRY TO ATTACK##
            previous_SelectedRgn=self.vwin.SelectedRgn
            if windll.user32.PtInRect(pointer(self.vwin.rcMessage_box),self.vwin.pt)==False:
                self.vwin.SelectedRgn=0
                self.vwin.toggle_Confirm_button=0
            ##Determine selected region##
                self.vwin.hdc=windll.user32.GetDC(self.hwnd)
                for i in range(42):
                    if windll.gdi32.PtInRegion(self.vwin.Countries[i].region,self.vwin.pt.x,self.vwin.pt.y):
                        temp=self.vwin.Countries[i].region
                        self.vwin.SelectedRgn=i+1
                        break
                ##Remove previously highlighted region and replace token
                if previous_SelectedRgn!=0 and self.vwin.place==False:
                    ##CLEAR ATTACK SELECTED COUNTRY##
                    if (self.vwin.SelectedRgn_ATTACK==0 or (self.vwin.SelectedRgn_ATTACK!=0 and self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player) or (ADJACENT(self.vwin.SelectedRgn_ATTACK,self.vwin.SelectedRgn)==False and self.vwin.SelectedRgn!=0) and self.vwin.SelectedRgn_DEFEND==0):
                        if self.vwin.SelectedRgn_ATTACK!=0:
                            previous_SelectedRgn=self.vwin.SelectedRgn_ATTACK
                            self.vwin.SelectedRgn_ATTACK=0                                                           
                        temp2=self.vwin.Countries[previous_SelectedRgn-1].region
                        windll.gdi32.SelectClipRgn(self.vwin.hdc,temp2)
                        windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
                        player=self.vwin.Countries[previous_SelectedRgn-1].Team
                        if player>-1:
                            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.Bkgnd_token[player])
                            point=self.vwin.Countries[previous_SelectedRgn-1].Token_point
                            Points=TOKEN_REGION(point.x,point.y)
                            soldiers=self.vwin.Countries[previous_SelectedRgn-1].Num_armies
                            windll.gdi32.SelectClipRgn(self.vwin.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                            windll.gdi32.StretchBlt(self.vwin.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                                int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                                0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                            windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                                  point.y+int(self.vwin.bm_token.bmHeight*.05),
                                                  point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
                    elif self.vwin.SelectedRgn_DEFEND!=0:
                        ##CLEAR ATTACK SELECTED COUNTRY##
                        temp2=self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].region
                        windll.gdi32.SelectClipRgn(self.vwin.hdc,temp2)
                        windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
                        player=self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Team
                        if player>-1:
                            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.Bkgnd_token[player])
                            point=self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Token_point
                            Points=TOKEN_REGION(point.x,point.y)
                            soldiers=self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Num_armies
                            windll.gdi32.SelectClipRgn(self.vwin.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                            windll.gdi32.StretchBlt(self.vwin.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                                int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                                0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                            windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                                  point.y+int(self.vwin.bm_token.bmHeight*.05),
                                                  point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
                        ##CLEAR DEFEND SELECTED COUNTRY##
                        temp2=self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].region
                        windll.gdi32.SelectClipRgn(self.vwin.hdc,temp2)
                        windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
                        player=self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Team
                        if player>-1:
                            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.Bkgnd_token[player])
                            point=self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Token_point
                            Points=TOKEN_REGION(point.x,point.y)
                            soldiers=self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Num_armies
                            windll.gdi32.SelectClipRgn(self.vwin.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                            windll.gdi32.StretchBlt(self.vwin.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                                int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                                0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                            windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                                  point.y+int(self.vwin.bm_token.bmHeight*.05),
                                                  point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
                        self.vwin.SelectedRgn_DEFEND=0
                        self.vwin.SelectedRgn_ATTACK=0

                ##Highlight Regions##
                if temp!=None:
                    windll.gdi32.SelectClipRgn(self.vwin.hdc,temp)
                    windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_gray,0,0,SRCCOPY)
                    windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
                    if self.vwin.SelectedRgn_ATTACK==0 and self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player:
                        self.vwin.SelectedRgn_ATTACK=self.vwin.SelectedRgn
                    elif self.vwin.SelectedRgn_ATTACK!=0 and self.vwin.Countries[self.vwin.SelectedRgn-1].Team!=self.vwin.Player:
                        self.vwin.SelectedRgn_DEFEND=self.vwin.SelectedRgn
            ##SELECT ARMIES FOR ATTACKING##
            if windll.user32.PtInRect(pointer(self.vwin.rcSelect[1]),self.vwin.pt) and self.vwin.SelectedRgn_DEFEND!=0:
                self.vwin.place=True
                self.vwin.num_attacking=0
                self.vwin.toggle_Confirm_button=1
            elif windll.user32.PtInRect(pointer(self.vwin.rcConfirm_button),self.vwin.pt) and self.vwin.toggle_Confirm_button==1:
                    windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcConfirm_button.left,self.vwin.rcConfirm_button.top,
                    (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                    self.vwin.hdcCompat_Confirm_button[1],0,0,
                    (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                    SRCCOPY)
                    self.vwin.toggle_Confirm_button=2
                    defending= self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Num_armies
                    armies_left=self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Num_armies-self.vwin.num_attacking
                    defend_player=self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Team
                    [self.vwin.num_attacking,defending]=FAST_DICE(self.vwin.num_attacking,defending)
                    ##DEFENSE WINS##
                    if defending>0:
                        self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Num_armies=defending
                        self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Num_armies=self.vwin.num_attacking+armies_left
                    ##ATTACKER WINS##
                    else:
                        self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Num_armies=self.vwin.num_attacking
                        self.vwin.Countries[self.vwin.SelectedRgn_DEFEND-1].Team=self.vwin.Player
                        self.vwin.All_Players[self.vwin.Player].Num_countries=self.vwin.All_Players[self.vwin.Player].Num_countries+1
                        self.vwin.All_Players[defend_player].Num_countries=self.vwin.All_Players[defend_player].Num_countries-1
                        self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Num_armies=armies_left    
                    ##REINITIALIZE ARMY SELECTOR##
                    self.vwin.num_attacking=0
                    windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        elif self.vwin.Phase==2:
            self.vwin.SelectedRgn_ATTACK=0
            self.vwin.SelectedRgn_DEFEND=0
        ##ADVANCE TO THE NEXT PHASE##
        if (windll.user32.PtInRect(pointer(self.vwin.rcNext_button),self.vwin.pt)):
            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            windll.gdi32.SelectObject(self.vwin.hdc,None)
            windll.gdi32.SelectClipRgn(self.vwin.hdc,None)
            ##PLACE NEXT BUTTON##
            if self.vwin.All_Players[self.vwin.Player].Num_armies<=0:
                windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcNext_button.left,self.vwin.rcNext_button.top,
                                (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                self.vwin.hdcCompat_Next_button[1],0,0,
                                (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                SRCCOPY)
                self.vwin.toggle_Next_button=True
                self.vwin.All_Players[self.vwin.Player].Num_armies=-1
                if self.vwin.Phase<2:
                    self.vwin.Phase=self.vwin.Phase+1
                else:
                    self.vwin.Phase=0
                    ##CONTINUE TO THE NEXT PLAYERS TURN##
                    if self.vwin.Player<(len(self.vwin.All_Players)-1):
                        self.vwin.Player=self.vwin.Player+1
                    else:
                        self.vwin.Player=0
                    ##REMOVE PREVIOUS PLAYER BORDER##
                    current=self.vwin.Player
                    past=self.vwin.Player-1
                    if past==-1:
                        past=len(self.vwin.All_Players)-1
                    windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot_player[past])
                    windll.gdi32.Rectangle(self.vwin.ps.hdc,1,1,
                                           self.vwin.rcClient.right-self.vwin.rcClient.left,self.vwin.rcClient.bottom-self.vwin.rcClient.top)
                    ##DRAW NEW BORDER##
                    windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot_player[current])
                    windll.gdi32.Rectangle(self.vwin.ps.hdc,1,1,
                                           self.vwin.rcClient.right-self.vwin.rcClient.left,self.vwin.rcClient.bottom-self.vwin.rcClient.top)
                
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
            
        return 0
    def WM_MOUSEMOVE(self):
        inputs={1:"MK_LBUTTON"}
        MK_LBUTTON=inputs.get(self.wParam,False)
        ##Draw a target rectangle or drag the bitmap rectangle,
        ##Depending on the status of the fDragRect flag
        if((self.wParam and MK_LBUTTON) and self.vwin.place==True):
            ##Erase the previous rectangle and draw the next one if still on bar##
            if(self.lParam.x-self.vwin.pt.x+self.vwin.rcSelect[1].left)>5 and (self.lParam.x-self.vwin.pt.x+self.vwin.rcSelect[1].right)<156:
                self.vwin.hdc=windll.user32.GetDC(self.hwnd)
                windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
                windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot)
                windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcSelect[1].left,self.vwin.rcSelect[1].top,
                                       self.vwin.rcSelect[1].right,self.vwin.rcSelect[1].bottom)
                ##Draw new rectangle
                windll.user32.OffsetRect(pointer(self.vwin.rcSelect[1]),self.lParam.x-self.vwin.pt.x,0)

                windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcSelect[1].left,self.vwin.rcSelect[1].top,
                                       self.vwin.rcSelect[1].right,self.vwin.rcSelect[1].bottom)

                windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)

                ##Save the coordinates of the mouse cursor.
            center=(self.vwin.rcSelect[1].left+self.vwin.rcSelect[1].right)/2
            if self.vwin.Phase==0:
                self.vwin.num_adding=int(self.vwin.All_Players[self.vwin.Player].Num_armies*(center-10)/140+.5)
            elif self.vwin.Phase==1:
                num_armies=self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Num_armies-1
                self.vwin.num_attacking=int(num_armies*(center-10)/140+.5)
            
            self.vwin.pt.x=self.lParam.x
            self.vwin.pt.y=self.lParam.y            

        return 0
    def WM_LBUTTONUP(self):
##        input("pause")
        ##If the bitmap rectangle and target rectangle
        ##intersect, copy the bitmap into the target
        ##rectangle. Otherwise, copy the bitmap into the
        ##rectangle bitmap at its new location.
        ##UPDATE MESSAGEBOX##
        self.vwin.hdc=windll.user32.GetDC(self.hwnd)
        windll.gdi32.SelectClipRgn(self.vwin.hdc,None)
        #Clear previous message box#
        windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcMessage_box),self.vwin.hbrBkgnd)
        #Update Message Box#
        if self.vwin.SelectedRgn>0:
            ##Fill out message box##
            teams={0:"Red",1:"Blue"}
            country=self.vwin.Countries[self.vwin.SelectedRgn-1]
            info="Country: "+str(self.vwin.SelectedRgn)+"\n"
            info=info+"Owned by: "+teams[country.Team]+"\n"
            info=info+"Num of Armies: "+str(country.Num_armies)+"\n"
            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.crBkgnd)
            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(info),-1,pointer(self.vwin.rcMessage_box),0)
            ##FOR SELECTING ARMIES##
            if self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player and self.vwin.Phase!=1:
                info=info+"MOVE "+str(self.vwin.num_adding)+" ARMIES"
                info=info+"\n\n\n\n\n\n\n"+"NUM OF ARMIES LEFT:\n"
                info=info+str(self.vwin.All_Players[self.vwin.Player].Num_armies-self.vwin.num_adding)
                windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcSelect[0]),
                                       windll.gdi32.CreateSolidBrush(RGB(150,0,0)))
                windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot)
                windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcSelect[1].left,self.vwin.rcSelect[1].top,
                                   self.vwin.rcSelect[1].right,self.vwin.rcSelect[1].bottom)
            elif self.vwin.SelectedRgn_DEFEND!=0 and self.vwin.Phase==1:
                info=info+"ATTACK WITH "+str(self.vwin.num_attacking)
                info=info+"\n\n\n\n\n\n\n"+"NUM OF ARMIES LEFT:\n"
                info=info+str(self.vwin.Countries[self.vwin.SelectedRgn_ATTACK-1].Num_armies-self.vwin.num_attacking)
                windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcSelect[0]),
                                       windll.gdi32.CreateSolidBrush(RGB(150,0,0)))
                windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot)
                windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcSelect[1].left,self.vwin.rcSelect[1].top,
                                   self.vwin.rcSelect[1].right,self.vwin.rcSelect[1].bottom)
            if self.vwin.toggle_Confirm_button==1 or self.vwin.toggle_Confirm_button==2:
                windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcConfirm_button.left,self.vwin.rcConfirm_button.top,
                                        (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                                        self.vwin.hdcCompat_Confirm_button[0],0,0,
                                        (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                                        SRCCOPY)
                self.vwin.toggle_Confirm_bottom=1
            ##DRAW MESSAGE##
            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.crBkgnd)
            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(info),-1,pointer(self.vwin.rcMessage_box),0)
                
        if self.vwin.toggle_Next_button==True:
                windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcNext_button.left,self.vwin.rcNext_button.top,
                                        (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                        self.vwin.hdcCompat_Next_button[0],0,0,
                                        (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                        SRCCOPY)
                self.vwin.toggle_Next_button=False
        windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
##        if (windll.user32.IntersectRect(pointer(self.vwin.rcTmp),pointer(self.vwin.rcBmp),pointer(self.vwin.rcTarget))==True):
##            ##Erase the bitmap rectangle by filling it with
##            ##the background color.
##            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
##            windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcBmp),self.vwin.hbrBkgnd)
##            ##Redraw the target rectangle because the part
##            ##that intersected with the bitmap rectangle was
##            ##erased by the call to FillRect.
##            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcTarget.left,self.vwin.rcTarget.top,
##                                   self.vwin.rcTarget.right,self.vwin.rcTarget.bottom)
##            ##Copy the bitmap into the target rectangle.
##            windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcTarget.left+1,self.vwin.rcTarget.top+1,
##                                 (self.vwin.rcTarget.right-self.vwin.rcTarget.left)-2,
##                                 (self.vwin.rcTarget.bottom-self.vwin.rcTarget.top)-2,
##                                 self.vwin.hdcCompat,0,0,32,32,SRCCOPY)
##
##            ##Copy the target rectangle to the bitmap
##            ##rectangle, set the coordinates of the target
##            ##rectangle to 0, then reset the fDragRect flag.
##
##            windll.user32.CopyRect(pointer(self.vwin.rcBmp),pointer(self.vwin.rcTarget))
##            windll.user32.SetRectEmpty(pointer(self.vwin.rcTarget))
##            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
##            self.vwin.fDragRect=False
##        elif(self.vwin.fDragRect==True):
##            ##Draw the bitmap rectangle,copy the bitmap into
##            ##it, and reset the fDragRect flag
##            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
##            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
##                                   self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)
##            windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcBmp.left+1,self.vwin.rcBmp.top+1,
##                                 (self.vwin.rcBmp.right-self.vwin.rcBmp.left)-2,
##                                 (self.vwin.rcBmp.bottom-self.vwin.rcBmp.top)-2,
##                                 self.vwin.hdcCompat,0,0,32,32,SRCCOPY)
##            
##            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
##            self.vwin.fDragRect=False
##
##            ##Release the mouse cursor.
##            windll.user32.ClipCursor(pointer(self.vwin.rcClient))#pointer(RECT()))
        return 0
    def WM_DESTROY(self):
        ##Destry the background brush, compatible bitmap,
        ##and the bitmap
        windll.gdi32.DeleteObject(self.vwin.hbrBkgnd)
        windll.gdi32.DelectObject(self.vwin.region1)
        windll.gdi32.DeleteDC(self.vwin.hdcCompat_gray)
        windll.gdi32.DeleteDC(self.vwin.hdcCompat_main)
        windll.gdi32.DeleteObject(self.vwin.hbmp)
        windll.user32.PostQuitMessage(0)
        return
        
        
##a=MainWndProc(1234,"WM_CREATE",12,0)
##print(a.call_back("WM_CREATE"))
##a=Switcher()
##print(a.numbers_to_months(1))

