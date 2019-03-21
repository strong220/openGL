##THIS CLASS CONTAINS INFORMATION FOR PLAYER 1 CHARACTER##
import window_functions as wf
import window_structures as ws
import math
from ctypes import *
from ctypes.wintypes import *
def Draw_step(All_points,All_transforms,All_Regions,All_hdc,x_axis=None):
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
        temp1=ws.XFORM()
        TRANSFORM(temp,All_transforms[i][0],All_transforms[i][1],All_transforms[i][2])
        if x_axis!=None:
            points=wf.Transform_points_x(points,x_axis[i][0],x_axis[i][1],x_axis[i][2])
            TRANSFORM_X(temp1,x_axis[i][0],x_axis[i][1],x_axis[i][2])
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
        if x_axis!=None:
            windll.gdi32.ModifyWorldTransform(All_hdc[0],pointer(temp1),wf.MWT_RIGHTMULTIPLY)
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

def TRANSFORM_X(temp,rotate,dx,dy):
    rotate=math.pi/180*rotate
    temp.eM11=1
    temp.eM12=0
    temp.eM21=0
    temp.eM22=math.cos(rotate)
    temp.eDx=dx
    temp.eDy=dy
    return

class Player1_Sprite:
    def __init__(self,hdc_main,file_path_main,hwnd):
        windll.gdi32.SetGraphicsMode(hdc_main,wf.GM_ADVANCED)
        ##Initialize hdcs and load images##
        [character1_down_file,Head1_forward_file,Neck1_forward_file,Body1_forward_file,
        Forearm1_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,
         Head2_forward_file,Belt1_forward_file,Skirt1_forward_file,Skirt1_backward_file,
         Shin1_forward_file,Shoe1_forward_file,Shoe2_forward_file,Shoe3_forward_file,
         Belt2_forward_file,Belt3_forward_file,Forearm3_forward_file,Forearm4_forward_file]=["Face_forward_1a.bmp","Head_forward_1a.bmp","Neck_forward_1a.bmp","Body_forward_1a.bmp",
                              "Forearm_forward_1a.bmp","Forearm_forward_1b.bmp","Bicep_forward_left_1a.bmp","Bicep_forward_right_1a.bmp",
                              "Head_forward_1b.bmp","Belt_forward_1b.bmp","Skirt_forward_1a.bmp","Skirt_backward_1a.bmp",
                              "Shin_forward_1a.bmp","Shoe_forward_1a.bmp","Shoe_forward_1b.bmp","Shoe_forward_1c.bmp",
                              "Belt_forward_1c.bmp","Belt_forward_1d.bmp","Forearm_forward_1c.bmp","Forearm_forward_1d.bmp"]
        [character1_up_file,Head1_backward_file,Neck1_backward_file,Body1_backward_file,
        Bicep1_backward_file,Bicep2_backward_file,Forearm1_backward_file,Forearm2_backward_file,
         Belt1_backward_file,Skirt1_backward_file,Shin1_backward_file,Shoe1_backward_file,
         Forearm3_backward_file]=["Face_backward_1a.bmp","Head_backward_1a.bmp","Neck_forward_1a.bmp","Body_backward_1a.bmp",
                               "Bicep_forward_left_1a.bmp","Bicep_forward_right_1a.bmp","Forearm_backward_1a.bmp","Forearm_backward_1b.bmp",
                               "Belt_backward_1a.bmp","Skirt_backward_1b.bmp","Shin_forward_1a.bmp","Shoe_backward_1a.bmp",
                                  "Forearm_backward_1c.bmp"]
        [character1_right_file,Head1_right_file,Neck1_right_file,Body1_right_file,
         Forearm1_right_file,Bicep1_right_file,Belt1_right_file,Belt2_right_file,
         Belt3_right_file,Thigh1_right_file,Shin1_right_file,Skirt1_right_file,
         Shoe1_right_file,Skirt2_right_file,Skirt3_right_file,Forearm2_right_file,
         Head2_right_file]=["Face_right_1a.bmp","Head_right_1a.bmp","Neck_right_1a.bmp","Body_right_1a.bmp",
                            "Forearm_right_1a.bmp","Bicep_right_1a.bmp","Belt_right_1a.bmp","Belt_right_1b.bmp",
                            "Belt_right_1c.bmp","Thigh_right_1a.bmp","Shin_right_1a.bmp","Skirt_right_1a.bmp",
                            "Shoe_right_1a.bmp","Skirt_right_1b.bmp","Skirt_right_1c.bmp","Forearm_right_1b.bmp","Head_right_1b.bmp"]
        [character1_left_file,Head1_left_file,Neck1_left_file,Body1_left_file,
         Forearm1_left_file,Bicep1_left_file,Belt1_left_file,Belt2_left_file,
         Belt3_left_file,Thigh1_left_file,Shin1_left_file,Skirt1_left_file,
         Shoe1_left_file,Skirt2_left_file,Skirt3_left_file,Forearm2_left_file,
         Head2_left_file]=["Face_left_1a.bmp","Head_left_1a.bmp","Neck_left_1a.bmp","Body_left_1a.bmp",
                           "Forearm_left_1a.bmp","Bicep_left_1a.bmp","Belt_left_1a.bmp","Belt_left_1b.bmp",
                           "Belt_left_1c.bmp","Thigh_left_1a.bmp","Shin_left_1a.bmp","Skirt_left_1a.bmp",
                           "Shoe_left_1a.bmp","Skirt_left_1b.bmp","Skirt_left_1c.bmp","Forearm_left_1b.bmp","Head_left_1b.bmp"]
        ##Define dictionaries for the character##
        self.dict_character_to_index={0:"character1_down",1:"character1_up",2:"character1_right",3:"character1_left",
                                      4:"character2_down",7:"character2_up",10:"character2_right",13:"character2_left",
                                      5:"character3_down",8:"character3_up",11:"character3_right",14:"character3_left",
                                      6:"character4_down",9:"character4_up",12:"character4_right",15:"character4_left"}
        self.dict_index_to_character={"character1_down":0,"character1_up":1,"character1_right":2,"character1_left":3,
                                      "character2_down":4,"character2_up":7,"character2_right":10,"character2_left":13,
                                      "character3_down":5,"character3_up":8,"character3_right":11,"character3_left":14,
                                      "character4_down":6,"character4_up":9,"character4_right":12,"character4_left":15}
        self.character_files=[[character1_down_file,Neck1_forward_file,Head1_forward_file,Forearm1_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt1_forward_file,Shoe1_forward_file,Shoe1_forward_file],
                              [character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm1_backward_file,Forearm2_backward_file,Body1_backward_file,Bicep1_backward_file,Bicep2_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt1_backward_file,Shoe1_backward_file,Shoe1_backward_file],
                              [character1_right_file,Neck1_right_file,Head1_right_file,Body1_right_file,Shin1_right_file,Thigh1_right_file,Skirt1_right_file,Belt1_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file],
                              [character1_left_file,Neck1_left_file,Head1_left_file,Body1_left_file,Shin1_left_file,Thigh1_left_file,Skirt1_left_file,Belt1_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file],
                              [character1_down_file,Neck1_forward_file,Head2_forward_file,Forearm3_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shoe3_forward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt3_forward_file,Shoe2_forward_file],
                              [character1_down_file,Neck1_forward_file,Head2_forward_file,Forearm1_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt1_forward_file,Shoe1_forward_file,Shoe1_forward_file],
                              [character1_down_file,Neck1_forward_file,Head2_forward_file,Forearm1_forward_file,Forearm4_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shoe3_forward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt2_forward_file,Shoe2_forward_file],
                              [character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm3_backward_file,Forearm2_backward_file,Bicep1_backward_file,Bicep2_backward_file,Body1_backward_file,Shoe1_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt1_backward_file,Shoe1_backward_file],
                              [character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm1_backward_file,Forearm2_backward_file,Bicep1_backward_file,Bicep2_backward_file,Body1_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt1_backward_file,Shoe1_backward_file,Shoe1_backward_file],
                              [character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm1_backward_file,Forearm2_backward_file,Bicep1_backward_file,Bicep2_backward_file,Body1_backward_file,Shoe1_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt1_backward_file,Shoe1_backward_file],
                              [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt3_right_file,Belt3_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file,Shoe1_right_file],
                              [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt1_right_file,Belt1_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file,Shoe1_right_file],
                              [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt2_right_file,Belt2_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file,Shoe1_right_file],
                              [character1_left_file,Bicep1_left_file,Forearm2_left_file,Neck1_left_file,Head2_left_file,Body1_left_file,Shin1_left_file,Shin1_left_file,Thigh1_left_file,Thigh1_left_file,Skirt3_left_file,Belt3_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file,Shoe1_left_file],
                              [character1_left_file,Bicep1_left_file,Forearm2_left_file,Neck1_left_file,Head2_left_file,Body1_left_file,Shin1_left_file,Shin1_left_file,Thigh1_left_file,Thigh1_left_file,Skirt1_left_file,Belt1_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file,Shoe1_left_file],
                              [character1_left_file,Bicep1_left_file,Forearm2_left_file,Neck1_left_file,Head2_left_file,Body1_left_file,Shin1_left_file,Shin1_left_file,Thigh1_left_file,Thigh1_left_file,Skirt2_left_file,Belt2_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file,Shoe1_left_file]]
        self.character_hbmp=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        self.character_hdc=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        self.character_region=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        for i in range(16):
            for j in range(18):
                if len(self.character_hbmp[i])>j:
##                if j<5 or (i>=4 and j<16) or ((i==2 or i==3) and j<11) or (i==0 and j<17):
                    self.character_hbmp[i][j]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+self.character_files[i][j]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
                    ##Create HDC##
                    self.character_hdc[i][j]=windll.gdi32.CreateCompatibleDC(hdc_main)                  #Make hdc similar to the reference hdc
                    windll.gdi32.SetGraphicsMode(self.character_hdc[i][j],wf.GM_ADVANCED)
                    windll.gdi32.SelectObject(self.character_hdc[i][j],self.character_hbmp[i][j])       #Copy image into hdc

        ##LOAD REGIONS##
        ##DEFINE INITIAL POINTS##
        Head_forward_points=[(42,1),(60,1),(61,2),(64,2),(63,7),(66,7),(67,9),(69,9),(70,15),(73,19),(75,21),(76,25),(79,30),(79,35),(82,37),(81,40),(78,43),(79,46),(82,49),(83,51),(83,59),(81,63),(78,65),(78,69),(77,74),(76,77),(74,81),(73,83),(71,88),(68,91),(67,94),(61,100),(59,101),(55,103),(46,106),(38,106),(31,104),(26,102),(23,99),(16,92),(15,90),(14,88),(12,86),(10,82),(9,80),(8,77),(7,72),(6,67),(3,66),(1,64),(0,60),(0,52),(2,49),(3,46),(6,46),(6,45),(4,44),(2,43),(2,41),(3,40),(4,38),(4,35),(3,34),(3,33),(4,32),(3,30),(4,29),(3,28),(3,27),(6,22),(9,22),(9,17),(10,15),(12,13),(16,12),(17,10),(18,10),(19,6),(21,4),(23,3),(26,2),(27,1),(21,1),(35,0)]
        Neck_forward_points=[(17,0),(22,1),(26,5),(27,9),(27,13),(29,22),(30,24),(33,27),(33,29),(32,32),(29,35),(24,37),(17,38),(9,37),(6,36),(4,35),(1,32),(0,29),(0,27),(3,24),(4,21),(5,17),(6,13),(6,8),(7,5),(10,2),(16,0)]
        Bicep_forward_left_points=[(35,0),(34,3),(42,10),(41,11),(45,14),(47,21),(48,26),(48,28),(47,33),(46,37),(44,38),(44,39),(38,45),(37,45),(35,47),(34,47),(31,50),(31,55),(29,55),(26,61),(23,62),(22,68),(21,75),(20,81),(19,82),(19,90),(14,95),(8,95),(4,94),(2,90),(2,84),(2,79),(3,75),(5,63),(6,58),(7,52),(7,50),(6,49),(8,47),(8,31),(10,29),(15,6),(17,4),(27,0)]
        Bicep_forward_right_points=[(13,0),(14,3),(6,10),(7,11),(3,14),(1,21),(0,26),(0,28),(1,33),(2,37),(4,38),(4,39),(10,45),(11,45),(13,47),(14,47),(17,50),(17,55),(19,55),(22,61),(25,62),(26,68),(27,75),(28,81),(29,82),(29,90),(34,95),(40,95),(44,94),(46,90),(46,84),(46,79),(45,75),(43,63),(42,58),(41,52),(41,50),(42,49),(40,47),(40,31),(38,29),(33,6),(31,4),(21,0)]
        Forearm1_forward_points=[(10,0),(14,1),(18,5),(19,8),(18,9),(19,35),(20,45),(25,44),(26,47),(27,51),(28,54),(29,57),(27,58),(13,62),(11,62),(8,61),(4,57),(3,54),(3,49),(1,17),(0,16),(0,11),(3,3),(5,1),(9,0)]
        Forearm2_forward_points=[(19,0),(15,1),(11,5),(10,8),(11,9),(10,35),(9,45),(4,44),(3,47),(2,51),(1,54),(0,57),(2,58),(16,62),(18,62),(21,61),(25,57),(26,54),(26,49),(28,17),(29,16),(29,11),(26,3),(24,1),(20,0)]
        Belt_forward_points=[(0,0),(62,0),(62,21),(48,22),(46,22),(39,21),(32,20),(24,19),(18,19),(10,19),(2,18),(0,16)]
        Skirt1_forward_points=[(25,0),(83,0),(103,97),(103,99),(99,103),(94,104),(87,104),(80,101),(79,102),(74,102),(71,101),(70,100),(69,97),(67,95),(65,97),(62,98),(57,98),(52,97),(49,94),(48,94),(44,98),(41,99),(31,99),(26,97),(24,95),(23,96),(23,97),(22,98),(21,98),(19,100),(16,101),(11,101),(6,100),(5,99),(4,99),(2,97),(0,92),(0,87)]
        Skirt1_backward_points=[(25,0),(83,0),(103,96),(103,98),(102,101),(100,103),(100,105),(92,107),(84,105),(82,103),(80,107),(77,110),(73,110),(71,108),(69,104),(67,106),(66,106),(65,107),(65,109),(64,109),(61,110),(57,110),(54,109),(53,109),(52,106),(49,101),(46,102),(45,103),(44,106),(43,107),(41,109),(38,110),(34,110),(31,109),(27,105),(27,103),(26,102),(25,99),(24,96),(20,105),(13,108),(5,106),(2,103),(0,98),(0,88)]
        Thigh_right_points=[(27,0),(28,7),(29,19),(30,35),(30,50),(29,71),(27,94),(25,98),(23,100),(19,101),(11,101),(9,99),(8,99),(7,98),(5,92),(3,86),(2,78),(1,71),(0,62),(0,32),(1,19),(2,11),(3,4),(4,0)]
        Thigh_left_points=[(3,0),(2,7),(1,19),(0,35),(0,50),(1,71),(3,94),(5,98),(7,100),(11,101),(19,101),(21,99),(22,99),(23,98),(25,92),(27,86),(28,78),(29,71),(30,62),(30,32),(29,19),(28,11),(27,4),(26,0)]
        Shin1_forward_points=[(11,0),(13,0),(16,1),(20,5),(21,8),(22,18),(23,19),(24,40),(23,41),(23,44),(21,60),(20,72),(20,76),(16,79),(13,80),(11,80),(8,79),(4,75),(4,73),(3,60),(1,45),(0,36),(0,32),(1,30),(1,24),(3,7),(4,5),(8,1)]
        Shoe1_forward_points=[(15,0),(21,0),(25,2),(31,8),(34,15),(35,18),(35,22),(37,22),(37,25),(0,25),(1,19),(2,15),(5,8),(10,3)]
        Shoe2_forward_points=[(13,0),(21,0),(26,1),(31,6),(34,13),(35,17),(35,20),(36,20),(36,22),(35,23),(35,24),(32,24),(32,26),(31,26),(31,28),(5,28),(5,26),(4,26),(4,24),(1,24),(1,22),(0,22),(1,16),(2,13),(5,6),(10,1),(12,1)]
        Shoe3a_forward_points=[(12,1),(13,0),(23,0),(24,1),(26,1),(29,4),(34,19),(35,21),(35,25),(36,25),(36,27),(35,27),(30,29),(25,30),(19,31),(17,31),(10,30),(5,30),(0,27),(6,8)]
        Shoe3b_forward_points=[(7,5),(12,1),(13,0),(23,0),(24,1),(26,1),(29,4),(34,19),(35,21),(35,25),(36,25),(36,27),(35,27),(30,29),(25,30),(19,31),(17,31),(10,30),(5,30),(0,27),(6,8)]
        Body_forward_points=[(0,0),(99,0),(99,31),(81,122),(80,123),(78,131),(77,132),(77,133),(75,135),(70,140),(65,142),(55,145),(45,145),(39,143),(34,142),(28,139),(26,137),(25,137),(22,134),(20,131),(18,126),(0,27)]
        ##        maximum=0
##        for i in range(len(Skirt1_backward_points)):
##            if Skirt1_backward_points[i][0]>maximum:
##                maximum=Skirt1_backward_points[i][0]
##        out=""
##        for i in range(len(Skirt1_backward_points)):
##            out=out+"("+str(maximum-Skirt1_backward_points[i][0])+","+str(Skirt1_backward_points[i][1])+"),"
##        print(out)        

        out=[None,Neck_forward_points,Head_forward_points,Forearm1_forward_points,Forearm2_forward_points,Bicep_forward_left_points,Bicep_forward_right_points,Body_forward_points,Skirt1_backward_points,Shin1_forward_points,Shin1_forward_points,Thigh_right_points,Thigh_left_points,Skirt1_forward_points,Belt_forward_points,Shoe1_forward_points,Shoe1_forward_points]
        transforms=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-17),95],    ##Neck
                    [0,int(wf.character_width/2-42),0],     ##Head
                    [-5,int(wf.character_width/2-78+5),200],##Forearm1
                    [5,int(wf.character_width/2+48-5),198], ##Forearm2
                    [0,10+5,120],                           ##Bicep left
                    [0,int(wf.character_width/2+30-5),120], ##Bicep right
                    [0,int(wf.character_width/2-50),120],   ##Body
                    [0,int(wf.character_width/2-55),260],   ##Skirt in the back
                    [0,int(wf.character_width/2-28),352],   ##Shin1
                    [0,int(wf.character_width/2+2),352],    ##Shin2
                    [0,int(wf.character_width/2-33),260],   ##Right thigh
                    [0,int(wf.character_width/2+2),260],    ##Left thigh
                    [0,int(wf.character_width/2-55),260],   ##Skirt in the front
                    [0,int(wf.character_width/2-32),248],   ##Belt
                    [0,int(wf.character_width/2),410],      ##Shoe1
                    [0,50,410]]                             ##Shoe2

        ##Draw Character_DOWN
        Draw_step(out,transforms,self.character_region[0],self.character_hdc[0])#,transforms_x)
        out2=[None,Neck_forward_points,Head_forward_points,Forearm1_forward_points,Forearm2_forward_points,Bicep_forward_left_points,Bicep_forward_right_points,Body_forward_points,Skirt1_backward_points,Shoe3a_forward_points,Shin1_forward_points,Shin1_forward_points,Thigh_right_points,Thigh_left_points,Skirt1_forward_points,Belt_forward_points,Shoe2_forward_points]
        transforms2=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-17),95],    ##Neck
                    [0,int(wf.character_width/2-42),0],     ##Head
                    [5,int(wf.character_width/2-78+18),200],##Forearm1
                    [5,int(wf.character_width/2+48-5),198], ##Forearm2
                    [-7,10+5,120],                           ##Bicep left
                    [0,int(wf.character_width/2+30-5),120], ##Bicep right
                    [0,int(wf.character_width/2-50),120],   ##Body
                    [0,int(wf.character_width/2-55),260],   ##Skirt in the back
                    [0,52,410],                             ##Shoe2
                    [0,int(wf.character_width/2-28),352],   ##Shin1
                    [0,int(wf.character_width/2+2),352],    ##Shin2
                    [0,int(wf.character_width/2-33),260],   ##Right thigh
                    [0,int(wf.character_width/2+2),260],    ##Left thigh
                    [0,int(wf.character_width/2-55),260],   ##Skirt in the front
                    [0,int(wf.character_width/2-32),248],   ##Belt
                    [0,int(wf.character_width/2),410]]      ##Shoe1
        transforms_x=[[0,0,0],                              ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,13],                             ##Forearm1
                      [30,0,18],                            ##Forearm2
                      [40,0,33],                             ##Bicep left
                      [30,0,18],                            ##Bicep right
                      [0,0,0],                              ##Body
                      [0,0,0],                              ##Skirt in the back
                      [0,0,-6],                             ##Shoe2
                      [15,0,-5],                            ##Shin1
                      [15,0,-5],                            ##Shin2
                      [20,0,15],                            ##Right thigh
                      [20,0,15],                            ##Left thigh
                      [0,0,0],                              ##Skirt in the front
                      [0,0,0],                              ##Belt
                      [0,0,-3]]                             ##Shoe1

        ##Draw Character_DOWN
        Draw_step(out2,transforms2,self.character_region[4],self.character_hdc[4],transforms_x)

        ##Draw Character_DOWN
        Draw_step(out,transforms,self.character_region[5],self.character_hdc[5])
        out3=[None,Neck_forward_points,Head_forward_points,Forearm1_forward_points,Forearm2_forward_points,Bicep_forward_left_points,Bicep_forward_right_points,Body_forward_points,Skirt1_backward_points,Shoe3b_forward_points,Shin1_forward_points,Shin1_forward_points,Thigh_right_points,Thigh_left_points,Skirt1_forward_points,Belt_forward_points,Shoe2_forward_points]
        transforms3=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-17),95],    ##Neck
                    [0,int(wf.character_width/2-42),0],     ##Head
                    [-5,int(wf.character_width/2-78+5),200],##Forearm1
                    [-5,int(wf.character_width/2+48-18),198], ##Forearm2
                    [0,10+5,120],                           ##Bicep left
                    [7,int(wf.character_width/2+30-5),120], ##Bicep right
                    [0,int(wf.character_width/2-50),120],   ##Body
                    [0,int(wf.character_width/2-55),260],   ##Skirt in the back
                    [0,int(wf.character_width/2)-4,410],      ##Shoe1
                    [0,int(wf.character_width/2-28),352],   ##Shin1
                    [0,int(wf.character_width/2+2),352],    ##Shin2
                    [0,int(wf.character_width/2-33),260],   ##Right thigh
                    [0,int(wf.character_width/2+2),260],    ##Left thigh
                    [0,int(wf.character_width/2-55),260],   ##Skirt in the front
                    [0,int(wf.character_width/2-32),248],   ##Belt
                    [0,50,410]]                             ##Shoe2
        transforms_x=[[0,0,0],                              ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,18],                             ##Forearm1
                      [30,0,17],                            ##Forearm2
                      [30,0,18],                             ##Bicep left
                      [40,0,28],                            ##Bicep right
                      [0,0,0],                              ##Body
                      [0,0,0],                              ##Skirt in the back
                      [0,0,-6],                             ##Shoe2
                      [15,0,-5],                            ##Shin1
                      [15,0,-5],                            ##Shin2
                      [20,0,15],                            ##Right thigh
                      [20,0,15],                            ##Left thigh
                      [0,0,0],                              ##Skirt in the front
                      [0,0,0],                              ##Belt
                      [0,0,-3]]                             ##Shoe1

        ##Draw Character_DOWN
        Draw_step(out3,transforms3,self.character_region[6],self.character_hdc[6],transforms_x)

        Head_backward_points=[(41,1),(23,1),(22,2),(19,2),(20,7),(17,7),(16,9),(14,9),(13,15),(10,19),(8,21),(7,25),(4,30),(4,35),(1,37),(2,40),(5,43),(4,46),(1,49),(0,51),(0,59),(2,63),(5,65),(5,69),(6,74),(7,77),(9,81),(10,83),(12,88),(15,91),(16,94),(22,100),(24,101),(28,103),(37,106),(45,106),(52,104),(57,102),(60,99),(67,92),(68,90),(69,88),(71,86),(73,82),(74,80),(75,77),(76,72),(77,67),(80,66),(82,64),(83,60),(83,52),(81,49),(80,46),(77,46),(77,45),(79,44),(81,43),(81,41),(80,40),(79,38),(79,35),(80,34),(80,33),(79,32),(80,30),(79,29),(80,28),(80,27),(77,22),(74,22),(74,17),(73,15),(71,13),(67,12),(66,10),(65,10),(64,6),(62,4),(60,3),(57,2),(56,1),(62,1),(48,0)]
        Neck_backward_points=[(17,0),(22,1),(26,5),(27,9),(27,13),(29,22),(30,24),(33,27),(33,29),(32,32),(29,35),(24,37),(17,38),(9,37),(6,36),(4,35),(1,32),(0,29),(0,27),(3,24),(4,21),(5,17),(6,13),(6,8),(7,5),(10,2),(16,0)]
        Bicep_backward_left_points=[(35,0),(34,3),(42,10),(41,11),(45,14),(47,21),(48,26),(48,28),(47,33),(46,37),(44,38),(44,39),(38,45),(37,45),(35,47),(34,47),(31,50),(31,55),(29,55),(26,61),(23,62),(22,68),(21,75),(20,81),(19,82),(19,90),(14,95),(8,95),(4,94),(2,90),(2,84),(2,79),(3,75),(5,63),(6,58),(7,52),(7,50),(6,49),(8,47),(8,31),(10,29),(15,6),(17,4),(27,0)]
        Bicep_backward_right_points=[(13,0),(14,3),(6,10),(7,11),(3,14),(1,21),(0,26),(0,28),(1,33),(2,37),(4,38),(4,39),(10,45),(11,45),(13,47),(14,47),(17,50),(17,55),(19,55),(22,61),(25,62),(26,68),(27,75),(28,81),(29,82),(29,90),(34,95),(40,95),(44,94),(46,90),(46,84),(46,79),(45,75),(43,63),(42,58),(41,52),(41,50),(42,49),(40,47),(40,31),(38,29),(33,6),(31,4),(21,0)]
        Forearm1_backward_points=[(10,0),(14,1),(18,5),(19,8),(18,9),(19,35),(20,45),(25,44),(26,47),(27,51),(28,54),(29,57),(27,58),(13,62),(11,62),(8,61),(4,57),(3,54),(3,49),(1,17),(0,16),(0,11),(3,3),(5,1),(9,0)]
        Forearm2_backward_points=[(19,0),(15,1),(11,5),(10,8),(11,9),(10,35),(9,45),(4,44),(3,47),(2,51),(1,54),(0,57),(2,58),(16,62),(18,62),(21,61),(25,57),(26,54),(26,49),(28,17),(29,16),(29,11),(26,3),(24,1),(20,0)]
        Belt_backward_points=[(62,0),(0,0),(0,21),(14,22),(16,22),(23,21),(30,20),(38,19),(44,19),(52,19),(60,18),(62,16)]
        Skirt2_backward_points=[(78,0),(20,0),(0,96),(0,98),(1,101),(3,103),(3,105),(11,107),(19,105),(21,103),(23,107),(26,110),(30,110),(32,108),(34,104),(36,106),(37,106),(38,107),(38,109),(39,109),(42,110),(46,110),(49,109),(50,109),(51,106),(54,101),(57,102),(58,103),(59,106),(60,107),(62,109),(65,110),(69,110),(72,109),(76,105),(76,103),(77,102),(78,99),(79,96),(83,105),(90,108),(98,106),(101,103),(103,98),(103,88)]
        Thigh_right_points=[(27,0),(28,7),(29,19),(30,35),(30,50),(29,71),(27,94),(25,98),(23,100),(19,101),(11,101),(9,99),(8,99),(7,98),(5,92),(3,86),(2,78),(1,71),(0,62),(0,32),(1,19),(2,11),(3,4),(4,0)]
        Thigh_left_points=[(3,0),(2,7),(1,19),(0,35),(0,50),(1,71),(3,94),(5,98),(7,100),(11,101),(19,101),(21,99),(22,99),(23,98),(25,92),(27,86),(28,78),(29,71),(30,62),(30,32),(29,19),(28,11),(27,4),(26,0)]
        Shin1_backward_points=[(11,0),(13,0),(16,1),(20,5),(21,8),(22,18),(23,19),(24,40),(23,41),(23,44),(21,60),(20,72),(20,76),(16,79),(13,80),(11,80),(8,79),(4,75),(4,73),(3,60),(1,45),(0,36),(0,32),(1,30),(1,24),(3,7),(4,5),(8,1)]
        Shoe1_backward_points=[(16,0),(20,0),(25,2),(31,8),(34,15),(36,22),(36,25),(0,25),(0,22),(1,21),(1,19),(2,15),(5,8),(11,2)]
        Shoe2_forward_points=[(13,0),(21,0),(26,1),(31,6),(34,13),(35,17),(35,20),(36,20),(36,22),(35,23),(35,24),(32,24),(32,26),(31,26),(31,28),(5,28),(5,26),(4,26),(4,24),(1,24),(1,22),(0,22),(1,16),(2,13),(5,6),(10,1),(12,1)]
        Shoe3a_forward_points=[(12,1),(13,0),(23,0),(24,1),(26,1),(29,4),(34,19),(35,21),(35,25),(36,25),(36,27),(35,27),(30,29),(25,30),(19,31),(17,31),(10,30),(5,30),(0,27),(6,8)]
        Shoe3b_forward_points=[(7,5),(12,1),(13,0),(23,0),(24,1),(26,1),(29,4),(34,19),(35,21),(35,25),(36,25),(36,27),(35,27),(30,29),(25,30),(19,31),(17,31),(10,30),(5,30),(0,27),(6,8)]
        Body_backward_points=[(0,0),(99,0),(99,31),(81,122),(80,123),(78,131),(77,132),(77,133),(75,135),(70,140),(65,142),(55,145),(45,145),(39,143),(34,142),(28,139),(26,137),(25,137),(22,134),(20,131),(18,126),(0,27)]

        out=[None,Neck_backward_points,Head_backward_points,Forearm1_backward_points,Forearm2_backward_points,Body_backward_points,Bicep_backward_left_points,Bicep_backward_right_points,Shin1_backward_points,Shin1_backward_points,Thigh_right_points,Thigh_left_points,Skirt2_backward_points,Belt_backward_points,Shoe1_backward_points,Shoe1_backward_points]
        transforms=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-17),95],    ##Neck
                    [0,int(wf.character_width/2-42),0],     ##Head
                    [-5,int(wf.character_width/2-78+5),200],##Forearm1
                    [5,int(wf.character_width/2+48-5),198], ##Forearm2
                    [0,int(wf.character_width/2-50),120],   ##Body
                    [0,10+5,120],                           ##Bicep left
                    [0,int(wf.character_width/2+30-5),120], ##Bicep right
                    [0,int(wf.character_width/2-28),352],   ##Shin1
                     [0,int(wf.character_width/2+2),352],    ##Shin2
                    [0,int(wf.character_width/2-33),260],   ##Right thigh
                    [0,int(wf.character_width/2+2),260],    ##Left thigh
                    [0,int(wf.character_width/2-50),260],   ##Skirt in the back
                    [0,int(wf.character_width/2-32),248],   ##Belt
                    [0,int(wf.character_width/2),410],      ##Shoe1
                    [0,50,410]]                             ##Shoe2

        ##Draw Character_UP##
        Draw_step(out,transforms,self.character_region[1],self.character_hdc[1])
        out1=[None,Neck_backward_points,Head_backward_points,Forearm1_backward_points,Forearm2_backward_points,Bicep_backward_left_points,Bicep_backward_right_points,Body_backward_points,Shoe1_backward_points,Shin1_backward_points,Shin1_backward_points,Thigh_right_points,Thigh_left_points,Skirt2_backward_points,Belt_backward_points,Shoe1_backward_points]
        transforms2=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-17),95],    ##Neck
                    [0,int(wf.character_width/2-42),0],     ##Head
                    [5,int(wf.character_width/2-78+18),200],##Forearm1
                    [5,int(wf.character_width/2+48-5),198], ##Forearm2
                    [-7,10+5,120],                           ##Bicep left
                    [0,int(wf.character_width/2+30-5),120], ##Bicep right
                    [0,int(wf.character_width/2-50),120],   ##Body
                    [0,52,410],                             ##Shoe2
                    [0,int(wf.character_width/2-28),352],   ##Shin1
                    [0,int(wf.character_width/2+2),352],    ##Shin2
                    [0,int(wf.character_width/2-33),260],   ##Right thigh
                    [0,int(wf.character_width/2+2),260],    ##Left thigh
                    [0,int(wf.character_width/2-50),260],   ##Skirt in the front
                    [0,int(wf.character_width/2-32),248],   ##Belt
                    [0,int(wf.character_width/2),410]]      ##Shoe1
        transforms_x=[[0,0,0],                              ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,13],                             ##Forearm1
                      [30,0,18],                            ##Forearm2
                      [40,0,33],                             ##Bicep left
                      [30,0,18],                            ##Bicep right
                      [0,0,0],                              ##Body
                      [0,0,-6],                             ##Shoe2
                      [15,0,-5],                            ##Shin1
                      [15,0,-5],                            ##Shin2
                      [20,0,15],                            ##Right thigh
                      [20,0,15],                            ##Left thigh
                      [0,0,0],                              ##Skirt in the front
                      [0,0,0],                              ##Belt
                      [0,0,-3]]                             ##Shoe1

        ##Draw Character_UP##
        Draw_step(out1,transforms2,self.character_region[7],self.character_hdc[7],transforms_x)

        ##Draw Character_UP##
        Draw_step(out,transforms,self.character_region[8],self.character_hdc[8])
        out2=[None,Neck_backward_points,Head_backward_points,Forearm1_backward_points,Forearm2_backward_points,Bicep_backward_left_points,Bicep_backward_right_points,Body_backward_points,Shoe1_backward_points,Shin1_backward_points,Shin1_backward_points,Thigh_right_points,Thigh_left_points,Skirt2_backward_points,Belt_backward_points,Shoe1_backward_points]
        transforms3=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-17),95],    ##Neck
                    [0,int(wf.character_width/2-42),0],     ##Head
                    [-5,int(wf.character_width/2-78+5),200],##Forearm1
                    [-5,int(wf.character_width/2+48-18),198], ##Forearm2
                    [0,10+5,120],                           ##Bicep left
                    [7,int(wf.character_width/2+30-5),120], ##Bicep right
                    [0,int(wf.character_width/2-50),120],   ##Body
                    [0,int(wf.character_width/2)-4,410],    ##Shoe1
                    [0,int(wf.character_width/2-28),352],   ##Shin1
                    [0,int(wf.character_width/2+2),352],    ##Shin2
                    [0,int(wf.character_width/2-33),260],   ##Right thigh
                    [0,int(wf.character_width/2+2),260],    ##Left thigh
                    [0,int(wf.character_width/2-50),260],   ##Skirt in the front
                    [0,int(wf.character_width/2-32),248],   ##Belt
                    [0,50,410]]                             ##Shoe2
        transforms_x=[[0,0,0],                              ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,18],                             ##Forearm1
                      [30,0,17],                            ##Forearm2
                      [30,0,18],                             ##Bicep left
                      [40,0,28],                            ##Bicep right
                      [0,0,0],                              ##Body
                      [0,0,-6],                             ##Shoe2
                      [15,0,-5],                            ##Shin1
                      [15,0,-5],                            ##Shin2
                      [20,0,15],                            ##Right thigh
                      [20,0,15],                            ##Left thigh
                      [0,0,0],                              ##Skirt in the front
                      [0,0,0],                              ##Belt
                      [0,0,-3]]                             ##Shoe1


        ##Draw Character_UP##
        Draw_step(out2,transforms3,self.character_region[9],self.character_hdc[9],transforms_x)
##        Points=wf.REGION(19)
        ##Character1_up##
##        self.character_region[1][0]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
##        for i in range(20,27):
##            Points=wf.REGION(i)
##            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
##            windll.gdi32.CombineRgn(self.character_region[1][0],self.character_region[1][0],temp,wf.RGN_OR)
##        self.character_region[1][1]=self.character_region[1][0]

        ##Character1_RIGHT##
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
        Shoe_right_points=[(5,2),(6,2),(8,4),(20,4),(21,3),(23,3),(24,2),(28,1),(32,0),(35,0),(42,1),(43,2),(44,2),(51,5),(56,10),(56,11),(58,13),(61,20),(61,22),(63,22),(63,25),(0,25),(1,14),(2,8),(3,4)]
        
        out=[None,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Thigh_right_points,Skirt_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points,Shoe_right_points]
        transforms=[[0,0,0],                                ##Canvas
                    [0,int(wf.character_width/2-10),100],   ##Neck
                    [0,int(wf.character_width/2-77/2),0],   ##Head
                    [0,int(wf.character_width/2-34),115],   ##Body
                    [0,int(wf.character_width/2-12),345],   #Shin
                    [0,int(wf.character_width/2-15),255],   ##Thigh
                    [0,int(wf.character_width/2-41),262],   #Skirt
                    [0,int(wf.character_width/2-24),245],   ##Belt
                    [0,int(wf.character_width/2-15),115],   ##Bicep
                    [0,int(wf.character_width/2-20),180],   ##Forearm
                    [0,int(wf.character_width/2-13),410]]   ##Shoe

        ##Draw Character RIGHT##
        Draw_step(out,transforms,self.character_region[2],self.character_hdc[2])
        out2=[None,Bicep_right_points,Forearm_right_points,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Shin_right_points,Thigh_right_points,Thigh_right_points,Skirt2_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points,Shoe_right_points,Shoe_right_points]
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
                     [-25,int(wf.character_width/2-15),125],    ##Bicep
                     [-35,int(wf.character_width/2+10),190],    ##Forearm
                     [-5,int(wf.character_width/2+36),410],     ##Shoe1
                     [10,int(wf.character_width/2-62),400]]     ##Shoe2

        ##Draw_Character RIGHT##        
        Draw_step(out2,transforms2,self.character_region[10],self.character_hdc[10])
        out3=[None,Bicep_right_points,Forearm_right_points,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Shin_right_points,Thigh_right_points,Thigh_right_points,Skirt_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points,Shoe_right_points,Shoe_right_points]
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
                     [0,int(wf.character_width/2-15),115],  ##Bicep
                     [0,int(wf.character_width/2-20),180],  ##Forearm
                     [0,int(wf.character_width/2-13),410],  ##Shoe1
                     [0,int(wf.character_width/2-13),410]]  ##Shoe2

        ##Draw_Character RIGHT##
        Draw_step(out3,transforms3,self.character_region[11],self.character_hdc[11])
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
                     [30,int(wf.character_width/2-15),110],     ##Bicep
                     [10,int(30),170],                          ##Forearm
                     [10,int(wf.character_width/2-62),400],     ##Shoe1
                     [-5,int(wf.character_width/2+36),410]]     ##Shoe2

        ##Draw_Character RIGHT##
        Draw_step(out2,transforms4,self.character_region[12],self.character_hdc[12])

        ##Character1_LEFT##
        Head_left_points=[(36,0),(34,3),(31,3),(29,4),(26,6),(25,6),(22,8),(22,11),(21,11),(19,13),(18,14),(18,18),(15,18),(13,20),(15,25),(15,27),(11,34),(11,36),(10,36),(9,37),(9,38),(10,39),(10,43),(9,44),(5,51),(5,52),(3,54),(0,62),(0,64),(5,65),(7,66),(10,84),(13,90),(15,96),(18,98),(18,99),(26,107),(36,110),(37,110),(46,108),(47,107),(55,99),(55,98),(58,96),(60,89),(62,85),(64,78),(66,65),(69,58),(71,56),(71,54),(74,49),(75,45),(73,42),(76,37),(76,33),(75,31),(75,27),(74,24),(72,20),(70,17),(67,11),(64,10),(61,7),(58,5),(53,3),(48,4),(44,1),(42,0)]
        Neck_left_points=[(0,6),(2,4),(2,3),(3,2),(9,0),(10,0),(16,2),(16,3),(19,7),(19,24),(18,26),(14,30),(10,31),(5,30),(1,26),(0,23)]
        Body_left_points=[(47,1),(20,0),(8,9),(4,14),(0,25),(3,70),(7,132),(10,136),(11,138),(15,142),(19,144),(23,146),(33,148),(43,146),(48,144),(54,138),(56,133),(58,125),(64,70),(67,39),(67,33),(66,23),(64,17),(62,14),(60,11),(54,5),(51,4),(49,2)]
        Bicep_left_points=[(29,39),(28,24),(27,11),(25,6),(23,5),(23,4),(21,1),(18,0),(8,0),(6,2),(4,3),(3,6),(1,9),(1,38),(4,39),(4,46),(5,47),(6,54),(7,59),(8,68),(10,72),(13,75),(17,76),(19,76),(23,75),(26,72),(26,39)]
        Forearm_left_points=[(28,0),(23,0),(21,1),(18,4),(16,11),(16,19),(15,37),(14,42),(14,49),(12,51),(9,59),(9,73),(14,75),(22,77),(24,74),(24,71),(28,63),(28,59),(25,52),(29,44),(30,41),(32,35),(34,29),(35,24),(35,11),(33,4),(30,1)]
        Belt_left_points=[(52,0),(41,0),(40,1),(24,1),(23,2),(2,2),(1,11),(0,23),(5,23),(6,24),(16,24),(17,25),(36,25),(37,26),(51,26),(52,25),(53,21),(53,1)]
        Thigh_left_points=[(3,0),(2,7),(1,19),(0,35),(0,50),(1,71),(3,94),(5,98),(7,100),(11,101),(19,101),(21,99),(22,99),(23,98),(25,92),(27,86),(28,78),(29,71),(30,62),(30,32),(29,19),(28,11),(27,4),(26,0)]
        Shin_left_points=[(14,0),(9,0),(6,1),(2,5),(1,9),(0,21),(0,34),(1,71),(1,75),(5,79),(8,80),(10,80),(14,79),(18,76),(19,71),(21,60),(23,44),(24,37),(23,23),(21,10),(20,5),(16,1),(15,1)]
        Skirt_left_points=[(69,0),(18,0),(0,89),(0,92),(2,97),(3,99),(9,101),(15,101),(19,97),(22,101),(23,102),(28,104),(30,104),(35,102),(37,98),(40,104),(42,105),(44,107),(47,107),(51,106),(53,104),(55,100),(57,104),(58,105),(61,107),(66,107),(68,105),(69,105),(70,104),(71,101),(73,103),(73,104),(75,106),(78,107),(79,107),(83,106),(85,104),(86,101),(87,97),(87,95),(73,16)]
        Skirt2_left_points=[(76,0),(25,0),(0,82),(0,86),(2,93),(4,95),(5,96),(7,93),(7,89),(7,92),(9,97),(10,99),(16,101),(22,101),(26,97),(29,101),(30,102),(35,104),(37,104),(42,102),(44,98),(47,104),(49,105),(51,107),(54,107),(58,106),(60,104),(62,100),(64,104),(65,105),(68,107),(73,107),(75,105),(76,105),(77,104),(78,101),(80,103),(80,104),(82,106),(85,107),(86,107),(90,106),(92,104),(93,101),(94,97),(97,96),(99,93),(99,88)]
        Shoe_left_points=[(58,2),(57,2),(55,4),(43,4),(42,3),(40,3),(39,2),(35,1),(31,0),(28,0),(21,1),(20,2),(19,2),(12,5),(7,10),(7,11),(5,13),(2,20),(2,22),(0,22),(0,25),(63,25),(62,14),(61,8),(60,4)]
        out=[None,Neck_left_points,Head_left_points,Body_left_points,Shin_left_points,Thigh_left_points,Skirt_left_points,Belt_left_points,Bicep_left_points,Forearm_left_points,Shoe_left_points]
        transforms=[[0,0,0],                                   ##Canvas
                    [0,int(wf.character_width/2-12+13),100],   ##Neck
                    [0,int(wf.character_width/2-77/2+13),0],   ##Head
                    [0,int(wf.character_width/2-36+13),115],   ##Body
                    [0,int(wf.character_width/2-17+13),345],   #Shin
                    [0,int(wf.character_width/2-19+13),255],   ##Thigh
                    [0,int(wf.character_width/2-49+13),262],   #Skirt
                    [0,int(wf.character_width/2-31+13),245],   ##Belt
                    [0,int(wf.character_width/2-16+13),115],   ##Bicep
                    [0,int(wf.character_width/2-25+13),180],   ##Forearm
                    [0,int(wf.character_width/2-54+13),410]]   ##Shoe

        ##Draw_Character LEFT##
        Draw_step(out,transforms,self.character_region[3],self.character_hdc[3])
        out2=[None,Bicep_left_points,Forearm_left_points,Neck_left_points,Head_left_points,Body_left_points,Shin_left_points,Shin_left_points,Thigh_left_points,Thigh_left_points,Skirt2_left_points,Belt_left_points,Bicep_left_points,Forearm_left_points,Shoe_left_points,Shoe_left_points]
        transforms2=[[0,0,0],                                   ##Canvas
                     [-30,int(wf.character_width/2-12+13),127], ##Bicep_right
                     [-10,int(wf.character_width/2+12+13),177], ##Forearm
                     [0,int(wf.character_width/2-12+13),100],   ##Neck
                     [0,int(wf.character_width/2-77/2+13),0],   ##Head
                     [0,int(wf.character_width/2-36+13),115],   ##Body
                     [5,int(wf.character_width/2-55+13),336],   #Shin1
                     [-20,int(wf.character_width/2+8+13),340],  #Shin2
                     [25,int(wf.character_width/2-15+13),253],  ##Thigh1
                     [-18,int(wf.character_width/2-18+13),262], ##Thigh2
                     [0,int(wf.character_width/2-55+13),262],   ##Skirt
                     [0,int(wf.character_width/2-31+13),245],   ##Belt
                     [25,int(wf.character_width/2-15+13),112],  ##Bicep
                     [35,int(wf.character_width/2-48+13),165],  ##Forearm
                     [5,int(-13+13),405],                       ##Shoe1
                     [-10,int(wf.character_width/2-5+13),410]]  ##Shoe2

        ##Draw_Character LEFT##       
        Draw_step(out2,transforms2,self.character_region[13],self.character_hdc[13])
        out3=[None,Bicep_left_points,Forearm_left_points,Neck_left_points,Head_left_points,Body_left_points,Shin_left_points,Shin_left_points,Thigh_left_points,Thigh_left_points,Skirt_left_points,Belt_left_points,Bicep_left_points,Forearm_left_points,Shoe_left_points,Shoe_left_points]
        transforms3=[[0,0,0],                                   ##Canvas
                     [0,int(wf.character_width/2-16+13),115],   ##Bicep
                     [0,int(wf.character_width/2-25+13),180],   ##Forearm
                     [0,int(wf.character_width/2-12+13),100],   ##Neck
                     [0,int(wf.character_width/2-77/2+13),0],   ##Head
                     [0,int(wf.character_width/2-36+13),115],   ##Body
                     [0,int(wf.character_width/2-17+13),345],   #Shin1
                     [0,int(wf.character_width/2-17+13),345],   #Shin2
                     [0,int(wf.character_width/2-19+13),255],   ##Thigh1
                     [0,int(wf.character_width/2-19+13),255],   ##Thigh2
                     [0,int(wf.character_width/2-49+13),262],   #Skirt
                     [0,int(wf.character_width/2-31+13),245],   ##Belt
                     [0,int(wf.character_width/2-16+13),115],   ##Bicep
                     [0,int(wf.character_width/2-25+13),180],   ##Forearm
                     [0,int(wf.character_width/2-54+13),410],   ##Shoe1
                     [0,int(wf.character_width/2-54+13),410]]   ##Shoe2

        ##Draw_Character LEFT##
        Draw_step(out3,transforms3,self.character_region[14],self.character_hdc[14])
        transforms4=[[0,0,0],                                   ##Canvas
                     [25,int(wf.character_width/2-15+13),112],  ##Bicep
                     [35,int(wf.character_width/2-48+13),165],  ##Forearm
                     [0,int(wf.character_width/2-12+13),100],   ##Neck
                     [0,int(wf.character_width/2-77/2+13),0],   ##Head
                     [0,int(wf.character_width/2-36+13),115],   ##Body
                     [-20,int(wf.character_width/2+8+13),340],  #Shin1
                     [5,int(wf.character_width/2-55+13),336],   #Shin2
                     [-18,int(wf.character_width/2-18+13),262], ##Thigh1
                     [25,int(wf.character_width/2-15+13),253],  ##Thigh2
                     [0,int(wf.character_width/2-55+13),262],   ##Skirt
                     [0,int(wf.character_width/2-31+13),245],   ##Belt
                     [-30,int(wf.character_width/2-12+13),127], ##Bicep_right
                     [-10,int(wf.character_width/2+12+13),177], ##Forearm
                     [-10,int(wf.character_width/2-5+13),410],  ##Shoe1
                     [5,int(-13+13),405]]                       ##Shoe2

        ##Draw_Character LEFT
        Draw_step(out2,transforms4,self.character_region[15],self.character_hdc[15])

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

        ##RELEASE UNNEEDED HDCS##
        for i in range(10):
            for j in range(1,18):
                if j<5 or (i>=4 and j<16) or ((i==2 or i==3) and j<11) or (i==0 and j<17):
                    ##Release HDC##
                    windll.user32.ReleaseDC(hwnd,self.character_hdc[i][j])                  #Make hdc similar to the reference hdc
        
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
        self.step=0
        for j in range(1):
            i=self.dict_index_to_character["character"+str(int(self.step)+1)+"_"+self.direction]        ##Find the desired image
            windll.gdi32.OffsetRgn(self.character_region[i][j],                                         ##Shift the region to draw the character
                                   position_new)
            windll.gdi32.SelectClipRgn(hdc,self.character_region[i][j])                                 ##Select the shifted region for copying the image
            windll.gdi32.BitBlt(hdc,position_new,wf.character_width+50,                                    ##Add Character to Background
                                wf.character_height,self.character_hdc[i][j],
                                0,0,wf.SRCCOPY)
            ##Reset class object and hdc##
            windll.gdi32.SelectClipRgn(hdc,None)                                                        ##Remove clipping region
            windll.gdi32.OffsetRgn(self.character_region[i][j],-position_new.x,                         #Return Region to original positoin
                                    -position_new.y)
