##THIS CLASS IS FOR INHERATENCE OF MAIN CHARACTER FUNCTIONS##
##THIS CLASS CONTAINS INFORMATION FOR PLAYER 1 CHARACTER##
import window_functions as wf
import math
from random import random
from ctypes import *
from ctypes.wintypes import *

class Character_Sprite_Main(object):
    def __init__(self,hwnd):
        ##Create Name
        self.Character=None
        self.Step=0
        self.Tool_selection=None
        self.build_object=1
        self.build_step=0
        self.build_objects={0:"Wall",1:"Wheat"}
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
        self.button_position=POINT(0,0)

        ##DEFINE RESOURCE DICTIONARY##
        self.resource={"Tree":0,"Wheat":0}

        ##STAMINA AND OUT OF BOUNDS##
        self.Stamina=100
        self.out_of_bounds=False

        ##DEFINE DICTIONARY FOR DAMAGE##
        self.Damage={"A":10,"C":20,"D":30}

    def Reference_Tile(self):
        #Reference Tile#
        return self.tile_position

    def Change_build_object(self):
        self.build_step=(self.build_step+.05)%2
        self.build_object=int(self.build_step)
        
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
    def Dice_roll(self,number_of_dice):
        total=0
        for i in range(number_of_dice):
            dice=int(random()*6)+1
            total=dice+total
        return total
    
    def Attack_Phase(self,map_all,target_point):
        ##If attack is successful change tile to being under attack by player##
        if self.Dice_roll(2)>4:
            temp=map_all[target_point.x][target_point.y]
            map_all[target_point.x][target_point.y]=temp[0:4]+"A"+self.Character[0]+temp[6:]
            return 1
        ##If attack is unsuccesful return 0
        return 0
    
    def Defense_Phase(self,map_all):
        ##GGOOBPCC##
        point=self.Target_box()[0]
        x=int(point.x/wf.tile_w)
        y=int(point.y/wf.tile_h)
        string=map_all[x][y]
        if string[4]!="B" and string[4]!="-" and string[5]!=self.Character[0]:
            ##Attempt Defense##
            if self.Dice_roll(1)<3:
                ##Remove Stamina##
                self.Stamina=self.Stamina-self.Damage[string[4]]
            ##If out of Stamina Player is put out of bounds##
            if self.Stamina<=0:
                ##Clear Previous tiles##
                gridposition=RECT()
                [UL,UR,LL,LR]=self.Target_box()
                gridposition.left=int(UL.x/wf.tile_w)
                gridposition.top=int(UL.y/wf.tile_h)
                gridposition.right=int(LR.x/wf.tile_w)
                gridposition.bottom=int(LR.y/wf.tile_h)
                if map_all[gridposition.left][gridposition.top][6]==self.Character[0]:
                    map_all[gridposition.left][gridposition.top]=map_all[gridposition.left][gridposition.top][0:6]+"--"
                if map_all[gridposition.left][gridposition.bottom][6]==self.Character[0]:
                    map_all[gridposition.left][gridposition.bottom]=map_all[gridposition.left][gridposition.bottom][0:6]+"--"
                if map_all[gridposition.right][gridposition.top][6]==self.Character[0]:
                    map_all[gridposition.right][gridposition.top]=map_all[gridposition.right][gridposition.top][0:6]+"--"
                if map_all[gridposition.right][gridposition.bottom][6]==self.Character[0]:
                    map_all[gridposition.right][gridposition.bottom]=map_all[gridposition.right][gridposition.bottom][0:6]+"--"
                self.out_of_bounds=True
                return 1
        return 0

    def Update_Position(self,shiftx,shifty,map_all,key_press=False,collision=POINT(-1,-1)):
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
            
        ##Button_placement or selection##
        ##Clear previous button##
        map_all[self.button_position.x][self.button_position.y]=map_all[self.button_position.x][self.button_position.y][:4]+"--"+map_all[self.button_position.x][self.button_position.y][6:]
        self.button_position=POINT(0,0)
        ##Define dictionaries for button placements
        shift=int((self.position.x%wf.tile_w)/wf.tile_w+.5)
        shift2=int((self.position.y%wf.tile_h)/wf.tile_h+.65)
        ##Dictionary for placing button for building##
        checktiles={"up":[gridposition.left-1+int(self.Step),gridposition.top-2],
                    "down":[gridposition.left-1+int(self.Step),gridposition.bottom+1],
                    "left":[gridposition.left-1,gridposition.top-2+int(self.Step)],
                    "right":[gridposition.right+1,gridposition.top-2+int(self.Step)]}
        
        #GGOOBPCC#
        ##Building selection##
        if self.Tool_selection==wf.Empty_Hand:
            ##Check to make sure selected tile is in map##
            if checktiles[self.direction][1]>=int(wf.map_h/200):
                checktiles[self.direction][1]=int(wf.map_h/200)-1
            temp=map_all[checktiles[self.direction][0]][checktiles[self.direction][1]]
            if temp[5]=="-" and temp[2]=="-":
                ##Update Map to show there is a button##
                map_all[checktiles[self.direction][0]][checktiles[self.direction][1]]=temp[0:4]+"B"+self.Character[0]+temp[6:]
                temp=map_all[checktiles[self.direction][0]][checktiles[self.direction][1]]
                ##Record button placement##
                self.button_position=POINT(checktiles[self.direction][0],checktiles[self.direction][1])
            if temp[4:6]=="B"+self.Character[0] and temp[2]!=0:
                ##Put in build request if key is pressed
                if key_press==True:
                    if self.build_objects[self.build_object]=="Wall" and self.resource["Tree"]>=1:
                        ##Define dictionary for marking walls##
                        wall_direction={"right":"0","left":"1","up":"2","down":"3"}
                        ##Record wall placement##
                        map_all[checktiles[self.direction][0]][checktiles[self.direction][1]]=temp[0:2]+"W"+wall_direction[self.direction]+"--"+temp[6:]
                        self.resource["Tree"]=self.resource["Tree"]-1
                    elif self.build_objects[self.build_object]=="Wheat" and self.resource["Wheat"]>=1 and temp[0:2]=="D1":
                        ##Record wall placement##
                        map_all[checktiles[self.direction][0]][checktiles[self.direction][1]]=temp[0:2]+"F-"+"--"+temp[6:]
                        self.resource["Wheat"]=self.resource["Wheat"]-1
        ##Selection of Adjacent objects##
        elif collision.x!=-1:
            temp=map_all[collision.x][collision.y]
            if temp[5]=="-" and (temp[2]!="-" or temp[6]!="-"):
                ##Update Map to show there is a button##
                map_all[collision.x][collision.y]=temp[0:4]+"B"+self.Character[0]+temp[6:]
                temp=map_all[collision.x][collision.y]
                ##Record button placement##
                self.button_position=POINT(collision.x,collision.y)
            if temp[4:6]=="B"+self.Character[0] and key_press==True:#and temp[2]!="-"
                ##Check for tree##
                if temp[2]=="T":
                    ##Cut down Tree##
                    map_all[collision.x][collision.y]=temp[0:2]+"----"+temp[6:]
                    self.resource["Tree"]=self.resource["Tree"]+1
                elif temp[2]=="W":
                    ##Cut down wall##
                    map_all[collision.x][collision.y]=temp[0:2]+"----"+temp[6:]
                    self.resource["Tree"]=self.resource["Tree"]+5
                elif temp[2]=="F":
                    ##Harvest Crops##
                    map_all[collision.x][collision.y]=temp[0:2]+"----"+temp[6:]
                    self.resource["Wheat"]=self.resource["Wheat"]+5
                else:
                    ##Attempt attack##
                    self.Attack_Phase(map_all,collision)
                    
        return self.resource

    def Move(self,inputs,map_all,objects,key_press=False):
        if self.out_of_bounds==True:
            return self.resource
        self.Defense_Phase(map_all)
        [down,up,left,right,change_build_object]=inputs
        [dy,dx]=[0,0]
        ##Update build object##
        if change_build_object:
            self.Change_build_object()

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
        collision_point=POINT(-1,-1)#POINT(self.tile_position.x,self.tile_position.y)
        for i in range(gridposition.left,gridposition.right+1):
            for j in range(gridposition.top-1,gridposition.bottom+1):
                if j>=0:
                ##IF THE PLAYER IS IN THE TILE CHECK FOR COLLISION##
                ##map strings are GGOOBPCC check for objects                        
                    for k in range(len(objects)):
                        collision=False
                        check_y_temp=check_y
                        check_x_temp=check_x
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
                                    collision=True
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                            POINT(ULt.x,UL.y),POINT(LLt.x,LL.y)):
                                    check_x=False
                                    check_temp=False
                                    collision=True
                            ##Check for intersection of the top and bottom of collision box and the right side of player
                            elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,URt,LRt):
                                if wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                          POINT(UR.x,URt.y),POINT(LR.x,LRt.y)):
                                    check_y=False
                                    check_temp=False
                                    collision=True
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                            POINT(URt.x,UR.y),POINT(LRt.x,LR.y)):
                                    check_x=False
                                    check_temp=False
                                    collision=True

                            ##Check for intersection of the left and right side of the collision box and the top side of player
##                            if check_temp==True or check_temp==False:
                            if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,ULt,URt):
                                if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                          POINT(ULt.x,UL.y),POINT(URt.x,UR.y)):
                                    check_x=False
                                    collision=True
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                            POINT(UL.x,ULt.y),POINT(UR.x,URt.y)):
                                    check_y=False
                                    collision=True
                            ##Check for intersection of the left and right side of the collision box and the bottom side of player
                            elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,LLt,LRt):
                                if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                          POINT(LLt.x,LL.y),POINT(LRt.x,LR.y)):
                                    check_x=False
                                    collision=True
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                            POINT(LL.x,LLt.y),POINT(LR.x,LRt.y)):
                                    check_y=False
                                    collision=True
                            if collision==True:
                                collision_point.x=int(rcCollisionULt.x/wf.tile_w)
                                collision_point.y=int(rcCollisionULt.y/wf.tile_h)
                                if objects[k][1]=="F":
                                    check_y=check_y_temp
                                    check_x=check_x_temp


        ##########################
        ##UPDATE PLAYER POSITION##
        ##########################

        ##PLAYER1##
        if check_x==False or (new_position.x<0+wf.shiftx or (new_position.x+wf.character_width)>(wf.map_w-wf.shiftx)):
                new_position.x=self.position.x
        if check_y==False or (new_position.y<0+wf.shifty or (new_position.y+wf.character_height)>wf.map_h-wf.shifty):
                new_position.y=self.position.y
                
        return self.Update_Position(new_position.x,new_position.y,map_all,key_press,collision_point)

    def Target_Box_Shifted(self,shiftx,shifty):
        shifted_tboxUL=POINT(self.tboxUL.x+shiftx,self.tboxUL.y+shifty)
        shifted_tboxUR=POINT(self.tboxUR.x+shiftx,self.tboxUR.y+shifty)
        shifted_tboxLL=POINT(self.tboxLL.x+shiftx,self.tboxLL.y+shifty)
        shifted_tboxLR=POINT(self.tboxLR.x+shiftx,self.tboxLR.y+shifty)
        return [shifted_tboxUL,shifted_tboxUR,shifted_tboxLL,shifted_tboxLR]
    
    def Target_box(self,changex=None,changey=None,Type=None):
        if self.out_of_bounds==False:
            shiftx=self.position.x
            shifty=self.position.y
            shifted_tboxUL=POINT(self.tboxUL.x+shiftx,self.tboxUL.y+shifty)
            shifted_tboxUR=POINT(self.tboxUR.x+shiftx,self.tboxUR.y+shifty)
            shifted_tboxLL=POINT(self.tboxLL.x+shiftx,self.tboxLL.y+shifty)
            shifted_tboxLR=POINT(self.tboxLR.x+shiftx,self.tboxLR.y+shifty)
            return [shifted_tboxUL,shifted_tboxUR,shifted_tboxLL,shifted_tboxLR]
        return [POINT(0,0),POINT(0,0),POINT(0,0),POINT(0,0)]

    def Draw_Character(self,hdc,reference_tile):
        if self.out_of_bounds==False:
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
        

