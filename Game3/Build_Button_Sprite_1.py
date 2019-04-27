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
        ##Load tokens##
        build_wall_file="Wall_build_token.bmp"
        wheat_build_file="Wheat_build_token.bmp"
        self.token_file=[build_wall_file,wheat_build_file]
        self.token_hbmp=[None,None]
        self.token_hdc=[None,None]
        for i in range(2):
            self.token_hbmp[i]=wf.LoadImage(c_void_p(),LPCWSTR(file_path+self.token_file[i]),    #Load image
                                           wf.IMAGE_BITMAP,0,0,
                                           8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
            ##LOAD HDC##
            self.token_hdc[i]=windll.gdi32.CreateCompatibleDC(hdc_main)
            ##COPY IMAGES INTO HDC##
            windll.gdi32.SelectObject(self.token_hdc[i],self.token_hbmp[i])
        
        ##Define dictionaries##
        self.direction={"right":wf.r_build,"left":wf.l_build,"up":wf.u_build,"down":wf.d_build}          ##Define dictionary for button placement when building
        self.build={"Wall":0,"Wheat":1}                                                                  ##Identify the index for the token
    def Target_box(self,x_shit,y_shift,number=None):
        ##Return nothing##
        return [POINT(),POINT(),POINT(),POINT()]
    def Draw(self,hdc,object_string,x_shift,y_shift,player):
        text=["E","9","-"]
        ##GGOOBPCC##
        if player.Tool_selection==wf.Empty_Hand:
            if object_string[2]=="-" and object_string[4:6]=="B"+player.Character[0]:
                ##Update position for button depending on where player is facing
                position=POINT(self.direction[player.direction].x+x_shift,
                               self.direction[player.direction].y+y_shift)
                self.button.Draw_Button(hdc,position.x,position.y,text[int(player.Character[0])])
                ##Draw token depending on selection##
                position.x=position.x+wf.button_w
                windll.gdi32.BitBlt(hdc,position,50,50,self.token_hdc[self.build[player.build_objects[player.build_object]]],0,0,wf.SRCCOPY)               ##Add button to background            
                return 0
        return -1
            
