##THIS CLASS IS FOR THE SMALL TREE SPRITE##
import window_functions as wf
import window_structures as ws
from Button_Sprite import Button
from ctypes import *
from ctypes.wintypes import *

class Barrel_Sprite_1:
    def __init__(self,hdc_main,file_path):
        ##Initialize hdc, and load image##
        barrel_file="Wheat_Barrel.bmp"
        self.hbmp=wf.LoadImage(c_void_p(),LPCWSTR(file_path+barrel_file),    #Load image
                                    wf.IMAGE_BITMAP,0,0,
                                    8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        
        self.hdc=windll.gdi32.CreateCompatibleDC(hdc_main)                 #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(self.hdc,self.hbmp)                       #Copy image into hdc
        self.button=Button(hdc_main,file_path,"red")                              #Load Button
        self.out_of_bounds=False                 ##Change to False when finished
        self.Amount=0
        self.Character="W"
        ##LOAD REGIONS##
        points=[(102,155),(17,155),(15,150),(13,148),(13,147),(11,142),(10,141),(10,140),
                 (8,135),(8,134),(7,133),(7,130),(5,130),(4,127),(3,124),(2,118),(3,118),
                 (2,108),(1,107),(0,90),(0,82),(1,69),(2,61),(3,56),(3,54),(2,54),(3,49),
                 (4,45),(5,42),(7,42),(7,40),(8,37),(9,35),(10,32),(11,30),(12,28),(13,25),
                 (14,23),(15,21),(16,19),(103,19),(104,21),(105,23),(106,25),(107,28),(108,30),
                 (109,32),(110,35),(111,38),(112,40),(112,42),(114,42),(115,45),(116,48),(117,52),
                 (117,54),(116,54),(117,62),(118,70),(119,80),(119,94),(118,104),(117,112),(116,118),
                 (117,118),(116,124),(115,127),(114,130),(112,130),(112,132),(111,135),(110,138),
                 (109,140),(108,143),(107,145),(106,147),(105,150),(104,151),(103,152)]
            
        ##TRANSLATE POINTS INTO REGION##
        Rgn=POINT*len(points)
        temp=[]
        for i in range(len(points)):
            temp.append(POINT(points[i][0],points[i][1]))
        out=Rgn(*temp)
        
        self.Region=wf.CreatePolygonRgn(out,len(out),wf.WINDING)

        ##DEFINE THE TARGET BOX##
        self.tboxUL=POINT(50,80)
        self.tboxUR=POINT(wf.tile_w-50,80)
        self.tboxLL=POINT(50,wf.tile_h-20)
        self.tboxLR=POINT(wf.tile_w-50,wf.tile_h-20)

        ##DEFINE REFERENCE POSITION##
        self.position=POINT(int(wf.tile_w/2-wf.tree1_w/2)+600,wf.tile_h-wf.tree1_h+900)
        self.tile_position=(int(self.position.x/wf.tile_w),int(self.position.y/wf.tile_h))                                        ##Define tile position
    def Update_Position(self,shiftx,shifty):
        self.position=POINT(shiftx,shifty)
        self.tile_position=(int(self.position.x/wf.tile_w),int(self.position.y/wf.tile_h))                                        ##Define tile position
        return 0

    def Fill_barrel(self,Player,amount):
        ##Remove wheat from player resource and add to the barrel##
        if Player.resource["Wheat"]>=amount:
            self.Amount=self.Amount+amount
            Player.resource["Wheat"]=Player.resource["Wheat"]-amount
            return 0
        ##If attempting to add more resources than the player has
        return -1

    def Empty_barrel(self,Player,amount):
        ##Remove wheat from player resource and add to the barrel##
        if self.Amount>=amount:
            self.Amount=self.Amount-amount
            Player.resource["Wheat"]=Player.resource["Wheat"]+amount
            return 0
        ##If attempting to remove more resources than are in the barrel
        return -1

    def Target_box_Shifted(self,x_shift,y_shift,number=None):
        ##Return the shifted target box
        shiftedboxUL=POINT(self.tboxUL.x+x_shift,self.tboxUL.y+y_shift)
        shiftedboxUR=POINT(self.tboxUR.x+x_shift,self.tboxUR.y+y_shift)
        shiftedboxLL=POINT(self.tboxLL.x+x_shift,self.tboxLL.y+y_shift)
        shiftedboxLR=POINT(self.tboxLR.x+x_shift,self.tboxLR.y+y_shift)
        return [shiftedboxUL,shiftedboxUR,shiftedboxLL,shiftedboxLR]

    def Target_box(self,changex=None,changey=None,Type=None):
        if self.out_of_bounds==True:
            return [POINT(0,0),POINT(0,0),POINT(0,0),POINT(0,0)]
        ##Return the shifted target box
        x_shift=self.position.x
        y_shift=self.position.y
        shiftedboxUL=POINT(self.tboxUL.x+x_shift,self.tboxUL.y+y_shift)
        shiftedboxUR=POINT(self.tboxUR.x+x_shift,self.tboxUR.y+y_shift)
        shiftedboxLL=POINT(self.tboxLL.x+x_shift,self.tboxLL.y+y_shift)
        shiftedboxLR=POINT(self.tboxLR.x+x_shift,self.tboxLR.y+y_shift)
        return [shiftedboxUL,shiftedboxUR,shiftedboxLL,shiftedboxLR]

    def Draw(self,hdc,object_string,reference_tile,Player):
        if self.out_of_bounds==True:
            return -1
        text=["E","9"]
        ##Copy Object onto tile
        position_new=POINT(self.position.x-reference_tile.x*wf.tile_w,
                           self.position.y-reference_tile.y*wf.tile_h)
        windll.gdi32.OffsetRgn(self.Region,position_new)                                                    ##Shift the region to draw the barrel
        windll.gdi32.SelectClipRgn(hdc,self.Region)                                                     ##Select the shifted region for copying the barrel
        windll.gdi32.BitBlt(hdc,position_new,wf.barrel1_w,wf.barrel1_h,self.hdc,0,0,wf.SRCCOPY)             ##Add tree to background
        ##Reset class object and hdc
        windll.gdi32.SelectClipRgn(hdc,None)                                                            ##Remove Clipping Region
        windll.gdi32.OffsetRgn(self.Region,-position_new.x,-position_new.y)                                     ##Return the region back
        ##CHECK TO SEE IF BUTTON NEEDS TO BE DRAWN##
        if object_string[4]=="B" and Player.Tool_selection==wf.Axe and Player.Character[0]==object_string[5]:
            ##Position the button##
            position_new=POINT()
            position_new.x=position_new.x+int(wf.tile_w/2)
            position_new.y=position_new.y+wf.tile_h-40
            ##DRAW BUTTON##
            self.button.Draw_Button(hdc,position_new.x,position_new.y,text[int(Player.Character[0])])
            ##Return 1 if button was drawn
            return 1
        else:
            ##Return 0 if object was drawn
            return 0
            
