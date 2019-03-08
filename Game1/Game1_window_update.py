###This file is designed to translate the Using Rectangles code from C++
##to python
from ctypes import *
from ctypes.wintypes import *
from Points import *
import cv2
import random
import math

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
R2_COPYPEN=0x000D
WHITENESS=0x00FF0062
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

##DEFINE STRUCTURES
class XFORM(Structure):
    _fields_=[("eM11",c_float),
              ("eM12",c_float),
              ("eM21",c_float),
              ("eM22",c_float),
              ("eDx",c_float),
              ("eDy",c_float)]

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
class CARDS(Structure):
    _fields_=[("Type",c_int),                   ##1 for apple, 2 for walls, 3 for swords
              ("Country",c_int)]

class PLAYER(Structure):
    _fields_=[("Team",c_int),
              ("Num_countries",c_int),
              ("Cards",CARDS*5),
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
              ("hdcCompat_card",HDC*3),          ##DC for copying blue and red token pieces
              ("pt",POINT),                     ##x and y coordinates of cursor
              ("rcBmp",RECT),                   ##rectangle that encloses bitmap
              ("rcSelect",RECT*2),              ##rectangle for selecting armies
              ("rcTarget",RECT),                ##rectangle to receive bitmap
              ("rcClient",RECT),                ##client-area rectangle
              ("fDragRect",c_bool),             ##TRUE if bitmap rect. is dragged
              ("hbmp_main",HBITMAP),            ##handle of bitmap to main map
              ("hbmp_gray",HBITMAP),            ##handle of bitmap to gray map
              ("hbmp_token",HBITMAP*2),         ##handle of bitmap to blue token and red tokens
              ("hbmp_card",HBITMAP*3),         ##handle of bitmap to card pictures
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
              ("card_region",HRGN*5),           ##Regions for Cards
              ("SelectedRgn",c_int),            ##Region currently selected
              ("SelectedRgn_ATTACK",c_int),            ##Region currently selected
              ("SelectedRgn_DEFEND",c_int),            ##Region currently selected
              ("SelectedRgn_SOURCE",c_int),            ##Region currently selected
              ("SelectedRgn_DESTINATION",c_int),            ##Region currently selected
              ("SelectedRgn_CARD",c_int*3),
              ("Selected_cards",CARDS*3),       ##SELECT CARDS
              ("hbmp_Next_button",HBITMAP*2),
              ("hdcCompat_Next_button",HDC*2),
              ("hbmp_Confirm_button",HBITMAP*2),
              ("hdcCompat_Confirm_button",HDC*2),
              ("rcConfirm_button",RECT),               ##Box for Confirm
              ("toggle_Next_button",c_bool),
              ("toggle_Confirm_button",c_int),  ##0-hide, 1-Unselected, 2-Selected
              ("toggle_cards_displayed",c_bool),
              ("clear",c_bool),
              ("rcNext_button",RECT),
              ("rcMessage_box",RECT),
              ("rcCard",RECT),                  ##Outline of Card
              ("bitmapheader",BITMAPINFOHEADER),##BITMAPINFOHEADER for creating a compatible bitmap
              ("bitmapinfo",BITMAPINFO),
              ("test",BYTE*1115136),#836352),
              ("temp2",POINTER(BYTE*1115136)),
              ("test2",BYTE*836352),
              ("t",c_ulong*278784),#BYTE*1115136),
              ("Countries",COUNTRY*42),
              ("Deck",CARDS*42),
              ("Draw_card",c_int),
              ("Card_bonus",c_int),             #Bonus from cards, if -1 it has not been played yet
              ("Card_bonus_amount",c_int),
              ("Succesful_attack",c_bool),
              ("bm",BITMAP),
              ("place",c_bool),                 ##For selecting the number of armies
              ("num_adding",c_int),             ##Number of armies to be added
              ("num_attacking",c_int),          ##Number of armies to attack with
              ("num_moving",c_int),             ##Number of armies for reinforcements
              ("Phase",c_int),                  ##What phase of the turn
              ("Player",c_int),                 ##Which players turn is it
              ("windowmove",c_bool),
              ("All_Players",PLAYER*2),
              ("Transform",XFORM*5),            ##Transformations for rotating cards
              ("InvTransform",XFORM*5),            ##Transformations for rotating cards
              ("bm_token",BITMAP)]                    ##Bitmap tracker
class hInstance(Structure):
    _fields_=[('hInstance',HANDLE)]

##DEFINE FUNCTIONS
def TRANSFORM(temp,rotate,dx,dy):
    temp.eM11=math.cos(rotate)
    temp.eM12=math.sin(rotate)
    temp.eM21=-math.sin(rotate)
    temp.eM22=math.cos(rotate)
    temp.eDx=dx
    temp.eDy=dy
    return

def CARD_REGION(reg):
    points=CARD_REGIONS(reg)
    Rgn=POINT*len(points)
    temp=[]
    for i in range(len(points)):
        temp.append(POINT(points[i][0],points[i][1]))
    out=Rgn(*temp)
    return out
    

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
        ##DICTIONARY FOR MESSAGE##
        inputs={1: "WM_CREATE",2: "WM_DESTROY",3:"WM_MOVE",5: "WM_SIZE",15: "WM_PAINT",
                160:"WM_NCMOUSEMOVE",161:"WM_NCLBUTTONDOWN",513: "WM_LBUTTONDOWN", 514:"WM_LBUTTONUP", 512: "WM_MOUSEMOVE"}
        ##TRANSLATE MESSAGE##
        Message=inputs.get(self.uMsg,"Invalid")
        ##CALL FUNCTION RELATED TO MESSAGE##
        method=getattr(self,Message,lambda:"Invalid message")
        return method()
    
    def VALID_DESTINATION(self,source,destination,team):
        ##Determine if countries are adjacent##
        if ADJACENT(source,destination):
            return True
        ##Otherwise find all countries owned by the player##
        player_countries=[]
        for i in range(42):
            if self.vwin.Countries[i].Team==team:
                player_countries.append(i+1)
        ##Besides the source and destination find all countries with two or more adjacently owned countries
        player_countries_with_neighbors=[]
        player_countries2=[]
        for i in range(len(player_countries)):
            temp=ADJACENT_DATA(player_countries[i])
            temp2=[]
            for j in range(len(temp)):
                if self.vwin.Countries[temp[j]].Team==team:
                    temp2.append(temp[j])
            if len(temp2)>1:
                player_countries_with_neighbors.append(temp2)
                player_countries2.append(player_countries[i]-1)
        ##Puzzle piece them together by trying every path
        source_places=[]
        temp=ADJACENT_DATA(source)
        for i in range(len(temp)):
            if self.vwin.Countries[temp[i]].Team==team:
                source_places.append(temp[i])
        end=False
        for i in range(len(source_places)):
            if self.Check(source_places[i],player_countries_with_neighbors,player_countries2,destination):
                return True
        return False
        
    def Check(self,Previous,pcwn,pc,goal):
        cont=True
        j=0
        k=0
        temp=False
        temp2=pcwn
        previous=Previous
        temp3=pc
        temp_int=0
        runs=0
        tried=[]
        tried2=[]
        next_go=0
        while len(tried2)<len(pc):
            ##Initialize Tried##
            tried=[]
            for entries in range(len(tried2)):
                tried.append(tried2[entries])
            k=0
            j=-1
            ##Check to see if country has neighbors##
            for i in range(len(pc)):
                if pc[i]==Previous:
                    j=i
            if j==-1:
                return False
            while k<(len(pcwn[j])):
                temp=True
                #See if adjacent country has been tried
                for i in range(len(tried)):
                    if pcwn[j][k]==tried[i]:
                        temp=False
                #Is the goal adjacent to this country#
                if temp==True:
                    temp=False
                    for i in range(len(pc)):
                        if pc[i]==pcwn[j][k]:
                            next_go=i
                            temp=True
                    if temp==False:
                        k=k+1
                    elif temp==True:
                        for i in range(len(pcwn[next_go])):
                                if pcwn[next_go][i]==goal-1:
                                    return True
                        #If not add this country to list of tried countries#
                        previous=pc[next_go]
                        tried.append(previous)
                        k=0
                        j=next_go
                else:
                    k=k+1
            ##Record the dead end of the path##
            if len(tried)==0:
                return False
            tried2.append(tried[-1])
        return False
    
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
        ##LOAD CARD IMAGAES##
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Apple_Type.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_card[0]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Wall_Type.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_card[1]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
        file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\Sword_Type.bmp"
        file_pointer_main=LPCWSTR(file_path_main)
        self.vwin.hbmp_card[2]=LoadImage(c_void_p(),file_pointer_main,IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
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
        self.vwin.hdcCompat_card[0]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_card[1]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        self.vwin.hdcCompat_card[2]=windll.gdi32.CreateCompatibleDC(self.vwin.hdc)
        windll.gdi32.SelectObject(self.vwin.hdcCompat_main,self.vwin.hbmp_main)
        windll.gdi32.SelectObject(self.vwin.hdcCompat_gray,self.vwin.hbmp_gray)
        windll.gdi32.SelectObject(self.vwin.hdcCompat_token[0],self.vwin.hbmp_token[0])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_token[1],self.vwin.hbmp_token[1])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Next_button[0],self.vwin.hbmp_Next_button[0])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Next_button[1],self.vwin.hbmp_Next_button[1])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Confirm_button[0],self.vwin.hbmp_Confirm_button[0])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_Confirm_button[1],self.vwin.hbmp_Confirm_button[1])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_card[0],self.vwin.hbmp_card[0])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_card[1],self.vwin.hbmp_card[1])
        windll.gdi32.SelectObject(self.vwin.hdcCompat_card[2],self.vwin.hbmp_card[2])
        ##ALLOW CARDS TO BE ROTATED##
        TRANSFORM(self.vwin.Transform[0],-.4, 300,300-math.sin(-.4)*160*.5)
        TRANSFORM(self.vwin.Transform[1],.4, 700,300-math.sin(.4)*160*.5)
        TRANSFORM(self.vwin.Transform[2],0, 500,250)
        TRANSFORM(self.vwin.Transform[3],1.2, 900,450-math.sin(1.2)*160*.5)
        TRANSFORM(self.vwin.Transform[4],-1.2, 200,450-math.sin(-1.2)*160*.5)
        TRANSFORM(self.vwin.InvTransform[0],.4, -300,-300+math.sin(-.4)*160*.5)
        TRANSFORM(self.vwin.InvTransform[1],-.4, -700,-300+math.sin(.4)*160*.5)
        TRANSFORM(self.vwin.InvTransform[2],0, -500,-250)
        TRANSFORM(self.vwin.InvTransform[3],1.2, -900,-450+math.sin(1.2)*160*.5)
        TRANSFORM(self.vwin.InvTransform[4],1.2, -200,-450+math.sin(-1.2)*160*.5)
        TRANSFORM(self.vwin.InvTransform[0],0, 0,0)                                 ##Identity matrix until I can figure out how the other transforms should work
        windll.gdi32.SetGraphicsMode(self.vwin.hdcCompat_card[0],GM_ADVANCED)
        windll.gdi32.SetGraphicsMode(self.vwin.hdc,GM_ADVANCED)
        ##INITIALIZE PLAYERS
        for i in range(len(self.vwin.All_Players)):
            self.vwin.All_Players[i].Team=i
            self.vwin.All_Players[i].Num_armies=80
        ##CREATE REGIONS FOR EACH COUNTRY, CREATE THE DECK, AND INITIALIZE TOKEN POINTS##
        self.vwin.SelectedRgn=0
        CreatePolygonRgn=windll.gdi32.CreatePolygonRgn
        for i in range(42):
            Points=REGION(i+1)
            Points_place=COUNTRY_POINTS(i+1)
            ##INITIALIZE DECK##
            self.vwin.Deck[i].Type=i%3+1
            self.vwin.Deck[i].Country=i
            ##ASSIGN TOKENS##
            self.vwin.Countries[i].region=CreatePolygonRgn(Points,len(Points),WINDING)
            self.vwin.Countries[i].Token_point.x=Points_place[0]
            self.vwin.Countries[i].Token_point.y=Points_place[1]
            ##RANDOMIZE COUNTRIES##
            player=int(random.random()+.5)
            while self.vwin.All_Players[player].Num_countries>42/len(self.vwin.All_Players):
                player=int(random.random()+.5)
            self.vwin.Countries[i].Team=player
            self.vwin.All_Players[player].Num_countries=self.vwin.All_Players[player].Num_countries+1
            ##ADD ARMIES##
            army=int(random.random()*5+.5)+1
            temp=(self.vwin.All_Players[player].Num_armies-army)/42*len(self.vwin.All_Players)
            if temp<1:
                army=1
##            if army>(self.vwin.All_Players[player].Num_armies/42*len(self.vwin.All_Players)):
##                army=int(self.vwin.All_Players[player].Num_armies/42*len(self.vwin.All_Players))
            self.vwin.Countries[i].Num_armies=army
            self.vwin.All_Players[player].Num_armies=self.vwin.All_Players[player].Num_armies-army
            
        ##GET TOKEN INFO##
        windll.gdi32.SelectObject(self.vwin.ps.hdc,self.vwin.token_region)
        ##CREATE REGIONS FOR EACH POTENTIAL CARD##
        for i in range(5):
            Points=CARD_REGION(i+1)
            self.vwin.card_region[i]=CreatePolygonRgn(Points,len(Points),WINDING)
        ##ASSIGN PHASE AND PLAYER##
        self.vwin.Phase=0
        self.vwin.Player=0
        self.vwin.Draw_card=0
        self.vwin.Card_bonus=-1
        self.vwin.Card_bonus_amount=4
        self.vwin.place=False
##        for i in range(2):
##            self.vwin.All_Players[0].Cards[i].Type=i%3+1
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
        windll.user32.SetRect(pointer(self.vwin.rcCard),1,1,161,251)
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
        self.vwin.toggle_cards_displayed=False
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
        previous_SelectedRgn=self.vwin.SelectedRgn
        ##PLACE ARMIES PHASE1##
        if self.vwin.Phase==0:
            self.vwin.num_moving=0
            ##GAIN ARMIES##
            if self.vwin.All_Players[self.vwin.Player].Num_armies==-1:
                self.vwin.toggle_Confirm_button=0
                windll.user32.SetRect(pointer(self.vwin.rcCard),1,1,161,251)
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
            ##ALLOW PLAYER TO USE CARDS##
            if self.vwin.Card_bonus==-1 and self.vwin.All_Players[self.vwin.Player].Cards[0].Type!=0:
##                self.vwin.hdc=windll.user32.GetDC(self.hwnd)
                selected_a_card=False
                if self.vwin.toggle_cards_displayed==True:
                    for i in range(5):
                        if windll.gdi32.PtInRegion(self.vwin.card_region[i],self.vwin.pt.x,self.vwin.pt.y) and self.vwin.All_Players[self.vwin.Player].Cards[i].Type!=0:
                            selected=False
                            self.vwin.clear=False
                            selected_a_card=True
                            for j in range(3):
                                if self.vwin.SelectedRgn_CARD[j]==i+1:
                                    selected=True
                            if selected==False:
                                if self.vwin.Selected_cards[0].Type==0:
                                    self.vwin.Selected_cards[0]=self.vwin.All_Players[self.vwin.Player].Cards[i]
                                    self.vwin.SelectedRgn_CARD[0]=i+1
                                    current_card=i
                                elif self.vwin.Selected_cards[1].Type==0:
                                    self.vwin.Selected_cards[1]=self.vwin.All_Players[self.vwin.Player].Cards[i]
                                    self.vwin.SelectedRgn_CARD[1]=i+1
                                    current_card=i
                                elif self.vwin.Selected_cards[2].Type==0:
                                    self.vwin.Selected_cards[2]=self.vwin.All_Players[self.vwin.Player].Cards[i]
                                    self.vwin.SelectedRgn_CARD[2]=i+1
                                else:
                                    for k in range(3):
                                        ##RESTART SELECTOIN IF ADDITIONAL CARD IS SELECTED##
                                        self.vwin.Selected_cards[k]=CARDS()
                                        self.vwin.SelectedRgn_CARD[k]=0
                                    self.vwin.Selected_cards[0]=self.vwin.All_Players[self.vwin.Player].Cards[i]
                                    self.vwin.SelectedRgn_CARD[0]=i+1
                                    self.vwin.toggle_Confirm_button=0
                    if selected_a_card==False and windll.user32.PtInRect(pointer(self.vwin.rcMessage_box),self.vwin.pt)==False:
                        for i in range(3):
                            self.vwin.Selected_cards[i]=CARDS()
                            self.vwin.SelectedRgn_CARD[i]=0
                    elif self.vwin.SelectedRgn_CARD[2]!=0 and self.vwin.toggle_Confirm_button==0:
                        ##CHECK TO SEE IF THERE IS A MATCH##
                        type1=0
                        type2=0
                        type3=0
                        for i in range(3):
                            if self.vwin.Selected_cards[i].Type==1:
                                type1=type1+1
                            elif self.vwin.Selected_cards[i].Type==2:
                                type2=type2+1
                            else:
                                type3=type3+1
                        if max(type1,type2,type3)==1:
                            self.vwin.toggle_Confirm_button=1
                        elif max(type1,type2,type3)==3:
                            self.vwin.toggle_Confirm_button=1
                    elif windll.user32.PtInRect(pointer(self.vwin.rcConfirm_button),self.vwin.pt) and self.vwin.toggle_Confirm_button==1:
                        windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcConfirm_button.left,self.vwin.rcConfirm_button.top,
                                                (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                                                self.vwin.hdcCompat_Confirm_button[1],0,0,
                                                (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                                                SRCCOPY)
                        self.vwin.toggle_Confirm_button=2
                        ##ADD ADDITIONAL ARMIES##
                        self.vwin.Card_bonus=self.vwin.Card_bonus_amount
                        self.vwin.Card_bonus_amount=self.vwin.Card_bonus_amount+4
                        self.vwin.All_Players[self.vwin.Player].Num_armies=self.vwin.All_Players[self.vwin.Player].Num_armies+self.vwin.Card_bonus
                        ##ADD ARMY TO THE FIRST COUNTRY OWNED IN THE SELECTED CARDS##
                        for i in range(3):
                            if self.vwin.Countries[self.vwin.Selected_cards[i].Country].Team==self.vwin.Player:
                                self.vwin.Countries[self.vwin.Selected_cards[i].Country].Num_armies=self.vwin.Countries[self.vwin.Selected_cards[i].Country].Num_armies+2
                                break
                        self.vwin.toggle_Confirm_botton=0
                        self.vwin.clear=True
                        self.vwin.Card_bonus=0
                        ##REMOVE SELECTED CARDS##
                        for i in range(3):
                            for j in range(5):
                                if self.vwin.All_Players[self.vwin.Player].Cards[j].Type==self.vwin.Selected_cards[i].Type and self.vwin.All_Players[self.vwin.Player].Cards[j].Country==self.vwin.Selected_cards[i].Country:
                                    self.vwin.All_Players[self.vwin.Player].Cards[j]=CARDS()
                else:
                    for i in range(3):
                        self.vwin.Selected_cards[i]=CARDS()
                        self.vwin.SelectedRgn_CARD[i]=0
                    self.vwin.toggle_cards_displayed=True
            ##SELECT COUNTRY TO PLACE ARMIES##
            elif windll.user32.PtInRect(pointer(self.vwin.rcMessage_box),self.vwin.pt)==False:
                self.vwin.Card_bonus=0
                self.vwin.toggle_cards_displayed=False
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
            self.vwin.Successful_attack=False
        ##ATTACK PHASE2##
        elif self.vwin.Phase==1:
            self.vwin.Card_bonus=-1
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
                    if (self.vwin.SelectedRgn_ATTACK==0 or (self.vwin.SelectedRgn_ATTACK!=0 and self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player) or (ADJACENT(self.vwin.SelectedRgn_ATTACK,self.vwin.SelectedRgn)==False and self.vwin.SelectedRgn!=0)) and self.vwin.SelectedRgn_DEFEND==0:
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
                        self.vwin.Successful_attack=True
                    ##REINITIALIZE ARMY SELECTOR##
                    self.vwin.num_attacking=0
                    windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        ##FORTIFY: PHASE 3##
        elif self.vwin.Phase==2:
            ##GRANT PLAYER CARD##
            if self.vwin.Successful_attack==True:
                for i in range(5):
                    if self.vwin.All_Players[self.vwin.Player].Cards[i].Type==0:
                        ##ADD CARD##
                        self.vwin.All_Players[self.vwin.Player].Cards[i]=self.vwin.Deck[self.vwin.Draw_card]
                        self.vwin.Draw_card=self.vwin.Draw_card+1
                        self.vwin.Successful_attack=False
                        break
            if self.vwin.SelectedRgn_DEFEND!=0:
                self.vwin.SelectedRgn_SOURCE=self.vwin.SelectedRgn_ATTACK
                self.vwin.SelectedRgn_DESTINATION=self.vwin.SelectedRgn_DEFEND
                self.vwin.SelectedRgn_ATTACK=0
                self.vwin.SelectedRgn_DEFEND=0
            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            ##PICK SOURCE COUNTRY AND PICK DESTINATION COUNTRY##
            previous_SelectedRgn=self.vwin.SelectedRgn
            if windll.user32.PtInRect(pointer(self.vwin.rcMessage_box),self.vwin.pt)==False:
                self.vwin.SelectedRgn=0
                self.vwin.toggle_Confirm_button=0
            ##Determine selected region##
                if self.vwin.num_moving>-1:
                    for i in range(42):
                        if windll.gdi32.PtInRegion(self.vwin.Countries[i].region,self.vwin.pt.x,self.vwin.pt.y):
                            temp=self.vwin.Countries[i].region
                            self.vwin.SelectedRgn=i+1
                            break
                ##Remove previously highlighted region and replace token
                if previous_SelectedRgn!=0 and self.vwin.place==False:
                    ##CLEAR SOURCE SELECTED COUNTRY##
                    ##DETERMINE CONNECTION##
                    connected=True
                    if self.vwin.SelectedRgn_SOURCE!=0 and self.vwin.SelectedRgn!=0:
                        connected=self.VALID_DESTINATION(self.vwin.SelectedRgn_SOURCE,self.vwin.SelectedRgn,self.vwin.Player)
                    if (self.vwin.SelectedRgn_SOURCE==0 or (self.vwin.SelectedRgn_SOURCE!=0 and self.vwin.Countries[self.vwin.SelectedRgn-1].Team!=self.vwin.Player) or connected==False) and self.vwin.SelectedRgn_DESTINATION==0:
                        if self.vwin.SelectedRgn_SOURCE!=0:
                            previous_SelectedRgn=self.vwin.SelectedRgn_SOURCE
                            self.vwin.SelectedRgn_SOURCE=0                                                           
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
                    elif self.vwin.SelectedRgn_DESTINATION!=0:
                        ##CLEAR SOURCE SELECTED COUNTRY##
                        temp2=self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].region
                        windll.gdi32.SelectClipRgn(self.vwin.hdc,temp2)
                        windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
                        player=self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].Team
                        if player>-1:
                            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.Bkgnd_token[player])
                            point=self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].Token_point
                            Points=TOKEN_REGION(point.x,point.y)
                            soldiers=self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].Num_armies
                            windll.gdi32.SelectClipRgn(self.vwin.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                            windll.gdi32.StretchBlt(self.vwin.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                                int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                                0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                            windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                                  point.y+int(self.vwin.bm_token.bmHeight*.05),
                                                  point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
                        ##CLEAR DESTINATION SELECTED COUNTRY##
                        temp2=self.vwin.Countries[self.vwin.SelectedRgn_DESTINATION-1].region
                        windll.gdi32.SelectClipRgn(self.vwin.hdc,temp2)
                        windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
                        player=self.vwin.Countries[self.vwin.SelectedRgn_DESTINATION-1].Team
                        if player>-1:
                            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.Bkgnd_token[player])
                            point=self.vwin.Countries[self.vwin.SelectedRgn_DESTINATION-1].Token_point
                            Points=TOKEN_REGION(point.x,point.y)
                            soldiers=self.vwin.Countries[self.vwin.SelectedRgn_DESTINATION-1].Num_armies
                            windll.gdi32.SelectClipRgn(self.vwin.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                            windll.gdi32.StretchBlt(self.vwin.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                                int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                                0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                            windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                                  point.y+int(self.vwin.bm_token.bmHeight*.05),
                                                  point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
                        self.vwin.SelectedRgn_DESTINATION=0
                        self.vwin.SelectedRgn_SOURCE=0
            
                ##Highlight Regions##
                if temp!=None:
                    windll.gdi32.SelectClipRgn(self.vwin.hdc,temp)
                    windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_gray,0,0,SRCCOPY)
                    windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
                    if self.vwin.SelectedRgn_SOURCE==0 and self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player:
                        self.vwin.SelectedRgn_SOURCE=self.vwin.SelectedRgn
                    elif self.vwin.SelectedRgn_SOURCE!=0 and self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player:
                        self.vwin.SelectedRgn_DESTINATION=self.vwin.SelectedRgn                
            if windll.user32.PtInRect(pointer(self.vwin.rcSelect[1]),self.vwin.pt) and self.vwin.SelectedRgn_DESTINATION!=0:
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
                self.vwin.Countries[self.vwin.SelectedRgn_DESTINATION-1].Num_armies=self.vwin.Countries[self.vwin.SelectedRgn_DESTINATION-1].Num_armies+self.vwin.num_moving
                self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].Num_armies=self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].Num_armies-self.vwin.num_moving
                ##REINITIALIZE ARMY SELECTOR##
                self.vwin.num_moving=-1
                windll.user32.SetRect(pointer(self.vwin.rcSelect[1]),5,590,15,595+20)
            windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)
        ##ADVANCE TO THE NEXT PHASE##
        if (windll.user32.PtInRect(pointer(self.vwin.rcNext_button),self.vwin.pt)):
            self.vwin.hdc=windll.user32.GetDC(self.hwnd)
            windll.gdi32.SelectObject(self.vwin.hdc,None)
            windll.gdi32.SelectClipRgn(self.vwin.hdc,None)
            ##PLACE NEXT BUTTON##
            if self.vwin.All_Players[self.vwin.Player].Num_armies<=0 or self.vwin.Card_bonus==-1:
                windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcNext_button.left,self.vwin.rcNext_button.top,
                                (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                self.vwin.hdcCompat_Next_button[1],0,0,
                                (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                SRCCOPY)
                self.vwin.toggle_Next_button=True
                if self.vwin.Card_bonus==-1 and self.vwin.Phase==0:
                    self.vwin.Card_bonus=0
                    self.vwin.clear=True
##                    print("self.vwin.Card_bonus=",self.vwin.Card_bonus)
                else:
                    self.vwin.All_Players[self.vwin.Player].Num_armies=-1
                if self.vwin.clear==False:
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
                        windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
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
            elif self.vwin.Phase==2 and self.vwin.num_moving>-1:
                num_armies=self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].Num_armies-1
                self.vwin.num_moving=int(num_armies*(center-10)/140+.5)
            
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
            if (self.vwin.Countries[self.vwin.SelectedRgn-1].Team==self.vwin.Player and self.vwin.Phase==0):
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
            elif (self.vwin.SelectedRgn_DESTINATION!=0 and self.vwin.Phase==2):
                info=info+"MOVE "+str(self.vwin.num_moving)+" ARMIES"
                info=info+"\n\n\n\n\n\n\n"+"NUM OF ARMIES LEFT:\n"
                info=info+str(self.vwin.Countries[self.vwin.SelectedRgn_SOURCE-1].Num_armies-self.vwin.num_moving)
                windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcSelect[0]),
                                       windll.gdi32.CreateSolidBrush(RGB(150,0,0)))
                windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot)
                windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcSelect[1].left,self.vwin.rcSelect[1].top,
                                   self.vwin.rcSelect[1].right,self.vwin.rcSelect[1].bottom)
            ##DRAW MESSAGE##
            windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.crBkgnd)
            windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(info),-1,pointer(self.vwin.rcMessage_box),0)
        if (self.vwin.toggle_Confirm_button==1 or self.vwin.toggle_Confirm_button==2) and (self.vwin.SelectedRgn>0 or self.vwin.Card_bonus==-1):
            windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcConfirm_button.left,self.vwin.rcConfirm_button.top,
                                    (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                                    self.vwin.hdcCompat_Confirm_button[0],0,0,
                                    (self.vwin.rcConfirm_button.right-self.vwin.rcConfirm_button.left),(self.vwin.rcConfirm_button.bottom-self.vwin.rcConfirm_button.top),
                                    SRCCOPY)
            self.vwin.toggle_Confirm_bottom=1
                
        if self.vwin.toggle_Next_button==True:
                windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcNext_button.left,self.vwin.rcNext_button.top,
                                        (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                        self.vwin.hdcCompat_Next_button[0],0,0,
                                        (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                        SRCCOPY)
                self.vwin.toggle_Next_button=False
        ##DISPLAY CARDS##
        if self.vwin.Phase==0 and self.vwin.Card_bonus==-1 and self.vwin.toggle_cards_displayed==True:
##            print("clear",self.vwin.clear,self.vwin.Card_bonus)
            for i in range(5):
                Type=self.vwin.All_Players[self.vwin.Player].Cards[i].Type
                if Type!=0:
##                    print("IN DISPLAY")
                    #ROTATE HDC FOR CARD PLACEMENT#
                    windll.gdi32.SetWorldTransform(self.vwin.hdc,pointer(self.vwin.Transform[i]))
                    selected=False
                    for j in range(len(self.vwin.SelectedRgn_CARD)):
                        if self.vwin.SelectedRgn_CARD[j]==i+1:
                            selected=True
                    if selected==False:
                        windll.gdi32.SelectObject(self.vwin.hdc,windll.gdi32.CreatePen(PS_DOT,2,RGB(0,0,0)))
                        windll.gdi32.SetROP2(self.vwin.hdc, R2_COPYPEN)
                        windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcCard.left-1,self.vwin.rcCard.top-1,
                                               self.vwin.rcCard.right+1,self.vwin.rcCard.bottom+1)
                        windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
                    else:
                        windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot_player[self.vwin.Player])
                        windll.gdi32.SetROP2(self.vwin.hdc, R2_COPYPEN)
                        windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcCard.left-1,self.vwin.rcCard.top-1,
                                               self.vwin.rcCard.right+1,self.vwin.rcCard.bottom+1)
                        windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
                    info="\n\nCountry "+str(self.vwin.All_Players[self.vwin.Player].Cards[i].Country)
                    #COPY CARD#
                    windll.gdi32.StretchBlt(self.vwin.hdc,self.vwin.rcCard.left,self.vwin.rcCard.top,
                                            (self.vwin.rcCard.right-self.vwin.rcCard.left),(self.vwin.rcCard.bottom-self.vwin.rcCard.top),
                                            self.vwin.hdcCompat_card[Type-1],0,0,
                                            (self.vwin.rcCard.right-self.vwin.rcCard.left),(self.vwin.rcCard.bottom-self.vwin.rcCard.top),
                                            SRCCOPY)
                    windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcCard.left,self.vwin.rcCard.top,
                                           self.vwin.rcCard.right,self.vwin.rcCard.bottom)
                    ##DRAW MESSAGE##
                    windll.gdi32.SetBkColor(self.vwin.hdc,RGB(255,255,255))
                    windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(info),-1,pointer(self.vwin.rcCard),1)
                    #ROTATE HDC BACK#
                    windll.gdi32.ModifyWorldTransform(self.vwin.hdc,pointer(self.vwin.InvTransform[i]),MWT_IDENTITY)
        elif self.vwin.clear==True:
        ##CLEAR CARDS##

            windll.gdi32.SelectObject(self.vwin.hdc,None)
            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcBmp.left,self.vwin.rcBmp.top,
                                   self.vwin.rcBmp.right,self.vwin.rcBmp.bottom)
            windll.gdi32.BitBlt(self.vwin.hdc,0,0,self.vwin.bm.bmWidth,self.vwin.bm.bmHeight,self.vwin.hdcCompat_main,0,0,SRCCOPY)
            windll.gdi32.StretchBlt(self.vwin.ps.hdc,self.vwin.rcNext_button.left,self.vwin.rcNext_button.top,
                                    (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                    self.vwin.hdcCompat_Next_button[0],0,0,
                                    (self.vwin.rcNext_button.right-self.vwin.rcNext_button.left),(self.vwin.rcNext_button.bottom-self.vwin.rcNext_button.top),
                                    SRCCOPY)
            windll.gdi32.SelectObject(self.vwin.hdc,windll.gdi32.CreatePen(PS_DOT,2,RGB(0,0,0)))
            windll.gdi32.SetROP2(self.vwin.hdc, R2_COPYPEN)
            windll.gdi32.Rectangle(self.vwin.hdc,self.vwin.rcMessage_box.left-1,self.vwin.rcMessage_box.top-1,
                                   self.vwin.rcMessage_box.right+1,self.vwin.rcMessage_box.bottom+1)
            windll.gdi32.SetROP2(self.vwin.hdc, R2_NOTXORPEN)
            windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcMessage_box),self.vwin.hbrBkgnd)
            ##CREATE BOARDER##
            windll.gdi32.SelectObject(self.vwin.hdc,self.vwin.hpenDot_player[self.vwin.Player])
            windll.gdi32.Rectangle(self.vwin.hdc,1,1,
                                   self.vwin.rcClient.right-self.vwin.rcClient.left,self.vwin.rcClient.bottom-self.vwin.rcClient.top)
            ##CREATE TOKENS##
            for i in range(42):
                player=self.vwin.Countries[i].Team
                if player>-1:
                    windll.gdi32.SetBkColor(self.vwin.hdc,self.vwin.Bkgnd_token[player])
                    point=self.vwin.Countries[i].Token_point
                    Points=TOKEN_REGION(point.x,point.y)
                    soldiers=self.vwin.Countries[i].Num_armies
                    windll.gdi32.SelectClipRgn(self.vwin.hdc,windll.gdi32.CreatePolygonRgn(Points,len(Points),WINDING))
                    windll.gdi32.StretchBlt(self.vwin.hdc,point.x,point.y,int(self.vwin.bm_token.bmWidth*.5),
                                                        int(self.vwin.bm_token.bmHeight*.5),self.vwin.hdcCompat_token[player],
                                                        0,0,self.vwin.bm_token.bmWidth,self.vwin.bm_token.bmHeight,SRCCOPY)
                    windll.user32.SetRect(pointer(self.vwin.rcTmp),point.x+int(self.vwin.bm_token.bmWidth*0.1),
                                          point.y+int(self.vwin.bm_token.bmHeight*.05),
                                          point.x+self.vwin.bm_token.bmWidth,point.y+self.vwin.bm_token.bmHeight)
                    windll.user32.DrawTextW(self.vwin.hdc,c_wchar_p(str(soldiers)),-1,pointer(self.vwin.rcTmp),0)
            self.vwin.clear=False
            self.vwin.toggle_cards_displayed==False
        windll.user32.ReleaseDC(self.hwnd,self.vwin.hdc)

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

