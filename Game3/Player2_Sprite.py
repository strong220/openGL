##THIS CLASS CONTAINS INFORMATION FOR PLAYER 2 CHARACTER##
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *

class Player2_Sprite:
    def __init__(self,hdc_main,file_path_main):
        ##Initialize hdcs and load images##
        character1_down_file="Face_forward_2a.bmp"
        character1_up_file="Face_backward_2a.bmp"
        character1_right_file="Face_right_2a.bmp"
        character1_left_file="Face_left_2a.bmp"
        ##Define dictionaries for the character##
        self.dict_character_to_index={0:"character1_down",1:"character1_up",2:"character1_right",3:"character1_left"}
        self.dict_index_to_character={"character1_down":0,"character1_up":1,"character1_right":2,"character1_left":3}
        self.character_files=[character1_down_file,character1_up_file,character1_right_file,character1_left_file]
        self.character_hbmp=[None,None,None,None]
        self.character_hdc=[None,None,None,None]
        self.character_region=[None,None,None,None]
        for i in range(4):
            self.character_hbmp[i]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+self.character_files[i]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
            ##Create HDC##
            self.character_hdc[i]=windll.gdi32.CreateCompatibleDC(hdc_main)             #Make hdc similar to the reference hdc
            windll.gdi32.SelectObject(self.character_hdc[i],self.character_hbmp[i])     #Copy image into hdc

        ##LOAD REGIONS##
        Points=wf.REGION(1)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        ##Character1_down##
        self.character_region[0]=temp
        for i in range(2,9):
            Points=wf.REGION(i)
            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
            windll.gdi32.CombineRgn(self.character_region[0],self.character_region[0],temp,wf.RGN_OR)
        Points=wf.REGION(19)
        ##Character1_up##
        self.character_region[1]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        for i in range(20,27):
            Points=wf.REGION(i)
            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
            windll.gdi32.CombineRgn(self.character_region[1],self.character_region[1],temp,wf.RGN_OR)
            Points=wf.REGION(27)
        Points=wf.REGION(9)
        ##Character1_right##
        self.character_region[2]= wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        for i in range(10,14):
            Points=wf.REGION(i)
            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
            windll.gdi32.CombineRgn(self.character_region[2],self.character_region[2],temp,wf.RGN_OR)
        Points=wf.REGION(14)
        ##Character1_left##
        self.character_region[3]= wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        for i in range(15,19):
            Points=wf.REGION(i)
            temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
            windll.gdi32.CombineRgn(self.character_region[3],self.character_region[3],temp,wf.RGN_OR)

        ##ADD HAIR##
        Points=wf.REGION(27)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(self.character_region[0],self.character_region[0],temp,wf.RGN_OR) ##add hair down
        Points=wf.REGION(28)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(self.character_region[1],self.character_region[1],temp,wf.RGN_OR) ##add hair up
        Points=wf.REGION(29)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(self.character_region[2],self.character_region[2],temp,wf.RGN_OR) ##add hair right
        Points=wf.REGION(30)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(self.character_region[3],self.character_region[3],temp,wf.RGN_OR) ##add hair left
        ##DEFINE THE TARGET BOX##
        self.tboxUL=POINT(0,wf.character_height-100)
        self.tboxUR=POINT(wf.character_width,wf.character_height-100)
        self.tboxLL=POINT(0,wf.character_height)
        self.tboxLR=POINT(wf.character_width,wf.character_height)
        
        ##DEFINE REFERNCE POSITIONS##
        self.position=POINT(wf.shiftx+100,wf.shifty+100)
        self.tile_position=POINT(int(100/wf.tile_w),int(100/wf.tile_h))
        self.direction="down"
        
    def Reference_Tile(self):
        #Reference Tile#
        return self.tile_position

    def Update_Position(self,shiftx,shifty):
        self.position=POINT(shiftx,shifty)
        self.tile_position=POINT(int(shiftx/wf.tile_w),int(shifty/wf.tile_h))
        return 0

    def Target_Box_Shifted(self,shiftx,shifty):
        shifted_tboxUL=POINT(self.tboxUL.x+shiftx,self.tboxUL.y+shifty)
        shifted_tboxUR=POINT(self.tboxUR.x+shiftx,self.tboxUR.y+shifty)
        shifted_tboxLL=POINT(self.tboxLL.x+shiftx,self.tboxLL.y+shifty)
        shifted_tboxLR=POINT(self.tboxLR.x+shiftx,self.tboxLR.y+shifty)
        return [shifted_tboxUL,shifted_tboxUR,shifted_tboxLL,shifted_tboxLR]
    

    def Target_Box(self):
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
        ##Copy Object onto tile
        i=self.dict_index_to_character["character1_"+self.direction]     ##Find the desired image
        windll.gdi32.OffsetRgn(self.character_region[i],                ##Shift the region to draw the character
                               position_new)
        windll.gdi32.SelectClipRgn(hdc,self.character_region[i])       ##Select the shifted region for copying the image
        windll.gdi32.BitBlt(hdc,position_new,wf.character_width,        ##Add Character to Background
                            wf.character_height,self.character_hdc[i],
                            0,0,wf.SRCCOPY)
        ##Reset class object and hdc##
        windll.gdi32.SelectClipRgn(hdc,None)                            ##Remove clipping region
        windll.gdi32.OffsetRgn(self.character_region[i],-position_new.x,#Return Region to original positoin
                                -position_new.y)
