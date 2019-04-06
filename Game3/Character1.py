##PLAYER 1 OBEJCT##
import window_functions as wf
import window_structures as ws
import math
from ctypes import *
from ctypes.wintypes import *
from Character_Sprite_Main import *
from Character1_draw_down import Draw_DOWN
from Character1_draw_up import Draw_UP
from Character1_draw_right import Draw_RIGHT
from Character1_draw_left import Draw_LEFT
print("loading character1 libraries...")

class Character1_Sprite(Character_Sprite_Main):
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

    def Update_Position(self,shiftx,shifty,map_all):
        gridposition=RECT()
        [UL,UR,LL,LR]=self.Target_box()
        gridposition.left=int(UL.x/wf.tile_w)
        gridposition.top=int(UL.y/wf.tile_h)
        gridposition.right=int(LR.x/wf.tile_w)
        gridposition.bottom=int(LR.y/wf.tile_h)
        if self.Tool_selection!=wf.Empty_Hand:
            self.position=POINT(shiftx,shifty)
            ##Clear Previous position##
            gridposition_new=RECT()
            [UL,UR,LL,LR]=self.Target_box()
            gridposition_new.left=int(UL.x/wf.tile_w)
            gridposition_new.top=int(UL.y/wf.tile_h)
            gridposition_new.right=int(LR.x/wf.tile_w)
            gridposition_new.bottom=int(LR.y/wf.tile_h)
            
            ##Update tile position##
            self.tile_position=POINT(int(shiftx/wf.tile_w),int(shifty/wf.tile_h))
            ##Clear previous tiles##
            if map_all[gridposition.left][gridposition.top][6]==self.Character[0]:
                map_all[gridposition.left][gridposition.top]=map_all[gridposition.left][gridposition.top][0:6]+"--"
            if map_all[gridposition.left][gridposition.bottom][6]==self.Character[0]:
                map_all[gridposition.left][gridposition.bottom]=map_all[gridposition.left][gridposition.bottom][0:6]+"--"
            if map_all[gridposition.right][gridposition.top][6]==self.Character[0]:
                map_all[gridposition.right][gridposition.top]=map_all[gridposition.right][gridposition.top][0:6]+"--"
            if map_all[gridposition.right][gridposition.bottom][6]==self.Character[0]:
                map_all[gridposition.right][gridposition.bottom]=map_all[gridposition.right][gridposition.bottom][0:6]+"--"
            ##Update Map all##
            if map_all[gridposition_new.left][gridposition_new.top][6]=="-":
                map_all[gridposition_new.left][gridposition_new.top]=map_all[gridposition_new.left][gridposition_new.top][0:6]+self.Character
            if map_all[gridposition_new.left][gridposition_new.bottom][6]=="-":
                map_all[gridposition_new.left][gridposition_new.bottom]=map_all[gridposition_new.left][gridposition_new.bottom][0:6]+self.Character
            if map_all[gridposition_new.right][gridposition_new.top][6]=="-":
                map_all[gridposition_new.right][gridposition_new.top]=map_all[gridposition_new.right][gridposition_new.top][0:6]+self.Character
            if map_all[gridposition_new.right][gridposition_new.bottom][6]=="-":
                map_all[gridposition_new.right][gridposition_new.bottom]=map_all[gridposition_new.right][gridposition_new.bottom][0:6]+self.Character
            gridposition=gridposition_new
            
        ##Button_placement##
        shift=int((self.position.x%wf.tile_w)/wf.tile_w+.5)
        shift2=int((self.position.y%wf.tile_h)/wf.tile_h+.65)
        checktiles={"up":[gridposition.left-1+int(self.Step),gridposition.top-2],
                    "down":[gridposition.left-1+int(self.Step),gridposition.bottom+1],
                    "left":[gridposition.left-1,gridposition.top-2+int(self.Step)],
                    "right":[gridposition.right+1,gridposition.top-2+int(self.Step)]}
        checktiles2={"up":[gridposition.left+shift,gridposition.top],
                    "down":[gridposition.left+shift,gridposition.bottom],
                    "left":[gridposition.left-1+shift,gridposition.top],
                    "right":[gridposition.right+shift,gridposition.top]}

        #GGOOBPCC#
        if self.Tool_selection==wf.Empty_Hand:
            temp=map_all[checktiles[self.direction][0]][checktiles[self.direction][1]]
            if temp[5]=="-" and temp[2]=="-":
                map_all[checktiles[self.direction][0]][checktiles[self.direction][1]]=temp[0:4]+"B"+self.Character+temp[6:]

        else:
            temp=map_all[checktiles2[self.direction][0]][checktiles2[self.direction][1]]
            if temp[5]=="-" and temp[2]!="-":
                map_all[checktiles2[self.direction][0]][checktiles2[self.direction][1]]=temp[0:4]+"B"+self.Character+temp[6:]
        return 0
##    def Button_placement(self,map_all):
##        gridposition.left=int(UL.x/wf.tile_w+.5)
##        gridposition.top=int(UL.y/wf.tile_h+.5)
##        gridposition.right=int(LR.x/wf.tile_w+.5)
##        gridposition.bottom=int(LR.y/wf.tile_h+.5)
        
##        print(map_all[gridposition.right][gridposition.bottom])
##file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\"
##test=Character1_Sprite(None,file_path_main,None)
