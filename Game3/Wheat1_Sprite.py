##THIS CLASS IS FOR THE SMALL TREE SPRITE##
import window_functions as wf
import window_structures as ws
from Button_Sprite import Button
from ctypes import *
from ctypes.wintypes import *

class Wheat_Sprite_1:
    def __init__(self,hdc_main,file_path):
        ##Initialize hdc, and load image##
        Wheat_Stalk_file="Wheat_Stalk1.bmp"
        Tile_file="Grass_1.bmp"#"Temp_background.bmp"
        self.stalk_hbmp=wf.LoadImage(c_void_p(),LPCWSTR(file_path+Wheat_Stalk_file),    #Load image
                                    wf.IMAGE_BITMAP,0,0,
                                    8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        self.hbmp=wf.LoadImage(c_void_p(),LPCWSTR(file_path+Tile_file),    #Load tile image
                            wf.IMAGE_BITMAP,0,0,
                            8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        
        self.hdc=windll.gdi32.CreateCompatibleDC(hdc_main)                 #Make hdc similar to the reference hdc
        self.stalk_hdc=windll.gdi32.CreateCompatibleDC(hdc_main)                 #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(self.hdc,self.hbmp)                       #Copy image into hdc
        windll.gdi32.SelectObject(self.stalk_hdc,self.stalk_hbmp)                       #Copy image into hdc
        self.button=Button(hdc_main,file_path,"red")                              #Load Button

        ##LOAD REGION##
        points=[(26,200),(24,193),(22,191),(21,191),(21,189),(19,189),(18,188),(16,188),(9,186),(5,185),(3,185),(2,184),
                (2,183),(11,183),(12,184),(14,184),(19,186),(21,188),(21,180),(20,176),(19,172),(18,169),(17,166),(12,166),
                (12,167),(8,167),(8,169),(6,171),(6,172),(5,172),(5,171),(7,169),(7,166),(8,165),(15,165),(16,166),(17,165),
                (13,158),(14,158),(16,160),(11,138),(9,138),(4,143),(4,144),(3,144),(2,145),(2,148),(1,147),(4,139),(4,137),
                (6,135),(10,135),(9,133),(8,129),(7,124),(7,120),(4,120),(4,116),(3,115),(3,112),(2,111),(4,111),(4,110),
                (3,109),(3,108),(2,107),(3,106),(2,105),(2,102),(3,101),(2,100),(5,100),(5,101),(6,102),(6,104),(7,105),
                (7,106),(8,108),(8,109),(7,110),(9,112),(10,120),(9,121),(9,122),(22,173),(22,170),(22,165),(23,165),(13,85),
                (10,84),(10,83),(9,76),(8,75),(10,75),(10,74),(9,73),(9,72),(8,71),(9,70),(8,69),(8,66),(9,65),(8,64),
                (11,64),(12,68),(13,69),(12,70),(14,72),(14,73),(13,74),(15,76),(16,84),(15,85),(16,99),(17,100),(20,100),
                (21,94),(22,94),(22,99),(21,100),(21,103),(20,104),(17,105),(17,106),(18,107),(26,172),(27,171),(27,165),
                (28,164),(28,162),(27,161),(26,152),(27,147),(28,156),(29,156),(29,122),(25,122),(23,124),(22,124),(22,121),
                (21,121),(21,119),(22,119),(23,118),(29,118),(29,72),(25,68),(24,68),(24,67),(20,63),(20,62),(18,60),(18,59),
                (15,56),(14,56),(14,55),(12,55),(12,54),(16,54),(21,56),(21,57),(23,59),(24,59),(25,60),(25,62),(27,64),(27,66),
                (29,66),(29,30),(28,30),(27,29),(27,20),(28,19),(27,18),(27,16),(28,15),(27,14),(27,12),(28,11),(28,9),(31,9),
                (31,10),(32,11),(32,19),(33,20),(33,29),(31,31),(31,87),(34,84),(34,83),(38,79),(42,78),(44,78),(44,79),(42,79),
                (41,80),(38,81),(38,84),(34,88),(34,89),(32,91),(32,96),(31,97),(31,109),(34,109),(34,110),(33,111),(32,111),
                (31,173),(34,170),(42,118),(39,118),(38,117),(36,116),(36,115),(34,112),(36,111),(40,115),(43,115),(51,60),
                (51,50),(53,48),(53,44),(54,43),(55,39),(57,39),(57,41),(58,42),(58,43),(56,45),(57,46),(57,48),(56,48),(55,49),
                (56,50),(57,50),(56,59),(53,60),(47,101),(50,98),(57,98),(57,99),(52,100),(52,101),(51,102),(50,102),(46,106),
                (45,109),(42,132),(45,132),(47,130),(52,130),(52,132),(49,133),(46,133),(45,134),(41,135),(36,171),(37,170),
                (38,167),(39,166),(39,168),(41,170),(42,169),(54,138),(56,136),(55,135),(55,132),(57,127),(57,126),(58,125),
                (60,125),(60,121),(61,120),(60,119),(61,118),(61,117),(63,117),(64,115),(64,114),(67,114),(67,118),(65,120),
                (64,125),(64,129),(63,129),(62,132),(62,134),(57,135),(56,136),(57,137),(48,161),(57,161),(57,164),(58,164),
                (58,165),(56,165),(56,164),(55,163),(51,163),(51,164),(46,164),(41,175),(41,183),(47,182),(56,182),(56,183),
                (54,183),(41,186),(40,188),(37,195),(36,196),(36,199)]
                

        ##TRANSLATE POINTS INTO REGION##
        Rgn=POINT*len(points)
        temp=[]
        for i in range(len(points)):
            temp.append(POINT(points[i][0],points[i][1]))
        out=Rgn(*temp)

        self.number_of_stalks=12
        self.spacing_x=[0,20,40,60,80,100,0,20,40,60,80,100]
        self.spacing_y=[0,0,0,0,0,0,120,120,120,120,120,120]
        self.Single_Region=wf.CreatePolygonRgn(out,len(out),wf.WINDING)
        self.Region=wf.CreatePolygonRgn(out,len(out),wf.WINDING)
        self.Temp_Region=[wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING),
                     wf.CreatePolygonRgn(out,len(out),wf.WINDING)]
        ##Combine Shifted Regions##
        for i in range(self.number_of_stalks):
            position=POINT(self.spacing_x[i],self.spacing_y[i])
            ##Create Regions for making image
            windll.gdi32.OffsetRgn(self.Temp_Region[i],position)
            ##Copy Object onto tile
            windll.gdi32.OffsetRgn(self.Single_Region,position)
            windll.gdi32.CombineRgn(self.Region,self.Region,self.Single_Region,wf.RGN_OR)
            windll.gdi32.OffsetRgn(self.Single_Region,-position.x,-position.y)

        ##DEFINE REFERENCE POSITION##
        self.position=POINT(int(wf.tile_w/2-wf.tree1_w/2),wf.tile_h-wf.tree1_h)
        
        for i in range(self.number_of_stalks):
                ##Shift the reference position to desired tile 
                position_new=POINT()#POINT(self.position.x,self.position.y)
                ##Copy Object onto tile
                windll.gdi32.OffsetRgn(self.Temp_Region[i],position_new)                                                ##Shift the region to draw the tree
                windll.gdi32.SelectClipRgn(self.hdc,self.Temp_Region[i])                                                     ##Select the shifted region for copying the tree
                windll.gdi32.BitBlt(self.hdc,position_new.x+self.spacing_x[i],position_new.y+self.spacing_y[i],wf.tree1_w,wf.tree1_h,self.stalk_hdc,0,0,wf.SRCCOPY)             ##Add tree to background
                ##Reset class object and hdc
                windll.gdi32.SelectClipRgn(self.hdc,None)                                                            ##Remove Clipping Region
                windll.gdi32.OffsetRgn(self.Temp_Region[i],-position_new.x,-position_new.y)                             ##Return the region back

        ##DEFINE THE TARGET BOX##
        self.tboxUL=POINT(10,10)
        self.tboxUR=POINT(wf.tile_w-10,10)
        self.tboxLL=POINT(10,wf.tile_h-10)
        self.tboxLR=POINT(wf.tile_w-10,wf.tile_h-10)

    def Target_box(self,x_shift,y_shift,number=None):
        ##Return the shifted target box
        shiftedboxUL=POINT(self.tboxUL.x+x_shift,self.tboxUL.y+y_shift)
        shiftedboxUR=POINT(self.tboxUR.x+x_shift,self.tboxUR.y+y_shift)
        shiftedboxLL=POINT(self.tboxLL.x+x_shift,self.tboxLL.y+y_shift)
        shiftedboxLR=POINT(self.tboxLR.x+x_shift,self.tboxLR.y+y_shift)
        return [shiftedboxUL,shiftedboxUR,shiftedboxLL,shiftedboxLR]

    def Draw(self,hdc,object_string,x_shift,y_shift,Player):
        ##IF TILE NEEDS OBJECT THEN ADD##
        text=["E","9"]
        if object_string[2]=="F":
            ##Shift the reference position to desired tile 
            position_new=POINT(x_shift,y_shift)
            ##Copy Object onto tile
            windll.gdi32.OffsetRgn(self.Region,position_new)                                                ##Shift the region to draw the tree
            windll.gdi32.SelectClipRgn(hdc,self.Region)                                                     ##Select the shifted region for copying the tree
            windll.gdi32.BitBlt(hdc,position_new,wf.tree1_w,wf.tree1_h,self.hdc,0,0,wf.SRCCOPY)             ##Add tree to background
            windll.gdi32.OffsetRgn(self.Region,-position_new.x,-position_new.y)                             ##Return the region back
            windll.gdi32.SelectClipRgn(hdc,None)                                                            ##Remove Clipping Region
            ##CHECK TO SEE IF BUTTON NEEDS TO BE DRAWN##
            position_new=POINT(self.position.x+x_shift,self.position.y+y_shift)
            if object_string[4]=="B" and Player.Tool_selection==wf.Axe and Player.Character[0]==object_string[5]:
                ##Position the button##
                position_new.x=position_new.x+int(wf.tile_w/2)-wf.button_w
                position_new.y=position_new.y-int(wf.tile_h/2)+wf.tree1_h-2*wf.button_h
                ##DRAW BUTTON##
                self.button.Draw_Button(hdc,position_new.x,position_new.y,text[int(Player.Character[0])])
                ##Return 1 if button was drawn
                return 1
            else:
                ##Return 0 if object was drawn
                return 0
        else:
            ##Return -1 if nothing was drawn
            return -1
            
