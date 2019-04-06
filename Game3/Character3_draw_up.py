##THIS FUNCTION RETURNS ANIMATION IMAGES FOR UP DIRECTION##
from window_structures import *
from window_functions import *
from ctypes import *
from ctypes.wintypes import *

def Draw_UP(hdc_main,file_path_main,hwnd):
    ##Initialize hdcs and load images##
        [character1_up_file,Head1_backward_file,Neck1_backward_file,Body1_backward_file,
        Bicep1_backward_file,Bicep2_backward_file,Forearm1_backward_file,Forearm2_backward_file,
         Belt1_backward_file,Skirt1_backward_file,Shin1_backward_file,Shoe1_backward_file,
         Forearm3_backward_file,Forearm4_backward_file,Shoe2_backward_file,Shoe3_backward_file,
         Belt2_backward_file,Belt3_backward_file,Thigh1_right_file,Thigh1_left_file]=["Face_backward_1a.bmp","Head_backward_1a.bmp","Neck_forward_1a.bmp","Body_backward_3a.bmp",
                                "Bicep_forward_left_1a.bmp","Bicep_forward_right_1a.bmp","Forearm_backward_1a.bmp","Forearm_backward_1b.bmp",
                                "Belt_backward_1a.bmp","Skirt_backward_1b.bmp","Shin_forward_1a.bmp","Shoe_backward_1a.bmp",
                                "Forearm_backward_1c.bmp","Forearm_backward_1d.bmp","Shoe_backward_1b.bmp","Shoe_backward_1c.bmp",
                                "Belt_backward_1b.bmp","Belt_backward_1c.bmp","Thigh_right_1a.bmp","Thigh_left_1a.bmp"]

        ##Define dictionaries for the character##
        character_files=[[character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm1_backward_file,Forearm2_backward_file,Body1_backward_file,Bicep1_backward_file,Bicep2_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt1_backward_file,Shoe1_backward_file,Shoe1_backward_file],
                        [character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm3_backward_file,Forearm2_backward_file,Body1_backward_file,Bicep1_backward_file,Bicep2_backward_file,Shoe3_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt2_backward_file,Shoe2_backward_file],
                        [character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm1_backward_file,Forearm2_backward_file,Body1_backward_file,Bicep1_backward_file,Bicep2_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt1_backward_file,Shoe1_backward_file,Shoe1_backward_file],
                        [character1_up_file,Neck1_backward_file,Head1_backward_file,Forearm1_backward_file,Forearm4_backward_file,Body1_backward_file,Bicep1_backward_file,Bicep2_backward_file,Shoe3_backward_file,Shin1_backward_file,Shin1_backward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_backward_file,Belt3_backward_file,Shoe2_backward_file]]        
        character_hbmp=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],                        
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]                             
        character_hdc=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],                            
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        character_region=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        for i in range(4):
            for j in range(16):
                character_hbmp[i][j]=LoadImage(c_void_p(),LPCWSTR(file_path_main+character_files[i][j]),IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
                ##Create HDC##
                character_hdc[i][j]=windll.gdi32.CreateCompatibleDC(hdc_main)                  #Make hdc similar to the reference hdc
                windll.gdi32.SetGraphicsMode(character_hdc[i][j],GM_ADVANCED)
                windll.gdi32.SelectObject(character_hdc[i][j],character_hbmp[i][j])       #Copy image into hdc

        ##DEFINE INITIAL POINTS##
        Head_backward_points=[(41,1),(23,1),(22,2),(19,2),(20,7),(17,7),(16,9),(14,9),(13,15),(10,19),(8,21),(7,25),(4,30),(4,35),(1,37),(2,40),(5,43),(4,46),(1,49),(0,51),(0,59),(2,63),(5,65),(5,69),(6,74),(7,77),(9,81),(10,83),(12,88),(15,91),(16,94),(22,100),(24,101),(28,103),(37,106),(45,106),(52,104),(57,102),(60,99),(67,92),(68,90),(69,88),(71,86),(73,82),(74,80),(75,77),(76,72),(77,67),(80,66),(82,64),(83,60),(83,52),(81,49),(80,46),(77,46),(77,45),(79,44),(81,43),(81,41),(80,40),(79,38),(79,35),(80,34),(80,33),(79,32),(80,30),(79,29),(80,28),(80,27),(77,22),(74,22),(74,17),(73,15),(71,13),(67,12),(66,10),(65,10),(64,6),(62,4),(60,3),(57,2),(56,1),(62,1),(48,0)]
        Neck_backward_points=[(17,0),(22,1),(26,5),(27,9),(27,13),(29,22),(30,24),(33,27),(33,29),(32,32),(29,35),(24,37),(17,38),(9,37),(6,36),(4,35),(1,32),(0,29),(0,27),(3,24),(4,21),(5,17),(6,13),(6,8),(7,5),(10,2),(16,0)]
        Bicep_backward_left_points=[(35,0),(34,3),(42,10),(41,11),(45,14),(47,21),(48,26),(48,28),(47,33),(46,37),(44,38),(44,39),(38,45),(37,45),(35,47),(34,47),(31,50),(31,55),(29,55),(26,61),(23,62),(22,68),(21,75),(20,81),(19,82),(19,90),(14,95),(8,95),(4,94),(2,90),(2,84),(2,79),(3,75),(5,63),(6,58),(7,52),(7,50),(6,49),(8,47),(8,31),(10,29),(15,6),(17,4),(27,0)]
        Bicep_backward_right_points=[(13,0),(14,3),(6,10),(7,11),(3,14),(1,21),(0,26),(0,28),(1,33),(2,37),(4,38),(4,39),(10,45),(11,45),(13,47),(14,47),(17,50),(17,55),(19,55),(22,61),(25,62),(26,68),(27,75),(28,81),(29,82),(29,90),(34,95),(40,95),(44,94),(46,90),(46,84),(46,79),(45,75),(43,63),(42,58),(41,52),(41,50),(42,49),(40,47),(40,31),(38,29),(33,6),(31,4),(21,0)]
        Forearm1_backward_points=[(10,0),(14,1),(18,5),(19,8),(18,9),(19,35),(20,45),(25,44),(26,47),(27,51),(28,54),(29,57),(27,58),(13,62),(11,62),(8,61),(4,57),(3,54),(3,49),(1,17),(0,16),(0,11),(3,3),(5,1),(9,0)]
        Forearm2_backward_points=[(19,0),(15,1),(11,5),(10,8),(11,9),(10,35),(9,45),(4,44),(3,47),(2,51),(1,54),(0,57),(2,58),(16,62),(18,62),(21,61),(25,57),(26,54),(26,49),(28,17),(29,16),(29,11),(26,3),(24,1),(20,0)]
        Belt_backward_points=[(0,0),(62,0),(64,26),(0,26)]
        Skirt2_backward_points=[(78,0),(20,0),(0,96),(0,98),(1,101),(3,103),(3,105),(11,107),(19,105),(21,103),(23,107),(26,110),(30,110),(32,108),(34,104),(36,106),(37,106),(38,107),(38,109),(39,109),(42,110),(46,110),(49,109),(50,109),(51,106),(54,101),(57,102),(58,103),(59,106),(60,107),(62,109),(65,110),(69,110),(72,109),(76,105),(76,103),(77,102),(78,99),(79,96),(83,105),(90,108),(98,106),(101,103),(103,98),(103,88)]
        Thigh_right_points=[(27,0),(28,7),(29,19),(30,35),(30,50),(29,71),(27,94),(25,98),(23,100),(19,101),(11,101),(9,99),(8,99),(7,98),(5,92),(3,86),(2,78),(1,71),(0,62),(0,32),(1,19),(2,11),(3,4),(4,0)]
        Thigh_left_points=[(3,0),(2,7),(1,19),(0,35),(0,50),(1,71),(3,94),(5,98),(7,100),(11,101),(19,101),(21,99),(22,99),(23,98),(25,92),(27,86),(28,78),(29,71),(30,62),(30,32),(29,19),(28,11),(27,4),(26,0)]
        Shin1_backward_points=[(11,0),(13,0),(16,1),(20,5),(21,8),(22,18),(23,19),(24,40),(23,41),(23,44),(21,60),(20,72),(20,76),(16,79),(13,80),(11,80),(8,79),(4,75),(4,73),(3,60),(1,45),(0,36),(0,32),(1,30),(1,24),(3,7),(4,5),(8,1)]
        Shoe1_backward_points=[(16,0),(20,0),(25,2),(31,8),(34,15),(36,22),(36,25),(0,25),(0,22),(1,21),(1,19),(2,15),(5,8),(11,2)]
        Shoe2_backward_points=[(0,27),(1,21),(3,13),(8,8),(8,5),(11,2),(16,0),(20,0),(27,3),(27,4),(30,8),(30,9),(32,11),(34,16),(35,17),(35,24),(36,24),(36,27),(34,27),(33,28),(32,28),(31,29),(19,32),(15,31),(10,30),(6,29),(3,28)]
        Shoe3_backward_points=[(15,0),(21,0),(26,1),(32,7),(33,10),(34,15),(36,20),(36,22),(35,23),(35,24),(33,26),(33,27),(32,28),(6,28),(4,26),(4,25),(3,24),(1,24),(0,20),(1,19),(3,11),(5,6),(10,1)]
        Body_backward_points=[(0,0),(99,0),(99,31),(81,122),(80,123),(78,131),(77,132),(77,133),(75,135),(70,140),(65,142),(55,145),(45,145),(39,143),(34,142),(28,139),(26,137),(25,137),(22,134),(20,131),(18,126),(0,27)]

        out0=[None,Neck_backward_points,Head_backward_points,Forearm1_backward_points,Forearm2_backward_points,Body_backward_points,Bicep_backward_left_points,Bicep_backward_right_points,Shin1_backward_points,Shin1_backward_points,Thigh_right_points,Thigh_left_points,Skirt2_backward_points,Belt_backward_points,Shoe1_backward_points,Shoe1_backward_points]
        transforms0=[[0,0,0],                               ##Canvas
                    [0,int(character_width/2-17),95],       ##Neck
                    [0,int(character_width/2-42),0],        ##Head
                    [-5,int(character_width/2-78+5),200],   ##Forearm1
                    [5,int(character_width/2+48-5),198],    ##Forearm2
                    [0,int(character_width/2-50),120],      ##Body
                    [0,10+5,120],                           ##Bicep left
                    [0,int(character_width/2+30-5),120],    ##Bicep right
                    [0,int(character_width/2-28),352],      ##Shin1
                    [0,int(character_width/2+2),352],       ##Shin2
                    [0,int(character_width/2-33),260],      ##Right thigh
                    [0,int(character_width/2+2),260],       ##Left thigh
                    [0,int(character_width/2-50),260],      ##Skirt in the back
                    [0,int(character_width/2-32),248],      ##Belt
                    [0,int(character_width/2),410],         ##Shoe1
                    [0,50,410]]                             ##Shoe2

        ##Draw Character_UP_step0##
        Draw_step(out0,transforms0,character_region[0],character_hdc[0])
        out1=[None,Neck_backward_points,Head_backward_points,Forearm1_backward_points,Forearm2_backward_points,Body_backward_points,Bicep_backward_left_points,Bicep_backward_right_points,Shoe3_backward_points,Shin1_backward_points,Shin1_backward_points,Thigh_right_points,Thigh_left_points,Skirt2_backward_points,Belt_backward_points,Shoe2_backward_points]
        transforms1=[[0,0,0],                               ##Canvas
                    [0,int(character_width/2-17),95],       ##Neck
                    [0,int(character_width/2-42),0],        ##Head
                    [5,int(character_width/2-78+18),200],   ##Forearm1
                    [5,int(character_width/2+48-5),198],    ##Forearm2
                    [0,int(character_width/2-50),120],      ##Body
                    [-7,10+5,120],                          ##Bicep left
                    [0,int(character_width/2+30-5),120],    ##Bicep right
                    [0,int(character_width/2),410],         ##Shoe1
                    [0,int(character_width/2-28),352],      ##Shin1
                    [0,int(character_width/2+2),352],       ##Shin2
                    [0,int(character_width/2-33),260],      ##Right thigh
                    [0,int(character_width/2+2),260],       ##Left thigh
                    [0,int(character_width/2-50),260],      ##Skirt in the front
                    [0,int(character_width/2-32),248],      ##Belt
                    [0,52,410]]                             ##Shoe2
        transforms_x1=[[0,0,0],                             ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,13],                            ##Forearm1
                      [30,0,18],                            ##Forearm2
                      [0,0,0],                              ##Body
                      [40,0,33],                            ##Bicep left
                      [30,0,18],                            ##Bicep right
                      [0,-4,-10],                           ##Shoe1
                      [15,0,-5],                            ##Shin1
                      [15,0,-5],                            ##Shin2
                      [20,0,15],                            ##Right thigh
                      [20,0,15],                            ##Left thigh
                      [0,0,0],                              ##Skirt in the front
                      [0,0,0],                              ##Belt
                      [0,0,-6]]                             ##Shoe2

        ##Draw Character_UP_step1##
        Draw_step(out1,transforms1,character_region[1],character_hdc[1],transforms_x1)

        ##Draw Character_UP_step2##
        Draw_step(out0,transforms0,character_region[2],character_hdc[2])
        out3=[None,Neck_backward_points,Head_backward_points,Forearm1_backward_points,Forearm2_backward_points,Body_backward_points,Bicep_backward_left_points,Bicep_backward_right_points,Shoe3_backward_points,Shin1_backward_points,Shin1_backward_points,Thigh_right_points,Thigh_left_points,Skirt2_backward_points,Belt_backward_points,Shoe2_backward_points]
        transforms3=[[0,0,0],                               ##Canvas
                    [0,int(character_width/2-17),95],       ##Neck
                    [0,int(character_width/2-42),0],        ##Head
                    [-5,int(character_width/2-78+5),200],   ##Forearm1
                    [-5,int(character_width/2+48-18),198],  ##Forearm2
                    [0,int(character_width/2-50),120],      ##Body
                    [0,10+5,120],                           ##Bicep left
                    [7,int(character_width/2+30-5),120],    ##Bicep right
                    [0,52,410],                             ##Shoe1
                    [0,int(character_width/2-28),352],      ##Shin1
                    [0,int(character_width/2+2),352],       ##Shin2
                    [0,int(character_width/2-33),260],      ##Right thigh
                    [0,int(character_width/2+2),260],       ##Left thigh
                    [0,int(character_width/2-50),260],      ##Skirt in the front
                    [0,int(character_width/2-32),248],      ##Belt
                    [0,int(character_width/2),410]]         ##Shoe2
        transforms_x3=[[0,0,0],                             ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,18],                            ##Forearm1
                      [30,0,17],                            ##Forearm2
                      [0,0,0],                              ##Body
                      [30,0,18],                            ##Bicep left
                      [40,0,28],                            ##Bicep right
                      [0,0,-8],                             ##Shoe2
                      [15,0,-5],                            ##Shin1
                      [15,0,-5],                            ##Shin2
                      [20,0,15],                            ##Right thigh
                      [20,0,15],                            ##Left thigh
                      [0,0,0],                              ##Skirt in the front
                      [0,0,0],                              ##Belt
                      [0,-2,-6]]                            ##Shoe1


        ##Draw Character_UP##
        Draw_step(out3,transforms3,character_region[3],character_hdc[3],transforms_x3)

        ##RELEASE UNNEEDED HDCS##
        for i in range(4):
            for j in range(1,17):
                if len(character_hbmp[i])>j:
                    ##Release HDC##
                    windll.user32.ReleaseDC(hwnd,character_hdc[i][j])
        ##RETURN COMPILED IMAGES##
        return [[character_hdc[0][0],character_hdc[1][0],character_hdc[2][0],character_hdc[3][0]],
                [character_region[0][0],character_region[1][0],character_region[2][0],character_region[3][0]]]

