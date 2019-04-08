##THIS CLASS IS FOR THE SMALL WALL SPRITES##
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *
from Button_Sprite import Button

class Wall_Sprite_1(object):
    def __init__(self,hdc_main,file_path_main,Wall):
        ##Initialize hdc, and load image##
        wall_vertical_file="Wall_vertical.bmp"
        wall_horizontal_file="Wall_horizontal.bmp"
        ##Load Image##
        hbmp_vertical=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+wall_vertical_file),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        hbmp_horizontal=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+wall_horizontal_file),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        self.hbmp=[hbmp_vertical,hbmp_horizontal]

        ##Load hdcs##
        hdc_vertical=windll.gdi32.CreateCompatibleDC(hdc_main)             #Make vertical hdc similar to the reference hdc
        hdc_horizontal=windll.gdi32.CreateCompatibleDC(hdc_main)           #Make horizontal hdc similar to the reference hdc
        self.hdc=[hdc_vertical,hdc_horizontal]
        windll.gdi32.SelectObject(self.hdc[0],self.hbmp[0])         #Copy vertical image into hdc
        windll.gdi32.SelectObject(self.hdc[1],self.hbmp[1])         #Copy horizontal image into hdc
        self.button=Button(hdc_main,file_path_main,"red")                              #Load Button

        ##LOAD REGION##
        points_vertical=[(20,8),(21,7),(24,6),(25,6),(28,7),(29,8),(29,299),(20,299)]

        points_horizontal=[(0,2),(2,0),(7,0),(9,2),(10,2),(12,0),(17,0),(19,2),(20,2),
                           (22,0),(27,0),(29,2),(30,2),(32,0),(37,0),(39,2),(40,2),
                           (42,0),(47,0),(49,2),(50,2),(52,0),(57,0),(59,2),(60,2),
                           (62,0),(67,0),(69,2),(70,2),(72,0),(77,0),(79,2),(80,2),
                           (82,0),(87,0),(89,2),(90,2),(92,0),(97,0),(99,2),(100,2),
                           (102,0),(107,0),(109,2),(110,2),(112,0),(117,0),(119,2),(120,2),
                           (122,0),(127,0),(129,2),(130,2),(132,0),(137,0),(139,2),(140,2),
                           (142,0),(147,0),(149,2),(150,2),(152,0),(157,0),(159,2),(160,2),
                           (162,0),(167,0),(169,2),(170,2),(172,0),(177,0),(179,2),(180,2),
                           (182,0),(187,0),(189,2),(190,2),(192,0),(197,0),(199,2),(199,104),
                           (0,104)]
        points=[points_vertical,points_horizontal]
        
        ##TRANSLATE POINTS INTO REGION##
        self.Region=[None,None]
        for i in range(2):
            Rgn=POINT*len(points[i])
            temp=[]
            for j in range(len(points[i])):
                temp.append(POINT(points[i][j][0],points[i][j][1]))
            out=Rgn(*temp)
            self.Region[i]=wf.CreatePolygonRgn(out,len(out),wf.WINDING)

        ##DEFINE THE TARGET BOX##
        self.Wall_target_boxes=[ws.FourPoint(),ws.FourPoint(),ws.FourPoint(),ws.FourPoint()]
        ##Facing right
        self.Wall_target_boxes[0].WallUL=POINT(0,0)
        self.Wall_target_boxes[0].WallUR=POINT(wf.wall_vertical_w,0)
        self.Wall_target_boxes[0].WallLL=POINT(0,wf.tile_h)
        self.Wall_target_boxes[0].WallLR=POINT(wf.wall_vertical_w,wf.tile_h)
        ##Facing left
        self.Wall_target_boxes[1].WallUL=POINT(wf.tile_w-wf.wall_vertical_w,0)
        self.Wall_target_boxes[1].WallUR=POINT(wf.tile_w,0)
        self.Wall_target_boxes[1].WallLL=POINT(wf.tile_w-wf.wall_vertical_w,wf.tile_h)
        self.Wall_target_boxes[1].WallLR=POINT(wf.tile_w,wf.tile_h)
        ##Facing up
        self.Wall_target_boxes[2].WallUL=POINT(0,wf.tile_h-int(wf.wall_horizontal_h/4))
        self.Wall_target_boxes[2].WallUR=POINT(wf.tile_w,wf.tile_h-int(wf.wall_horizontal_h/4))
        self.Wall_target_boxes[2].WallLL=POINT(0,wf.tile_h)
        self.Wall_target_boxes[2].WallLR=POINT(wf.tile_w,wf.tile_h)
        ##Facing down
        self.Wall_target_boxes[3].WallUL=POINT(0,0)
        self.Wall_target_boxes[3].WallUR=POINT(wf.tile_w,0)
        self.Wall_target_boxes[3].WallLL=POINT(0,int(wf.wall_horizontal_h/4))
        self.Wall_target_boxes[3].WallLR=POINT(wf.tile_w,int(wf.wall_horizontal_h/4))

        ##DEFINE REFERENCE POSITIONS##
        self.position=[POINT(0,wf.tile_h-wf.wall_vertical_h),                                                      ##Define dictionary for where to put the walls
                       POINT(wf.tile_w-wf.wall_vertical_w,wf.tile_h-wf.wall_vertical_h),
                       POINT(0,wf.tile_h-wf.wall_horizontal_h),
                       POINT(0,-int(wf.wall_horizontal_h*3/4))]
        self.direction={"0":wf.r_build,"1":wf.l_build,"2":wf.u_build,"3":wf.d_build}          ##Define dictionary for button placement
        self.wall_type=Wall

    def Target_box(self,x_shift,y_shift,direction):
        ##Return the shifted target box
        shiftedboxUL=POINT(self.Wall_target_boxes[direction].WallUL.x+x_shift,self.Wall_target_boxes[direction].WallUL.y+y_shift)
        shiftedboxUR=POINT(self.Wall_target_boxes[direction].WallUR.x+x_shift,self.Wall_target_boxes[direction].WallUR.y+y_shift)
        shiftedboxLL=POINT(self.Wall_target_boxes[direction].WallLL.x+x_shift,self.Wall_target_boxes[direction].WallLL.y+y_shift)
        shiftedboxLR=POINT(self.Wall_target_boxes[direction].WallLR.x+x_shift,self.Wall_target_boxes[direction].WallLR.y+y_shift)
        return [shiftedboxUL,shiftedboxUR,shiftedboxLL,shiftedboxLR]

    def Draw(self,hdc,object_string,x_shift,y_shift,Player):
        ##IF TILE NEEDS OBJECT THEN ADD##
        i=self.wall_type
        if object_string[2]=="W" and int(object_string[3])==i:
            j=int(i/2)
            ##Shift the reference position to desired tile
            position_new=POINT(self.position[i].x+x_shift,self.position[i].y+y_shift)
            ##Copy Object onto tile
            windll.gdi32.OffsetRgn(self.Region[j],position_new)                                                 ##Shift the region to draw the tree
            windll.gdi32.SelectClipRgn(hdc,self.Region[j])                                                      ##Select the shifted region for copying the tree
            windll.gdi32.BitBlt(hdc,position_new,wf.wall_w[j],wf.wall_h[j],self.hdc[j],0,0,wf.SRCCOPY)             ##Add tree to background
            ##Reset class object and hdc
            windll.gdi32.SelectClipRgn(hdc,None)                                                                ##Remove Clipping Region
            windll.gdi32.OffsetRgn(self.Region[j],-position_new.x,-position_new.y)                              ##Return the region back
            ##ADD BUTTON IF APPLICABLE##
            ##GGOOBPCC##
            if object_string[4:6]=="B"+Player.Character[0] and Player.Tool_selection==wf.Axe:
                text=["E","9"]
                ##Pick Button placement##
                position_new=POINT(self.direction[object_string[3]].x+x_shift,
                               self.direction[object_string[3]].y+y_shift)
                self.button.Draw_Button(hdc,position_new.x,position_new.y,text[int(Player.Character[0])])
            return 0
        return -1
