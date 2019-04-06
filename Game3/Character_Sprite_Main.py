##THIS CLASS IS FOR INHERATENCE OF MAIN CHARACTER FUNCTIONS##
##THIS CLASS CONTAINS INFORMATION FOR PLAYER 1 CHARACTER##
import window_functions as wf
import window_structures as ws
import math
import wm_create                 ##This allows us to get all the types
from ctypes import *
from ctypes.wintypes import *

class Character_Sprite_Main(object):
    def __init__(self,hwnd):
        ##Create Name
        self.Character=None
        self.Step=0
        ##Save hwnd##
        self.HWND=hwnd
        ##Define dictionaries for the character##
        self.dict_index_to_character={"down":0,"up":1,"right":2,"left":3}
        self.character_hbmp=[[None,None,None,None],     #DOWN
                             [None,None,None,None],     #UP
                             [None,None,None,None],     #LEFT
                             [None,None,None,None]]     #RIGHT
        self.character_hdc=[[None,None,None,None],      #DOWN
                             [None,None,None,None],     #UP
                             [None,None,None,None],     #LEFT
                             [None,None,None,None]]     #RIGHT
        self.character_region=[[None,None,None,None],   #DOWN
                             [None,None,None,None],     #UP
                             [None,None,None,None],     #RIGHT
                             [None,None,None,None]]     #LEFT

        ##DEFINE THE TARGET BOX##
        self.tboxUL=POINT(0,wf.character_height-100)
        self.tboxUR=POINT(wf.character_width,wf.character_height-100)
        self.tboxLL=POINT(0,wf.character_height)
        self.tboxLR=POINT(wf.character_width,wf.character_height)
        
        ##DEFINE REFERNCE POSITIONS##
        self.position=POINT(wf.shiftx+100,wf.shifty+100)
        self.tile_position=POINT(int(self.position.x/wf.tile_w),int(self.position.y/wf.tile_h))
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
            self.Step=(self.Step+.11)%4
        else:
            self.step=0
        return

    def Update_Position(self,shiftx,shifty,Map=None):
        self.position=POINT(shiftx,shifty)
        self.tile_position=POINT(int(shiftx/wf.tile_w),int(shifty/wf.tile_h))
        return 0

    def Move(self,inputs,map_all,objects):
        [down,up,left,right]=inputs
        [dy,dx]=[0,0]
        ##Update Direction##
        temp_direction=self.direction
        if down:
            temp_direction="down"
            dy=10
        if up:
            temp_direction="up"
            dy=-10
        if left:
            temp_direction="left"
            dx=-10
        if right:
            temp_direction="right"
            dx=10
        ##Save temp new position##
        new_position=POINT(self.position.x+dx,self.position.y+dy)
        ##Update Step##
        if dx!=0 or dy!=0:
            self.Update_direction(temp_direction)
            self.Animate_step(True)
        else:
            self.step=0
        gridposition=RECT()             ##Use to determine what tiles are being viewed on the map##
        ##Check for object collisions in x or y directions##
        check_x=True
        check_y=True
        
        ##Convert player rectangle into grid position
        y_shift=-300
        [UL,UR,LL,LR]=self.Target_box()
        [ULt,URt,LLt,LRt]=self.Target_Box_Shifted(new_position.x,new_position.y)
        gridposition.left=int(ULt.x/wf.tile_w)
        gridposition.top=int(ULt.y/wf.tile_h)
        gridposition.right=int(LRt.x/wf.tile_w)
        gridposition.bottom=int(LRt.y/wf.tile_h)
        rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=POINT(),POINT(),POINT(),POINT()
        ##LOOK AT TILES COVERED BY PLAYER CHARACTER AND ALL ADJACENT TILES##
        check_temp=True
        for i in range(gridposition.left,gridposition.right+1):
            for j in range(gridposition.top-1,gridposition.bottom+1):
                if j>=0:
                ##IF THE PLAYER IS IN THE TILE CHECK FOR COLLISION##
                ##map strings are GGOOBPCC check for objects                        
                    for k in range(len(objects)):
##                        if map_all[i][j][2]==objects[k][1] or map_all[i][j][6:8]==objects[k][1] and objects[k][1]!=self.Character:
                        if map_all[i][j][2]==objects[k][1] or (map_all[i][j][6:8]!="--"  and objects[k][1][0]=="P") and objects[k][1][1:]!=self.Character:
                            if map_all[i][j][3]!="-":
                                rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=objects[k][0].Target_box(i*wf.tile_w,j*wf.tile_h,int(map_all[i][j][3]))
                            else:
                                rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=objects[k][0].Target_box(i*wf.tile_w,j*wf.tile_h)
                            ##CHECK X and Y direction for collision##
                            ##Check for intersection of the top and bottom of collision box and the left side of player##        
                            if wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,ULt,LLt):
                                if wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                          POINT(UL.x,ULt.y),POINT(LL.x,LLt.y)):
                                    check_y=False
                                    check_temp=False
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                            POINT(ULt.x,UL.y),POINT(LLt.x,LL.y)):
                                    check_x=False
                                    check_temp=False
                            ##Check for intersection of the top and bottom of collision box and the right side of player
                            elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,URt,LRt):
                                if wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                          POINT(UR.x,URt.y),POINT(LR.x,LRt.y)):
                                    check_y=False
                                    check_temp=False
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                            POINT(URt.x,UR.y),POINT(LRt.x,LR.y)):
                                    check_x=False
                                    check_temp=False

                            ##Check for intersection of the left and right side of the collision box and the top side of player
                            if check_temp==True:
                                if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,ULt,URt):
                                    if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                              POINT(ULt.x,UL.y),POINT(URt.x,UR.y)):
                                        check_x=False
                                    elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                                POINT(UL.x,ULt.y),POINT(UR.x,URt.y)):
                                        check_y=False
                                ##Check for intersection of the left and right side of the collision box and the bottom side of player
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,LLt,LRt):
                                    if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                              POINT(LLt.x,LL.y),POINT(LRt.x,LR.y)):
                                        check_x=False
                                    elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                                POINT(LL.x,LLt.y),POINT(LR.x,LRt.y)):
                                        check_y=False


        ##########################
        ##UPDATE PLAYER POSITION##
        ##########################

        ##PLAYER1##
        if check_x==False or (new_position.x<0+wf.shiftx or (new_position.x+wf.character_width)>(wf.map_w-wf.shiftx)):
                new_position.x=self.position.x
        if check_y==False or (new_position.y<0+wf.shifty or (new_position.y+wf.character_height)>wf.map_h-wf.shifty):
                new_position.y=self.position.y
                
        self.Update_Position(new_position.x,new_position.y,map_all)

    def Target_Box_Shifted(self,shiftx,shifty):
        shifted_tboxUL=POINT(self.tboxUL.x+shiftx,self.tboxUL.y+shifty)
        shifted_tboxUR=POINT(self.tboxUR.x+shiftx,self.tboxUR.y+shifty)
        shifted_tboxLL=POINT(self.tboxLL.x+shiftx,self.tboxLL.y+shifty)
        shifted_tboxLR=POINT(self.tboxLR.x+shiftx,self.tboxLR.y+shifty)
        return [shifted_tboxUL,shifted_tboxUR,shifted_tboxLL,shifted_tboxLR]
    
    def Target_box(self,changex=None,changey=None,Type=None):
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
        ##Find the desired image
        i=self.dict_index_to_character[self.direction]        

        ##COPY OBJECT ONTO TILE##
        windll.gdi32.OffsetRgn(self.character_region[i][int(self.step)],                                 ##Shift the region to draw the character
                               position_new)
        windll.gdi32.SelectClipRgn(hdc,self.character_region[i][int(self.step)])                         ##Select the shifted region for copying the image
        windll.gdi32.BitBlt(hdc,position_new,wf.character_width+50,                                      ##Add Character to Background
                            wf.character_height,self.character_hdc[i][int(self.step)],
                            0,0,wf.SRCCOPY)
        ##Reset class object and hdc##
        windll.gdi32.SelectClipRgn(hdc,None)                                                             ##Remove clipping region
        windll.gdi32.OffsetRgn(self.character_region[i][int(self.step)],-position_new.x,                 #Return Region to original positoin
                                -position_new.y)

    def __del__(self):
        ##RELEASE ALL HANDLES##
        ##RELEASE HDCS##
        for i in range(4):
            for j in range(4):
                ##Release HDC##
                windll.user32.ReleaseDC(self.HWND,self.character_hdc[i][j])                  #Make hdc similar to the reference hdc
        

