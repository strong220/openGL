##THIS FUNCTION RETURNS ANIMATION IMAGES FOR RIGHT DIRECTION##
from window_structures import *
from window_functions import *
from ctypes import *
from ctypes.wintypes import *

def Draw_RIGHT(hdc_main,file_path_main,hwnd):
    ##Initialize hdcs and load images##
        [character1_right_file,Head1_right_file,Neck1_right_file,Body1_right_file,
         Forearm1_right_file,Bicep1_right_file,Belt1_right_file,Belt2_right_file,
         Belt3_right_file,Thigh1_right_file,Shin1_right_file,Skirt1_right_file,
         Shoe1_right_file,Skirt2_right_file,Skirt3_right_file,Forearm2_right_file,
         Head2_right_file]=["Face_right_1a.bmp","Head_right_2a.bmp","Neck_right_1a.bmp","Body_right_2a.bmp",
                            "Forearm_right_1a.bmp","Bicep_right_2a.bmp","Belt_right_1a.bmp","Belt_right_1b.bmp",
                            "Belt_right_1c.bmp","Thigh_right_1a.bmp","Shin_right_1a.bmp","Skirt_right_1a.bmp",
                            "Shoe_right_1a.bmp","Skirt_right_1b.bmp","Skirt_right_1c.bmp","Forearm_right_1b.bmp","Head_right_2b.bmp"]

        ##Define dictionaries for the character##
        character_files=[[character1_right_file,Neck1_right_file,Head1_right_file,Body1_right_file,Shin1_right_file,Thigh1_right_file,Skirt1_right_file,Belt1_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file],
                        [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt3_right_file,Belt3_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file,Shoe1_right_file],
                        [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt1_right_file,Belt1_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file,Shoe1_right_file],
                        [character1_right_file,Bicep1_right_file,Forearm2_right_file,Neck1_right_file,Head2_right_file,Body1_right_file,Shin1_right_file,Shin1_right_file,Thigh1_right_file,Thigh1_right_file,Skirt2_right_file,Belt2_right_file,Bicep1_right_file,Forearm1_right_file,Shoe1_right_file,Shoe1_right_file]]        
        character_hbmp=[[None,None,None,None,None,None,None,None,None,None,None],                        
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]                             
        character_hdc=[[None,None,None,None,None,None,None,None,None,None,None],                            
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                            [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        character_region=[[None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None],
                             [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]]
        for i in range(4):
            for j in range(16):
                if len(character_files[i])>j:
                    character_hbmp[i][j]=LoadImage(c_void_p(),LPCWSTR(file_path_main+character_files[i][j]),IMAGE_BITMAP,0,0,8192|LR_DEFAULTSIZE|LR_LOADFROMFILE)
                    ##Create HDC##
                    character_hdc[i][j]=windll.gdi32.CreateCompatibleDC(hdc_main)                  #Make hdc similar to the reference hdc
                    windll.gdi32.SetGraphicsMode(character_hdc[i][j],GM_ADVANCED)
                    windll.gdi32.SelectObject(character_hdc[i][j],character_hbmp[i][j])       #Copy image into hdc

        ##DEFINE INITIAL POINTS##
        Head_right_points=[(41,0),(34,0),(30,2),(24,4),(20,5),(17,6),(16,7),(13,10),(12,12),(9,17),(5,24),(4,28),(3,36),(3,47),(4,48),(4,51),(3,52),(7,59),(8,60),(9,62),(10,65),(11,67),(11,74),(8,81),(7,86),(7,101),(8,104),(11,108),(11,91),(13,91),(14,100),(14,108),(12,107),(11,108),(11,112),(12,115),(17,119),(18,118),(18,113),(21,116),(22,115),(23,112),(24,115),(27,118),(27,105),(28,105),(29,106),(29,109),(28,109),(28,114),(31,118),(33,117),(35,113),(36,113),(39,116),(40,115),(40,110),(43,110),(51,108),(60,99),(60,98),(63,95),(64,90),(65,90),(67,86),(68,82),(69,77),(70,72),(71,65),(73,65),(78,64),(78,61),(75,55),(74,53),(73,52),(70,46),(68,44),(68,40),(69,39),(68,38),(67,38),(67,35),(65,30),(67,28),(67,24),(64,17),(63,16),(58,10),(57,10),(53,6),(50,5),(50,4),(47,4),(45,3),(43,2)]
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
        
        out0=[None,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Thigh_right_points,Skirt_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points,Shoe_right_points]
        transforms0=[[0,0,0],                             ##Canvas
                    [0,int(character_width/2-10),100],   ##Neck
                    [0,int(character_width/2-77/2),0],   ##Head
                    [0,int(character_width/2-34),115],   ##Body
                    [0,int(character_width/2-12),345],   #Shin
                    [0,int(character_width/2-15),255],   ##Thigh
                    [0,int(character_width/2-41),262],   #Skirt
                    [0,int(character_width/2-24),245],   ##Belt
                    [0,int(character_width/2-15),115],   ##Bicep
                    [0,int(character_width/2-20),180],   ##Forearm
                    [0,int(character_width/2-13),410]]   ##Shoe

        ##Draw Character RIGHT_step0##
        Draw_step(out0,transforms0,character_region[0],character_hdc[0])
        out1=[None,Bicep_right_points,Forearm_right_points,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Shin_right_points,Thigh_right_points,Thigh_right_points,Skirt2_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points,Shoe_right_points,Shoe_right_points]
        transforms1=[[0,0,0],                                ##Canvas
                     [30,int(character_width/2-15),110],     ##Bicep_right
                     [10,int(30),170],                       ##Forearm
                     [0,int(character_width/2-10),100],      ##Neck
                     [0,int(character_width/2-77/2),0],      ##Head
                     [0,int(character_width/2-34),115],      ##Body
                     [-5,int(character_width/2+30),338],     #Shin1
                     [20,int(character_width/2-38),332],     #Shin2
                     [-25,int(character_width/2-13),263],    ##Thigh1
                     [18,int(character_width/2-13),250],     ##Thigh2
                     [0,int(character_width/2-46),262],      ##Skirt
                     [0,int(character_width/2-24),245],      ##Belt
                     [-25,int(character_width/2-15),125],    ##Bicep
                     [-35,int(character_width/2+10),190],    ##Forearm
                     [-5,int(character_width/2+36),410],     ##Shoe1
                     [10,int(character_width/2-62),400]]     ##Shoe2

        ##Draw_Character RIGHT_step1##        
        Draw_step(out1,transforms1,character_region[1],character_hdc[1])
        out2=[None,Bicep_right_points,Forearm_right_points,Neck_right_points,Head_right_points,Body_right_points,Shin_right_points,Shin_right_points,Thigh_right_points,Thigh_right_points,Skirt_right_points,Belt_right_points,Bicep_right_points,Forearm_right_points,Shoe_right_points,Shoe_right_points]
        transforms2=[[0,0,0],                            ##Canvas
                     [0,int(character_width/2-20),180],  ##Bicep right
                     [0,int(character_width/2-15),115],  ##Forearm
                     [0,int(character_width/2-10),100],  ##Neck
                     [0,int(character_width/2-77/2),0],  ##Head
                     [0,int(character_width/2-34),115],  ##Body
                     [0,int(character_width/2-12),345],  #Shin1
                     [0,int(character_width/2-12),345],  #Shin2
                     [0,int(character_width/2-15),255],  ##Thigh1
                     [0,int(character_width/2-15),255],  ##Thigh2
                     [0,int(character_width/2-41),262],  ##Skirt
                     [0,int(character_width/2-24),245],  ##Belt
                     [0,int(character_width/2-15),115],  ##Bicep
                     [0,int(character_width/2-20),180],  ##Forearm
                     [0,int(character_width/2-13),410],  ##Shoe1
                     [0,int(character_width/2-13),410]]  ##Shoe2

        ##Draw_Character RIGHT_step2##
        Draw_step(out2,transforms2,character_region[2],character_hdc[2])
        transforms3=[[0,0,0],                                ##Canvas
                     [-25,int(character_width/2-15),125],    ##Bicep right
                     [-35,int(character_width/2+10),190],    ##Forearm
                     [0,int(character_width/2-10),100],      ##Neck
                     [0,int(character_width/2-77/2),0],      ##Head
                     [0,int(character_width/2-34),115],      ##Body
                     [20,int(character_width/2-38),332],     #Shin1
                     [-5,int(character_width/2+30),338],     #Shin2
                     [18,int(character_width/2-13),250],     ##Thigh1
                     [-25,int(character_width/2-13),263],    ##Thigh2
                     [0,int(character_width/2-46),262],      ##Skirt
                     [0,int(character_width/2-24),245],      ##Belt
                     [30,int(character_width/2-15),110],     ##Bicep
                     [10,int(30),170],                       ##Forearm
                     [10,int(character_width/2-62),400],     ##Shoe1
                     [-5,int(character_width/2+36),410]]     ##Shoe2

        ##Draw_Character RIGHT_step3##
        Draw_step(out1,transforms3,character_region[3],character_hdc[3])
        
        ##RELEASE UNNEEDED HDCS##
        for i in range(4):
            for j in range(1,16):
                if len(character_hbmp[i])>j:
                    ##Release HDC##
                    windll.user32.ReleaseDC(hwnd,character_hdc[i][j])
        ##RETURN COMPILED IMAGES##
        return [[character_hdc[0][0],character_hdc[1][0],character_hdc[2][0],character_hdc[3][0]],
                [character_region[0][0],character_region[1][0],character_region[2][0],character_region[3][0]]]

