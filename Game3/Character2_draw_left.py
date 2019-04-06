##THIS FUNCTION RETURNS ANIMATION IMAGES FOR LEFT DIRECTION##
from window_structures import *
from window_functions import *
from ctypes import *
from ctypes.wintypes import *

def Draw_LEFT(hdc_main,file_path_main,hwnd):
    ##Initialize hdcs and load images##
        [character1_left_file,Head1_left_file,Neck1_left_file,Body1_left_file,
         Forearm1_left_file,Bicep1_left_file,Belt1_left_file,Belt2_left_file,
         Belt3_left_file,Thigh1_left_file,Shin1_left_file,Skirt1_left_file,
         Shoe1_left_file,Skirt2_left_file,Skirt3_left_file,Forearm2_left_file,
         Head2_left_file]=["Face_left_1a.bmp","Head_left_2a.bmp","Neck_left_1a.bmp","Body_left_2a.bmp",
                           "Forearm_left_1a.bmp","Bicep_left_2a.bmp","Belt_left_1a.bmp","Belt_left_1b.bmp",
                           "Belt_left_1c.bmp","Thigh_left_1a.bmp","Shin_left_1a.bmp","Skirt_left_1a.bmp",
                           "Shoe_left_1a.bmp","Skirt_left_1b.bmp","Skirt_left_1c.bmp","Forearm_left_1b.bmp","Head_left_2b.bmp"]

        ##Define dictionaries for the character##
        character_files=[[character1_left_file,Neck1_left_file,Head1_left_file,Body1_left_file,Shin1_left_file,Thigh1_left_file,Skirt1_left_file,Belt1_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file],
                        [character1_left_file,Bicep1_left_file,Forearm2_left_file,Neck1_left_file,Head2_left_file,Body1_left_file,Shin1_left_file,Shin1_left_file,Thigh1_left_file,Thigh1_left_file,Skirt3_left_file,Belt3_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file,Shoe1_left_file],
                        [character1_left_file,Bicep1_left_file,Forearm2_left_file,Neck1_left_file,Head2_left_file,Body1_left_file,Shin1_left_file,Shin1_left_file,Thigh1_left_file,Thigh1_left_file,Skirt1_left_file,Belt1_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file,Shoe1_left_file],
                        [character1_left_file,Bicep1_left_file,Forearm2_left_file,Neck1_left_file,Head2_left_file,Body1_left_file,Shin1_left_file,Shin1_left_file,Thigh1_left_file,Thigh1_left_file,Skirt2_left_file,Belt2_left_file,Bicep1_left_file,Forearm1_left_file,Shoe1_left_file,Shoe1_left_file]]
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
        Head_left_points=[(37,0),(44,0),(48,2),(54,4),(58,5),(61,6),(62,7),(65,10),(66,12),(69,17),(73,24),(74,28),(75,36),(75,47),(74,48),(74,51),(75,52),(71,59),(70,60),(69,62),(68,65),(67,67),(67,74),(70,81),(71,86),(71,101),(70,104),(67,108),(67,91),(65,91),(64,100),(64,108),(66,107),(67,108),(67,112),(66,115),(61,119),(60,118),(60,113),(57,116),(56,115),(55,112),(54,115),(51,118),(51,105),(50,105),(49,106),(49,109),(50,109),(50,114),(47,118),(45,117),(43,113),(42,113),(39,116),(38,115),(38,110),(35,110),(27,108),(18,99),(18,98),(15,95),(14,90),(13,90),(11,86),(10,82),(9,77),(8,72),(7,65),(5,65),(0,64),(0,61),(3,55),(4,53),(5,52),(8,46),(10,44),(10,40),(9,39),(10,38),(11,38),(11,35),(13,30),(11,28),(11,24),(14,17),(15,16),(20,10),(21,10),(25,6),(28,5),(28,4),(31,4),(33,3),(35,2)]
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
        out0=[None,Neck_left_points,Head_left_points,Body_left_points,Shin_left_points,Thigh_left_points,Skirt_left_points,Belt_left_points,Bicep_left_points,Forearm_left_points,Shoe_left_points]
        transforms0=[[0,0,0],                               ##Canvas
                    [0,int(character_width/2-12+13),100],   ##Neck
                    [0,int(character_width/2-77/2+13),0],   ##Head
                    [0,int(character_width/2-36+13),115],   ##Body
                    [0,int(character_width/2-17+13),345],   #Shin
                    [0,int(character_width/2-19+13),255],   ##Thigh
                    [0,int(character_width/2-49+13),262],   #Skirt
                    [0,int(character_width/2-31+13),245],   ##Belt
                    [0,int(character_width/2-16+13),115],   ##Bicep
                    [0,int(character_width/2-25+13),180],   ##Forearm
                    [0,int(character_width/2-54+13),410]]   ##Shoe

        ##Draw_Character LEFT_step0##
        Draw_step(out0,transforms0,character_region[0],character_hdc[0])
        out1=[None,Bicep_left_points,Forearm_left_points,Neck_left_points,Head_left_points,Body_left_points,Shin_left_points,Shin_left_points,Thigh_left_points,Thigh_left_points,Skirt2_left_points,Belt_left_points,Bicep_left_points,Forearm_left_points,Shoe_left_points,Shoe_left_points]
        transforms1=[[0,0,0],                                   ##Canvas
                     [-30,int(character_width/2-12+13),127],    ##Bicep_right
                     [-10,int(character_width/2+12+13),177],    ##Forearm
                     [0,int(character_width/2-12+13),100],      ##Neck
                     [0,int(character_width/2-77/2+13),0],      ##Head
                     [0,int(character_width/2-36+13),115],      ##Body
                     [5,int(character_width/2-55+13),336],      ##Shin1
                     [-20,int(character_width/2+8+13),340],     ##Shin2
                     [25,int(character_width/2-15+13),253],     ##Thigh1
                     [-18,int(character_width/2-18+13),262],    ##Thigh2
                     [0,int(character_width/2-55+13),262],      ##Skirt
                     [0,int(character_width/2-31+13),245],      ##Belt
                     [25,int(character_width/2-15+13),112],     ##Bicep
                     [35,int(character_width/2-48+13),165],     ##Forearm
                     [5,int(-13+13),405],                       ##Shoe1
                     [-10,int(character_width/2-5+13),410]]     ##Shoe2

        ##Draw_Character LEFT_step1##       
        Draw_step(out1,transforms1,character_region[1],character_hdc[1])
        out2=[None,Bicep_left_points,Forearm_left_points,Neck_left_points,Head_left_points,Body_left_points,Shin_left_points,Shin_left_points,Thigh_left_points,Thigh_left_points,Skirt_left_points,Belt_left_points,Bicep_left_points,Forearm_left_points,Shoe_left_points,Shoe_left_points]
        transforms2=[[0,0,0],                                ##Canvas
                     [0,int(character_width/2-16+13),115],   ##Bicep
                     [0,int(character_width/2-25+13),180],   ##Forearm
                     [0,int(character_width/2-12+13),100],   ##Neck
                     [0,int(character_width/2-77/2+13),0],   ##Head
                     [0,int(character_width/2-36+13),115],   ##Body
                     [0,int(character_width/2-17+13),345],   #Shin1
                     [0,int(character_width/2-17+13),345],   #Shin2
                     [0,int(character_width/2-19+13),255],   ##Thigh1
                     [0,int(character_width/2-19+13),255],   ##Thigh2
                     [0,int(character_width/2-49+13),262],   #Skirt
                     [0,int(character_width/2-31+13),245],   ##Belt
                     [0,int(character_width/2-16+13),115],   ##Bicep
                     [0,int(character_width/2-25+13),180],   ##Forearm
                     [0,int(character_width/2-54+13),410],   ##Shoe1
                     [0,int(character_width/2-54+13),410]]   ##Shoe2

        ##Draw_Character LEFT_step2##
        Draw_step(out2,transforms2,character_region[2],character_hdc[2])
        transforms3=[[0,0,0],                                ##Canvas
                     [25,int(character_width/2-15+13),112],  ##Bicep
                     [35,int(character_width/2-48+13),165],  ##Forearm
                     [0,int(character_width/2-12+13),100],   ##Neck
                     [0,int(character_width/2-77/2+13),0],   ##Head
                     [0,int(character_width/2-36+13),115],   ##Body
                     [-20,int(character_width/2+8+13),340],  #Shin1
                     [5,int(character_width/2-55+13),336],   #Shin2
                     [-18,int(character_width/2-18+13),262], ##Thigh1
                     [25,int(character_width/2-15+13),253],  ##Thigh2
                     [0,int(character_width/2-55+13),262],   ##Skirt
                     [0,int(character_width/2-31+13),245],   ##Belt
                     [-30,int(character_width/2-12+13),127], ##Bicep_right
                     [-10,int(character_width/2+12+13),177], ##Forearm
                     [-10,int(character_width/2-5+13),410],  ##Shoe1
                     [5,int(-13+13),405]]                    ##Shoe2

        ##Draw_Character LEFT_step3##
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

