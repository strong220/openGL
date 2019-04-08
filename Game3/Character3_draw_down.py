##THIS FUNCTION RETURNS ANIMATION IMAGES FOR DOWN DIRECTION##
from window_structures import *
from window_functions import *
from ctypes import *
from ctypes.wintypes import *

def Draw_DOWN(hdc_main,file_path_main,hwnd):
    ##Initialize hdcs and load images##
        [character1_down_file,Head1_forward_file,Neck1_forward_file,Body1_forward_file,
        Forearm1_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,
         Head2_forward_file,Belt1_forward_file,Skirt1_forward_file,Skirt1_backward_file,
         Shin1_forward_file,Shoe1_forward_file,Shoe2_forward_file,Shoe3_forward_file,
         Belt2_forward_file,Belt3_forward_file,Forearm3_forward_file,Forearm4_forward_file,
         Thigh1_right_file,Thigh1_left_file]=["Face_forward_1a.bmp","Head_forward_1a.bmp","Neck_forward_1a.bmp","Body_forward_3a.bmp",
                                              "Forearm_forward_1a.bmp","Forearm_forward_1b.bmp","Bicep_forward_left_3a.bmp","Bicep_forward_right_3a.bmp",
                                              "Head_forward_1b.bmp","Belt_forward_1b.bmp","Skirt_forward_1a.bmp","Skirt_backward_1a.bmp",
                                              "Shin_forward_1a.bmp","Shoe_forward_1a.bmp","Shoe_forward_1b.bmp","Shoe_forward_1c.bmp",
                                              "Belt_forward_1c.bmp","Belt_forward_1d.bmp","Forearm_forward_1c.bmp","Forearm_forward_1d.bmp",
                                              "Thigh_right_1a.bmp","Thigh_left_1a.bmp"]

        ##Define dictionaries for the character##
        character_files=[[character1_down_file,Neck1_forward_file,Head1_forward_file,Forearm1_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt1_forward_file,Shoe1_forward_file,Shoe1_forward_file],            
                              [character1_down_file,Neck1_forward_file,Head2_forward_file,Forearm3_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shoe3_forward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt3_forward_file,Shoe2_forward_file],
                              [character1_down_file,Neck1_forward_file,Head2_forward_file,Forearm1_forward_file,Forearm2_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt1_forward_file,Shoe1_forward_file,Shoe1_forward_file],
                              [character1_down_file,Neck1_forward_file,Head2_forward_file,Forearm1_forward_file,Forearm4_forward_file,Bicep1_forward_left_file,Bicep1_forward_right_file,Body1_forward_file,Skirt1_backward_file,Shoe3_forward_file,Shin1_forward_file,Shin1_forward_file,Thigh1_right_file,Thigh1_left_file,Skirt1_forward_file,Belt2_forward_file,Shoe2_forward_file]]        
        character_hbmp=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],                        
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]                             
        character_hdc=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],                            
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        character_region=[[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        for i in range(4):
            for j in range(17):
                character_hbmp[i][j]=LoadImage(c_void_p(),LPCWSTR(file_path_main+character_files[i][j]),IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
                ##Create HDC##
                character_hdc[i][j]=windll.gdi32.CreateCompatibleDC(hdc_main)                  #Make hdc similar to the reference hdc
                windll.gdi32.SetGraphicsMode(character_hdc[i][j],GM_ADVANCED)
                windll.gdi32.SelectObject(character_hdc[i][j],character_hbmp[i][j])       #Copy image into hdc

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

        out0=[None,Neck_forward_points,Head_forward_points,Forearm1_forward_points,Forearm2_forward_points,Bicep_forward_left_points,Bicep_forward_right_points,Body_forward_points,Skirt1_backward_points,Shin1_forward_points,Shin1_forward_points,Thigh_right_points,Thigh_left_points,Skirt1_forward_points,Belt_forward_points,Shoe1_forward_points,Shoe1_forward_points]
        transforms0=[[0,0,0],                                ##Canvas
                    [0,int(character_width/2-17),95],       ##Neck
                    [0,int(character_width/2-42),0],        ##Head
                    [-5,int(character_width/2-78+5),200],   ##Forearm1
                    [5,int(character_width/2+48-5),198],    ##Forearm2
                    [0,10+5,120],                           ##Bicep left
                    [0,int(character_width/2+30-5),120],    ##Bicep right
                    [0,int(character_width/2-50),120],      ##Body
                    [0,int(character_width/2-55),260],      ##Skirt in the back
                    [0,int(character_width/2-28),352],      ##Shin1
                    [0,int(character_width/2+2),352],       ##Shin2
                    [0,int(character_width/2-33),260],      ##Right thigh
                    [0,int(character_width/2+2),260],       ##Left thigh
                    [0,int(character_width/2-55),260],      ##Skirt in the front
                    [0,int(character_width/2-32),248],      ##Belt
                    [0,int(character_width/2),410],         ##Shoe1
                    [0,50,410]]                             ##Shoe2

        ##Draw Character_DOWN_step0
        Draw_step(out0,transforms0,character_region[0],character_hdc[0])
        out1=[None,Neck_forward_points,Head_forward_points,Forearm1_forward_points,Forearm2_forward_points,Bicep_forward_left_points,Bicep_forward_right_points,Body_forward_points,Skirt1_backward_points,Shoe3a_forward_points,Shin1_forward_points,Shin1_forward_points,Thigh_right_points,Thigh_left_points,Skirt1_forward_points,Belt_forward_points,Shoe2_forward_points]
        transforms1=[[0,0,0],                               ##Canvas
                    [0,int(character_width/2-17),95],       ##Neck
                    [0,int(character_width/2-42),0],        ##Head
                    [5,int(character_width/2-78+18),200],   ##Forearm1
                    [5,int(character_width/2+48-5),198],    ##Forearm2
                    [-7,10+5,120],                          ##Bicep left
                    [0,int(character_width/2+30-5),120],    ##Bicep right
                    [0,int(character_width/2-50),120],      ##Body
                    [0,int(character_width/2-55),260],      ##Skirt in the back
                    [0,52,410],                             ##Shoe2
                    [0,int(character_width/2-28),352],      ##Shin1
                    [0,int(character_width/2+2),352],       ##Shin2
                    [0,int(character_width/2-33),260],      ##Right thigh
                    [0,int(character_width/2+2),260],       ##Left thigh
                    [0,int(character_width/2-55),260],      ##Skirt in the front
                    [0,int(character_width/2-32),248],      ##Belt
                    [0,int(character_width/2),410]]         ##Shoe1
        transforms1_x=[[0,0,0],                             ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,13],                            ##Forearm1
                      [30,0,18],                            ##Forearm2
                      [40,0,33],                            ##Bicep left
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

        ##Draw Character_DOWN_step1
        Draw_step(out1,transforms1,character_region[1],character_hdc[1],transforms1_x)

        ##Draw Character_DOWN_step2
        Draw_step(out0,transforms0,character_region[2],character_hdc[2])
        out3=[None,Neck_forward_points,Head_forward_points,Forearm1_forward_points,Forearm2_forward_points,Bicep_forward_left_points,Bicep_forward_right_points,Body_forward_points,Skirt1_backward_points,Shoe3b_forward_points,Shin1_forward_points,Shin1_forward_points,Thigh_right_points,Thigh_left_points,Skirt1_forward_points,Belt_forward_points,Shoe2_forward_points]
        transforms3=[[0,0,0],                               ##Canvas
                    [0,int(character_width/2-17),95],       ##Neck
                    [0,int(character_width/2-42),0],        ##Head
                    [-5,int(character_width/2-78+5),200],   ##Forearm1
                    [-5,int(character_width/2+48-18),198],  ##Forearm2
                    [0,10+5,120],                           ##Bicep left
                    [7,int(character_width/2+30-5),120],    ##Bicep right
                    [0,int(character_width/2-50),120],      ##Body
                    [0,int(character_width/2-55),260],      ##Skirt in the back
                    [0,int(character_width/2)-4,410],       ##Shoe1
                    [0,int(character_width/2-28),352],      ##Shin1
                    [0,int(character_width/2+2),352],       ##Shin2
                    [0,int(character_width/2-33),260],      ##Right thigh
                    [0,int(character_width/2+2),260],       ##Left thigh
                    [0,int(character_width/2-55),260],      ##Skirt in the front
                    [0,int(character_width/2-32),248],      ##Belt
                    [0,50,410]]                             ##Shoe2
        transforms3_x=[[0,0,0],                             ##Canvas
                      [0,0,0],                              ##Neck
                      [0,0,0],                              ##Head
                      [30,0,18],                            ##Forearm1
                      [30,0,17],                            ##Forearm2
                      [30,0,18],                            ##Bicep left
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
        Draw_step(out3,transforms3,character_region[3],character_hdc[3],transforms3_x)

        ##RELEASE UNNEEDED HDCS##
        for i in range(4):
            for j in range(1,18):
                if len(character_hbmp[i])>j:
                    ##Release HDC##
                    windll.user32.ReleaseDC(hwnd,character_hdc[i][j])
        ##RETURN COMPILED IMAGES##
        return [[character_hdc[0][0],character_hdc[1][0],character_hdc[2][0],character_hdc[3][0]],
                [character_region[0][0],character_region[1][0],character_region[2][0],character_region[3][0]]]

