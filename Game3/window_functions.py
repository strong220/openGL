##THIS FILE CONTAINS ALL THE FUNCTIONS FOR UPDATING THE WINDOW
from ctypes import *
from ctypes.wintypes import *
from Points import *
from math import *

##DEFINE ANY STRUCTURES NEEDED FOR THE FUNCTIONS##
class XFORM(Structure):
    _fields_=[("eM11",c_float),
              ("eM12",c_float),
              ("eM21",c_float),
              ("eM22",c_float),
              ("eDx",c_float),
              ("eDy",c_float)]


##DEFINE ANY FUNCTIONS##
def Draw_step(All_points,All_transforms,All_Regions,All_hdc,x_axis=None):
    #wf.CreatePolygonRgn(,len(Points),WINDING)
    for i in range(1,len(All_points)):
        x=100
        y=100
        x2=0
        y2=0
        for l in range(len(All_points[i])):
            ##Find width
            if All_points[i][l][0]<x:
                x=All_points[i][l][0]
            elif All_points[i][l][0]>x2:
                x2=All_points[i][l][0]
            ##Find height
            if All_points[i][l][1]<y:
                y=All_points[i][l][1]
            elif All_points[i][l][1]>y2:
                y2=All_points[i][l][1]
        ##Transform points##
        points=Transform_points(All_points[i],All_transforms[i][0],All_transforms[i][1],All_transforms[i][2])
        temp=XFORM()
        temp1=XFORM()
        TRANSFORM(temp,All_transforms[i][0],All_transforms[i][1],All_transforms[i][2])
        if x_axis!=None:
            points=Transform_points_x(points,x_axis[i][0],x_axis[i][1],x_axis[i][2])
            TRANSFORM_X(temp1,x_axis[i][0],x_axis[i][1],x_axis[i][2])
        ##Create Regions##
        All_Regions[i]=CreatePolygonRgn(points,len(points),WINDING)
        if i==1:
            All_Regions[0]=CreatePolygonRgn(points,len(points),WINDING)
        else:
            windll.gdi32.CombineRgn(All_Regions[0],All_Regions[0],All_Regions[i],RGN_OR)
        ##Select Region##
        windll.gdi32.SelectClipRgn(All_hdc[0],All_Regions[i])
        ##Transform hdc##
        windll.gdi32.SetWorldTransform(All_hdc[0],pointer(temp))
        if x_axis!=None:
            windll.gdi32.ModifyWorldTransform(All_hdc[0],pointer(temp1),MWT_RIGHTMULTIPLY)
        windll.gdi32.StretchBlt(All_hdc[0],x,y,x2,y2,All_hdc[i],
                        x,y,x2,y2,SRCCOPY)
        windll.gdi32.ModifyWorldTransform(All_hdc[0],pointer(temp),MWT_IDENTITY)
        windll.gdi32.SelectClipRgn(All_hdc[0],None)
    return 0
def REGION(points):
    Rgn=POINT*len(points)
    temp=[]
    for i in range(len(points)):
        temp.append(POINT(points[i][0],points[i][1]))
    out=Rgn(*temp)
    return out

def TRANSFORM(temp,rotate,dx,dy):
    rotate=pi/180*rotate
    temp.eM11=cos(rotate)
    temp.eM12=sin(rotate)
    temp.eM21=-sin(rotate)
    temp.eM22=cos(rotate)
    temp.eDx=dx
    temp.eDy=dy
    return

def TRANSFORM_X(temp,rotate,dx,dy):
    rotate=pi/180*rotate
    temp.eM11=1
    temp.eM12=0
    temp.eM21=0
    temp.eM22=cos(rotate)
    temp.eDx=dx
    temp.eDy=dy
    return

def Transform_points(points,rotation,x,y):
    theta=rotation*pi/180
    Rotation_matrix=[[cos(theta),-sin(theta),x],
                     [sin(theta),cos(theta),y],
                     [0,0,1]]
    points_out=POINT*len(points)
    temp0=[]
    for i in range(len(points)):
        Points=[points[i][0],points[i][1],1]
        temp=[0,0]
        for row in range(2):
            for col in range(3):
                temp[row]=Rotation_matrix[row][col]*Points[col]+temp[row]
        temp0.append(POINT(int(temp[0]),int(temp[1])))
    out=points_out(*temp0)
    return out

def Transform_points_x(points,rotation,x,y):
    theta=rotation*pi/180
    Rotation_matrix=[[1,0,x],
                     [0,cos(theta),y],
                     [0,0,1]]
    points_out=POINT*len(points)
    temp0=[]
    for i in range(len(points)):
        Points=[points[i].x,points[i].y,1]
        temp=[0,0]
        for row in range(2):
            for col in range(3):
                temp[row]=Rotation_matrix[row][col]*Points[col]+temp[row]
        temp0.append(POINT(int(temp[0]),int(temp[1])))
    out=points_out(*temp0)
    return out       

def ShiftRect(rcTemp,x,y):
    rcTemp.left=rcTemp.left+x
    rcTemp.right=rcTemp.right+x
    rcTemp.top=rcTemp.top+y
    rcTemp.bottom=rcTemp.bottom+y
    return 0

def orientation(p,q,r):
    ##function from geeksforgeeks.org
    val=(p.y-q.y)*(r.x-q.x)-(p.x-q.x)*(r.y-q.y)
    if val==0:
        return 0
    elif val>0:
        return 1
    else:
        return 2

def check_intersection(R1,R2,P1,P2):
    orientation1=orientation(R1,R2,P1)
    orientation2=orientation(R1,R2,P2)
##    if orientation1==0 or orientation2==0:
##        return False
    if orientation1!=orientation2:
        orientation3=orientation(P1,P2,R1)
        orientation4=orientation(P1,P2,R2)
        if orientation3!=orientation4:
##            if orientation3==0 or orientation4==0:
##                return False
##            else:
            return True
        else:
            return False
    else:
        return False

def check_intersection2(L1a,L1b,L2a,L2b,Ca,Cb):
    ##L1 is above L2 and Ca is above Cb##
    ##or L1 is left of L2 and Ca is left of Cb##
    orientation1=orientation(L1a,L1b,Cb)
    orientation2=orientation(L2a,L2b,Ca)
    if orientation1!=orientation2:# and orientation1!=0 and orientation2!=0:
        orientation3=orientation(Ca,Cb,L1a)
        orientation4=orientation(Ca,Cb,L1b)
        if orientation3!=orientation4:# and orientation3!=0 and orientation!=4:
            return True
    return False

def ARRAY_CREATE(h,w):
    #initialize
    matrix=[[]]
    for i in range(h):
        if i!=0:
            matrix.append([[]])
        for j in range(w):
            matrix[i].append([])
    return matrix

def REGION(reg):
    points=Character_Regions(reg)
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
def MATMULT(vector,matrix):
    col=len(vector)
    rows=len(matrix)
    result=None
    for i in range(rows):
        if i==0:
            result=[[0]]
        else:
            result.append([0])
        temp=0
        for j in range(col):
            temp=vector[j][0]*matrix[i][j]+temp
        result[i][0]=temp
    return result
            

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
R2_BLACK = 0x0001
R2_NOTMERGEPEN = 0x0002
R2_MASKNOTPEN = 0x0003
R2_NOTCOPYPEN = 0x0004
R2_MASKPENNOT = 0x0005
R2_NOT = 0x0006
R2_NOTMASKPEN = 0x0008
R2_MASKPEN = 0x0009
R2_NOTXORPEN = 0x000A
R2_NOP = 0x000B
R2_MERGENOTPEN = 0x000C
R2_MERGEPENNOT = 0x000E
R2_MERGEPEN = 0x000F
R2_WHITE = 0x0010
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
RGN_OR=0x02
##PICTURE CONSTANTS##
character_width=175
character_height=440
backgrnd_window_w=1000
backgrnd_window_h=1000
main_window_w=800
main_window_h=800
map_w=10000
map_h=10000
tile_w=200
tile_h=200
tree1_w=140
tree1_h=350
wall_vertical_w=50
wall_vertical_h=300
wall_horizontal_w=200
wall_horizontal_h=105
wall_w=[wall_vertical_w,wall_horizontal_w]
wall_h=[wall_vertical_h,wall_horizontal_h]
button_w=31
button_h=31
stats_block_w=200
stats_block_h=800
token_h=50
token_w=50
shiftx=int(main_window_w/2-character_width/2)
shifty=int(main_window_h/2-character_height/2)
r_build,l_build,u_build,d_build=[POINT(),POINT(),POINT(),POINT()]
r_build.x=0
r_build.y=int(tile_h/2)
l_build.x=tile_w-button_w
l_build.y=int(tile_h/2)
u_build.x=int(tile_w/2)
u_build.y=tile_h-button_h
d_build.x=int(tile_h/2)
d_build.y=0
##KEYBOARD KEYS
S_KEY=83
S_KEY_DOWN=115
A_KEY=65
A_KEY_DOWN=97
D_KEY=68
D_KEY_DOWN=100
W_KEY=87
W_KEY_DOWN=119
E_KEY=0x45
E_KEY_DOWN=101
Q_KEY=81
Q_KEY_DOWN=113
NUM4_KEY=100
NUM4_KEY_DOWN=52
NUM8_KEY=104
NUM8_KEY_DOWN=56
NUM6_KEY=102
NUM6_KEY_DOWN=54
NUM5_KEY=101
NUM5_KEY_DOWN=53
NUM9_KEY=105
NUM9_KEY_DOWN=57
NUM7_KEY=103
NUM7_KEY_DOWN=55
##TOOL SELECTION
Axe=0
Empty_Hand=1

LoadImage=windll.user32.LoadImageW
LoadImage.restype=HBITMAP
LoadImage.argtypes = [HINSTANCE, LPCWSTR, UINT, c_int, c_int, UINT]
CreatePolygonRgn=windll.gdi32.CreatePolygonRgn

