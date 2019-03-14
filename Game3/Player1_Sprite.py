##THIS CLASS CONTAINS INFORMATION FOR PLAYER 1 CHARACTER##
import window_functions as wf
import window_structures as ws
import math
from ctypes import *
from ctypes.wintypes import *
def Draw_step(All_points,All_transforms,All_Regions,All_hdc):
    #wf.CreatePolygonRgn(,len(Points),wf.WINDING)
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
        points=wf.Transform_points(All_points[i],All_transforms[i][0],All_transforms[i][1],All_transforms[i][2])
        temp=ws.XFORM()
        TRANSFORM(temp,All_transforms[i][0],All_transforms[i][1],All_transforms[i][2])
        ##Create Regions##
        All_Regions[i]=wf.CreatePolygonRgn(points,len(points),wf.WINDING)
        if i==1:
            All_Regions[0]=wf.CreatePolygonRgn(points,len(points),wf.WINDING)
        else:
            windll.gdi32.CombineRgn(All_Regions[0],All_Regions[0],All_Regions[i],wf.RGN_OR)
        ##Select Region##
        windll.gdi32.SelectClipRgn(All_hdc[0],All_Regions[i])
        ##Transform hdc##
        windll.gdi32.SetWorldTransform(All_hdc[0],pointer(temp))
        windll.gdi32.StretchBlt(All_hdc[0],x,y,x2,y2,All_hdc[i],
                        x,y,x2,y2,wf.SRCCOPY)
        windll.gdi32.ModifyWorldTransform(All_hdc[0],pointer(temp),wf.MWT_IDENTITY)
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
    rotate=math.pi/180*rotate
    temp.eM11=math.cos(rotate)
    temp.eM12=math.sin(rotate)
    temp.eM21=-math.sin(rotate)
    temp.eM22=math.cos(rotate)
    temp.eDx=dx
    temp.eDy=dy
    return

class Player1_Sprite:
    def __init__(self,hdc_main,file_path_main):
        windll.gdi32.SetGraphicsMode(hdc_main,wf.GM_ADVANCED)
        ##Initialize hdcs and load images##
        character1_down_file="Face_forward_1a.bmp"
        character1_up_file="Face_backward_1a.bmp"
        character1_right_file="Face_right_1a.bmp"
        Head1_right_file="Head_right_1a.bmp"#"Face_right_1a.bmp"
        Neck1_right_file="Neck_right_1a.bmp"
        Body1_right_file="Body_right_1a.bmp"
        Forearm1_right_file="Forearm_right_1a.bmp"
        Bicep1_right_file="Bicep_right_1a.bmp"
        Belt1_right_file="Belt_right_1a.bmp"
        Belt2_right_file="Belt_right_1b.bmp"
        Belt3_right_file="Belt_right_1c.bmp"
        Thigh1_right_file="Thigh_right_1a.bmp"
        Shin1_right_file="Shin_right_1a.bmp"
        Skirt1_right_file="Skirt_right_1a.bmp"
        Skirt2_right_file="Skirt_right_1b.bmp"
        Skirt3_right_file="Skirt_right_1c.bmp"
        Forearm2_right_file="Forearm_right_1b.bmp"
        Head2_right_file="Head_right_1b.bmp"#"Face_right_1a.bmp"
        character1_left_file="Face_left_1a.bmp"
        ##Define dictionaries for the character##
        self.dict_character_to_index={0:"character1_down",1:"character1_up",2:"character1_right",3:"character1_left",
                                      0:"character2_down",1:"character2_up",4:"character2_right",3:"character2_left",
                                      0:"character3_down",1:"character3_up",5:"character3_right",3:"character3_left",
                                      0:"character4_down",1:"character4_up",6:"character4_right",3:"character4_left"}
        self.dict_index_to_character={"character1_down":0,"character1_up":1,"character1_right":2,"character1_left":3,
                                      "character2_down":0,"character2_up":1,"character2_right":4,"character2_left":3,
                                      "character3_down":0,"character3_up":1,"character3_right":5,"character3_left":3,
                                      "character4_down":0,"character4_up":1,"character4_right":6,"character4_left":3}
        self.character_files=[[character1_down_file,character1_down_file,character1_down_file,character1_down_file,character1_down_file],
                              [character1_up_file,character1_up_file,character1_up_file,character1_up_file,character1_up_file],
                              [character1_right_file,Neck1_right_file,Head1_right_file,Body1_right_file,Shin1_right_file,Thigh1_right_file,Skirt1_right_file,Belt1_right_file,Bicep1_right_file,Forearm1_right_file],
                              [character1_left_file,character1_left_file,character1_left_file,character1_left_file,character1_left_file],
                              [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt3_right_file,Belt3_right_file,Bicep1_right_file,Forearm1_right_file],
                              [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt1_right_file,Belt1_right_file,Bicep1_right_file,Forearm1_right_file],
                              [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt2_right_file,Belt2_right_file,Bicep1_right_file,Forearm1_right_file]]
        self.character_hbmp=[[None,None,None,None,None],
                             [None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        self.character_hdc=[[None,None,None,None,None],
                            [None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        self.character_region=[[None,None,None,None,None],
                             [None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        for i in range(7):
            for j in range(14):
                if j<5 or i>=4 or (i==2 and j<10):
                    self.character_hbmp[i][j]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+self.character_files[i][j]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
                    ##Create HDC##
                    self.character_hdc[i][j]=windll.gdi32.CreateCompatibleDC(hdc_main)                  #Make hdc similar to the reference hdc
                    windll.gdi32.SetGraphicsMode(self.character_hdc[i][j],wf.GM_ADVANCED)
                    windll.gdi32.SelectObject(self.character_hdc[i][j],self.character_hbmp[i][j])       #Copy image into hdc

        ##LOAD REGIONS##
        Points=wf.REGION(1)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        ##Character1_down##
        self.character_region[0][0]=temp
        for i in range(2,9):
            Points=wf.REGION(i)
            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
            windll.gdi32.CombineRgn(self.character_region[0][0],self.character_region[0][0],temp,wf.RGN_OR)
        self.character_region[0][1]=self.character_region[0][0]
        Points=wf.REGION(19)
        ##Character1_up##
        self.character_region[1][0]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        for i in range(20,27):
            Points=wf.REGION(i)
            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
            windll.gdi32.CombineRgn(self.character_region[1][0],self.character_region[1][0],temp,wf.RGN_OR)
        self.character_region[1][1]=self.character_region[1][0]
        ##Character1_right##
        ##DEFINE INITIAL POINTS##
        Head_right_points=[(40,0),(42,3),(45,3),(47,4),(50,6),(51,6),(54,8),(54,11),(55,11),(57,13),(58,14),(58,18),(61,18),(63,20),(61,25),(61,27),(65,34),(65,36),(66,36),(67,37),(67,38),(66,39),(66,43),(67,44),(71,51),(71,52),(73,54),(76,62),(76,64),(71,65),(69,66),(66,84),(63,90),(61,96),(58,98),(58,99),(50,107),(40,110),(39,110),(30,108),(29,107),(21,99),(21,98),(18,96),(16,89),(14,85),(12,78),(10,65),(7,58),(5,56),(5,54),(2,49),(1,45),(3,42),(0,37),(0,33),(1,31),(1,27),(2,24),(4,20),(6,17),(9,11),(12,10),(15,7),(18,5),(23,3),(28,4),(32,1),(34,0)]
        Neck_right_points=[(0,6),(2,4),(2,3),(3,2),(9,0),(10,0),(16,2),(16,3),(19,7),(19,24),(18,26),(14,30),(10,31),(5,30),(1,26),(0,23)]
        Body_right_points=[(20,1),(47,0),(59,9),(63,14),(67,25),(64,70),(60,132),(57,136),(56,138),(52,142),(48,144),(44,146),(34,148),(24,146),(19,144),(13,138),(11,133),(9,125),(3,70),(0,39),(0,33),(1,23),(3,17),(5,14),(7,11),(13,5),(16,4),(18,2)]
        Bicep_right_points=[(1,39),(2,24),(3,11),(5,6),(7,5),(7,4),(9,1),(12,0),(22,0),(24,2),(26,3),(27,6),(29,9),(29,38),(26,39),(26,46),(25,47),(24,54),(23,59),(22,68),(20,72),(17,75),(13,76),(11,76),(7,75),(4,72),(4,39)]
        Forearm_right_points=[(14,0),(19,0),(21,1),(24,4),(26,11),(26,19),(27,37),(28,42),(28,49),(30,51),(33,59),(33,73),(28,75),(20,77),(18,74),(18,71),(14,63),(14,59),(17,52),(13,44),(12,41),(10,35),(8,29),(7,24),(7,11),(9,4),(12,1)]
        Belt_right_points=[(1,0),(12,0),(13,1),(29,1),(30,2),(51,2),(52,11),(53,23),(48,23),(47,24),(37,24),(36,25),(17,25),(16,26),(2,26),(1,25),(0,21),(0,1)]
        Thigh_right_points=[(27,0),(28,7),(29,19),(30,35),(30,50),(29,71),(27,94),(25,98),(23,100),(19,101),(11,101),(9,99),(8,99),(7,98),(5,92),(3,86),(2,78),(1,71),(0,62),(0,32),(1,19),(2,11),(3,4),(4,0)]
        Shin_right_points=[(10,0),(15,0),(18,1),(22,5),(23,9),(24,21),(24,34),(23,71),(23,75),(19,79),(16,80),(14,80),(10,79),(6,76),(5,71),(3,60),(1,44),(0,37),(1,23),(3,10),(4,5),(8,1),(9,1)]
        Skirt_right_points=[(18,0),(69,0),(87,89),(87,92),(85,97),(84,99),(78,101),(72,101),(68,97),(65,101),(64,102),(59,104),(57,104),(52,102),(50,98),(47,104),(45,105),(43,107),(40,107),(36,106),(34,104),(32,100),(30,104),(29,105),(26,107),(21,107),(19,105),(18,105),(17,104),(16,101),(14,103),(14,104),(12,106),(9,107),(8,107),(4,106),(2,104),(1,101),(0,97),(0,95),(14,16)]
        Skirt2_right_points=[(23,0),(74,0),(99,82),(99,86),(97,93),(95,95),(94,96),(92,93),(92,89),(92,92),(90,97),(89,99),(83,101),(77,101),(73,97),(70,101),(69,102),(64,104),(62,104),(57,102),(55,98),(52,104),(50,105),(48,107),(45,107),(41,106),(39,104),(37,100),(35,104),(34,105),(31,107),(26,107),(24,105),(23,105),(22,104),(21,101),(19,103),(19,104),(17,106),(14,107),(13,107),(9,106),(7,104),(6,101),(5,97),(2,96),(0,93),(0,88)]
        out=[None,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Thigh_right_points,Skirt_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points]
        transforms=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-10),100],   ##Neck
                    [0,int(wf.character_width/2-77/2),0],   ##Head
                    [0,int(wf.character_width/2-34),115],   ##Body
                    [0,int(wf.character_width/2-12),345],   #Shin
                    [0,int(wf.character_width/2-15),255],   ##Thigh
                    [0,int(wf.character_width/2-41),262],   #Skirt
                    [0,int(wf.character_width/2-24),245],   ##Belt
                    [0,int(wf.character_width/2-15),115],
                    [0,int(wf.character_width/2-20),180]]
        ##Draw Character##
        Draw_step(out,transforms,self.character_region[2],self.character_hdc[2])
        out2=[None,Bicep_right_points,Forearm_right_points,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Shin_right_points,Thigh_right_points,Thigh_right_points,Skirt2_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points]
        transforms2=[[0,0,0],                                   ##Canvas
                     [30,int(wf.character_width/2-15),110],     ##Bicep_right
                     [10,int(30),170],                          ##Forearm
                     [0,int(wf.character_width/2-10),100],      ##Neck
                     [0,int(wf.character_width/2-77/2),0],      ##Head
                     [0,int(wf.character_width/2-34),115],      ##Body
                     [-5,int(wf.character_width/2+30),338],     #Shin1
                     [20,int(wf.character_width/2-38),332],     #Shin2
                     [-25,int(wf.character_width/2-13),263],    ##Thigh1
                     [18,int(wf.character_width/2-13),250],     ##Thigh2
                     [0,int(wf.character_width/2-46),262],      ##Skirt
                     [0,int(wf.character_width/2-24),245],      ##Belt
                     [-25,int(wf.character_width/2-15),125],
                     [-35,int(wf.character_width/2+10),190]]
        ##Draw_Character        
        Draw_step(out2,transforms2,self.character_region[4],self.character_hdc[4])
        out3=[None,Bicep_right_points,Forearm_right_points,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Shin_right_points,Thigh_right_points,Thigh_right_points,Skirt_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points]
        transforms3=[[0,0,0],                               ##Canvas
                     [0,int(wf.character_width/2-20),180],  ##Bicep right
                     [0,int(wf.character_width/2-15),115],  ##Forearm
                     [0,int(wf.character_width/2-10),100],  ##Neck
                     [0,int(wf.character_width/2-77/2),0],  ##Head
                     [0,int(wf.character_width/2-34),115],  ##Body
                     [0,int(wf.character_width/2-12),345],  #Shin1
                     [0,int(wf.character_width/2-12),345],  #Shin2
                     [0,int(wf.character_width/2-15),255],  ##Thigh1
                     [0,int(wf.character_width/2-15),255],  ##Thigh2
                     [0,int(wf.character_width/2-41),262],  ##Skirt
                     [0,int(wf.character_width/2-24),245],  ##Belt
                     [0,int(wf.character_width/2-15),115],
                     [0,int(wf.character_width/2-20),180]]
        ##Draw_Character
        Draw_step(out3,transforms3,self.character_region[5],self.character_hdc[5])
        transforms4=[[0,0,0],                                   ##Canvas
                     [-25,int(wf.character_width/2-15),125],    ##Bicep right
                     [-35,int(wf.character_width/2+10),190],    ##Forearm
                     [0,int(wf.character_width/2-10),100],      ##Neck
                     [0,int(wf.character_width/2-77/2),0],      ##Head
                     [0,int(wf.character_width/2-34),115],      ##Body
                     [20,int(wf.character_width/2-38),332],     #Shin1
                     [-5,int(wf.character_width/2+30),338],     #Shin2
                     [18,int(wf.character_width/2-13),250],     ##Thigh1
                     [-25,int(wf.character_width/2-13),263],    ##Thigh2
                     [0,int(wf.character_width/2-46),262],      ##Skirt
                     [0,int(wf.character_width/2-24),245],      ##Belt
                     [30,int(wf.character_width/2-15),110],
                     [10,int(30),170]]
        ##Draw_Character
        Draw_step(out2,transforms4,self.character_region[6],self.character_hdc[6])
        Points=wf.REGION(14)
        ##Character1_left##
        self.character_region[3][0]= wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        for i in range(15,19):
            Points=wf.REGION(i)
            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
            windll.gdi32.CombineRgn(self.character_region[3][0],self.character_region[3][0],temp,wf.RGN_OR)
        self.character_region[3][1]=self.character_region[3][0]

        ##DEFINE THE TARGET BOX##
        self.tboxUL=POINT(0,wf.character_height-100)
        self.tboxUR=POINT(wf.character_width,wf.character_height-100)
        self.tboxLL=POINT(0,wf.character_height)
        self.tboxLR=POINT(wf.character_width,wf.character_height)
        
        ##DEFINE REFERNCE POSITIONS##
        self.position=POINT(wf.shiftx+100,wf.shifty+100)
        self.tile_position=POINT(int(100/wf.tile_w),int(100/wf.tile_h))
        self.direction="down"
        self.step=0
        
    def Reference_Tile(self):
        #Reference Tile#
        return self.tile_position

    def Update_direction(self,new_direction):
        if self.direction!=new_direction:
            self.step=0
            self.direction=new_direction
        return 0

    def Animate_step(self,move):
        if move==True:
            self.step=(self.step+.11)%4
        else:
            self.step=0
        return

    def Update_Position(self,shiftx,shifty):
        self.position=POINT(shiftx,shifty)
        self.tile_position=POINT(int(shiftx/wf.tile_w),int(shifty/wf.tile_h))
        return 0

    def Target_Box_Shifted(self,shiftx,shifty):
        shifted_tboxUL=POINT(self.tboxUL.x+shiftx,self.tboxUL.y+shifty)
        shifted_tboxUR=POINT(self.tboxUR.x+shiftx,self.tboxUR.y+shifty)
        shifted_tboxLL=POINT(self.tboxLL.x+shiftx,self.tboxLL.y+shifty)
        shifted_tboxLR=POINT(self.tboxLR.x+shiftx,self.tboxLR.y+shifty)
        return [shifted_tboxUL,shifted_tboxUR,shifted_tboxLL,shifted_tboxLR]
    
    def Target_Box(self):
        shiftx=self.position.x
        shifty=self.position.y
        shifted_tboxUL=POINT(self.tboxUL.x+shiftx,self.tboxUL.y+shifty)
        shifted_tboxUR=POINT(self.tboxUR.x+shiftx,self.tboxUR.y+shifty)
        shifted_tboxLL=POINT(self.tboxLL.x+shiftx,self.tboxLL.y+shifty)
        shifted_tboxLR=POINT(self.tboxLR.x+shiftx,self.tboxLR.y+shifty)
        return [shifted_tboxUL,shifted_tboxUR,shifted_tboxLL,shifted_tboxLR]

    def Draw_Character(self,hdc,reference_tile):
        ##Shift the reference position to the desired tile##
        position_new=POINT(self.position.x-reference_tile.x*wf.tile_w,
                           self.position.y-reference_tile.y*wf.tile_h)
        ##Copy Object onto tile
##        self.step=1
        for j in range(1):
            i=self.dict_index_to_character["character"+str(int(self.step)+1)+"_"+self.direction]        ##Find the desired image
            windll.gdi32.OffsetRgn(self.character_region[i][j],                                         ##Shift the region to draw the character
                                   position_new)
            windll.gdi32.SelectClipRgn(hdc,self.character_region[i][j])                                 ##Select the shifted region for copying the image
            windll.gdi32.BitBlt(hdc,position_new,wf.character_width,                                    ##Add Character to Background
                                wf.character_height,self.character_hdc[i][j],
                                0,0,wf.SRCCOPY)
            ##Reset class object and hdc##
            windll.gdi32.SelectClipRgn(hdc,None)                                                        ##Remove clipping region
            windll.gdi32.OffsetRgn(self.character_region[i][j],-position_new.x,                         #Return Region to original positoin
                                    -position_new.y)
