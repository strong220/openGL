##PLAYER 1 OBEJCT##
import window_functions as wf
import window_structures as ws
import math
from ctypes import *
from ctypes.wintypes import *
from Character_Sprite_Main import *
from Character2_draw_down import Draw_DOWN
from Character2_draw_up import Draw_UP
from Character2_draw_right import Draw_RIGHT
from Character2_draw_left import Draw_LEFT
print("loading character1 libraries...")

class Character2_Sprite(Character_Sprite_Main):
    def __init__(self,hdc_main,file_path_main,hwnd,name):
        ##BRING IN INHERITANCE CLASS##
        Character_Sprite_Main.__init__(self,hwnd)
        self.Character=name
        self.Tool_selection=None
        ##BRING IN IMAGES##
        print("loading character1 images...")
        [self.character_hdc[0],self.character_region[0]]=Draw_DOWN(hdc_main,file_path_main,hwnd)
        [self.character_hdc[1],self.character_region[1]]=Draw_UP(hdc_main,file_path_main,hwnd)
        [self.character_hdc[2],self.character_region[2]]=Draw_RIGHT(hdc_main,file_path_main,hwnd)
        [self.character_hdc[3],self.character_region[3]]=Draw_LEFT(hdc_main,file_path_main,hwnd)
        
##        print(map_all[gridposition.right][gridposition.bottom])
##file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\"
##test=Character1_Sprite(None,file_path_main,None)
