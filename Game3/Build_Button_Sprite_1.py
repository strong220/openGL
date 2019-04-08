##THIS CLASS IS FOR THE BUILD BUTTON SPRITE##
import window_functions as wf
import window_structures as ws
from Button_Sprite import Button
from ctypes import *
from ctypes.wintypes import *
import Character_Sprite_Main

class Build_Button_Sprite_1:
    def __init__(self,hdc_main,file_path):
        ##Load button##
        self.button=Button(hdc_main,file_path,"purple")
        ##Define dictionaries##
        self.direction={"right":wf.r_build,"left":wf.l_build,"up":wf.u_build,"down":wf.d_build}          ##Define dictionary for button placement when building
    def Target_box(self,x_shit,y_shift,number=None):
        ##Return nothing##
        return[0,0,0,0]
    def Draw(self,hdc,object_string,x_shift,y_shift,player):
        text=["E","9","-"]
        ##GGOOBPCC##
        if player.Tool_selection==wf.Empty_Hand:
            if object_string[2]=="-" and object_string[4:6]=="B"+player.Character[0]:
                ##Update position for button depending on where player is facing
                position=POINT(self.direction[player.direction].x+x_shift,
                               self.direction[player.direction].y+y_shift)
                self.button.Draw_Button(hdc,position.x,position.y,text[int(player.Character[0])])
                return 0
        return -1
            
