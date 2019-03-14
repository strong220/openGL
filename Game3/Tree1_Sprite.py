##THIS CLASS IS FOR THE SMALL TREE SPRITE##
import window_functions as wf
import window_structures as ws
from Button_Sprite import Button
from ctypes import *
from ctypes.wintypes import *

class Tree_Sprite_1:
    def __init__(self,hdc_main,file_path):
        ##Initialize hdc, and load image##
        tree_file="Tree_1.bmp"
        self.hbmp=wf.LoadImage(c_void_p(),LPCWSTR(file_path+tree_file),    #Load image
                                    wf.IMAGE_BITMAP,0,0,
                                    8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        
        self.hdc=windll.gdi32.CreateCompatibleDC(hdc_main)                 #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(self.hdc,self.hbmp)                       #Copy image into hdc
        self.button=Button(hdc_main,file_path,"red")                              #Load Button

        ##LOAD REGION##
        points=[(70, 1),(71, 2),(72, 10),(71, 13),(72, 15),(72, 27),(73, 28),(73, 29),(72, 39),(74, 43),
                (74, 48),(77, 47),(80, 47),(81, 49),(81, 51),(79, 53),(78, 54),(75, 54),(75, 56),(73, 57),
                (72, 57),(72, 59),(74, 59),(74, 67),(75, 68),(74, 71),(76, 72),(74, 75),(75, 76),(75, 78),
                (77, 79),(75, 83),(73, 86),(78, 86),(79, 89),(81, 87),(81, 84),(78, 84),(81, 81),(81, 78),
                (83, 77),(86, 77),(88, 75),(89, 76),(90, 79),(90, 82),(88, 84),(88, 95),(89, 94),(90, 92),
                (91, 96),(93, 96),(94, 98),(92, 99),(91, 104),(90, 102),(89, 102),(87, 105),(82, 105),(81, 107),
                (80, 108),(77, 108),(76, 109),(74, 108),(74, 123),(76, 121),(78, 125),(79, 125),(80, 124),(83, 122),
                (82, 126),(87, 124),(89, 123),(91, 124),(94, 122),(97, 123),(98, 129),(97, 130),(96, 130),(94, 128),
                (92, 128),(92, 129),(94, 133),(92, 133),(91, 131),(90, 132),(90, 134),(91, 137),(89, 136),(87, 137),
                (83, 136),(82, 136),(80, 134),(78, 133),(76, 132),(75, 133),(76, 134),(78, 135),(79, 139),(78, 139),
                (78, 141),(76, 143),(77, 144),(74, 145),(74, 163),(76, 164),(76, 166),(78, 163),(80, 163),(81, 161),
                (82, 162),(84, 163),(85, 163),(86, 163),(88, 164),(89, 162),(89, 155),(87, 153),(88, 153),(91, 153),
                (92, 151),(96, 152),(99, 153),(95, 157),(99, 158),(101, 159),(105, 160),(104, 161),(104, 166),(100, 168),
                (97, 168),(95, 169),(91, 171),(86, 172),(85, 173),(82, 173),(83, 174),(83, 176),(85, 178),(85, 181),
                (86, 182),(84, 183),(82, 183),(80, 185),(79, 183),(77, 182),(78, 181),(78, 178),(77, 179),(76, 181),
                (74, 180),(74, 196),(75, 197),(74, 198),(77, 199),(75, 201),(77, 202),(79, 204),(78, 205),(77, 208),
                (74, 212),(76, 213),(78, 212),(79, 209),(82, 208),(83, 205),(84, 203),(85, 206),(87, 204),(88, 203),
                (89, 200),(91, 200),(91, 197),(87, 196),(86, 194),(86, 192),(83, 191),(84, 190),(87, 191),(89, 189),
                (90, 187),(92, 188),(98, 191),(94, 191),(95, 186),(97, 180),(98, 177),(100, 178),(100, 180),(101, 180),
                (104, 177),(104, 179),(103, 184),(104, 191),(100, 187),(99, 190),(99, 193),(101, 193),(99, 196),(99, 200),
                (100, 202),(105, 202),(107, 200),(112, 200),(115, 206),(111, 206),(109, 208),(106, 209),(107, 211),(110, 212),
                (111, 213),(113, 214),(114, 219),(116, 218),(117, 222),(118, 225),(112, 224),(112, 222),(108, 221),(108, 219),
                (106, 220),(104, 226),(101, 225),(101, 224),(95, 221),(98, 220),(99, 217),(101, 216),(102, 213),(99, 212),
                (96, 211),(95, 212),(91, 214),(88, 216),(88, 217),(84, 217),(83, 219),(80, 220),(82, 221),(80, 223),
                (79, 225),(76, 226),(74, 223),(74, 236),(78, 235),(80, 235),(81, 234),(83, 236),(84, 238),(83, 239),
                (83, 241),(84, 242),(83, 244),(81, 242),(80, 243),(79, 245),(78, 245),(77, 246),(80, 247),(83, 247),
                (82, 248),(83, 249),(82, 251),(83, 252),(79, 253),(79, 254),(80, 254),(83, 257),(84, 255),(91, 255),
                (93, 256),(96, 255),(97, 254),(98, 255),(99, 255),(100, 254),(101, 255),(103, 253),(105, 255),(108, 254),
                (107, 253),(109, 252),(111, 247),(112, 245),(113, 246),(115, 244),(116, 246),(117, 245),(118, 248),(119, 249),
                (118, 252),(119, 253),(124, 252),(124, 253),(126, 257),(124, 258),(123, 259),(120, 259),(120, 261),(117, 261),
                (116, 262),(112, 263),(112, 264),(114, 264),(113, 267),(111, 265),(111, 266),(109, 268),(107, 264),(106, 267),
                (105, 266),(105, 264),(104, 264),(103, 266),(101, 266),(101, 264),(95, 264),(94, 265),(93, 264),(91, 264),
                (87, 263),(87, 268),(88, 269),(85, 272),(83, 272),(82, 274),(80, 272),(79, 274),(78, 275),(79, 278),
                (81, 278),(83, 277),(86, 276),(87, 277),(91, 277),(91, 273),(93, 274),(93, 272),(95, 271),(96, 271),
                (99, 271),(99, 273),(103, 273),(104, 272),(106, 272),(106, 274),(110, 275),(111, 274),(112, 275),(112, 278),
                (113, 279),(112, 280),(109, 279),(109, 282),(102, 281),(102, 284),(101, 285),(96, 282),(94, 282),(94, 284),
                (91, 285),(90, 285),(89, 284),(87, 283),(87, 285),(85, 286),(83, 288),(85, 289),(84, 290),(84, 293),
                (79, 294),(77, 296),(77, 299),(80, 297),(87, 295),(95, 294),(96, 293),(99, 293),(102, 292),(104, 292),
                (105, 291),(109, 290),(110, 289),(113, 289),(115, 291),(116, 290),(117, 293),(127, 293),(128, 294),(132, 293),
                (134, 295),(136, 291),(137, 292),(136, 296),(137, 299),(136, 300),(135, 299),(135, 298),(134, 298),(134, 302),
                (133, 302),(132, 301),(131, 301),(130, 303),(129, 300),(125, 302),(124, 303),(123, 305),(122, 302),(119, 305),
                (118, 302),(116, 302),(115, 306),(114, 303),(112, 306),(110, 305),(108, 303),(107, 306),(100, 305),(99, 303),
                (98, 303),(96, 305),(95, 305),(93, 303),(92, 305),(90, 305),(89, 303),(88, 303),(87, 306),(83, 306),
                (80, 304),(80, 306),(76, 306),(76, 328),(78, 331),(80, 333),(80, 335),(82, 335),(68, 339),(66, 339),
                (57, 336),(58, 335),(59, 333),(60, 332),(61, 330),(62, 329),(64, 329),(65, 328),(65, 298),(63, 296),
                (62, 298),(59, 299),(53, 299),(52, 300),(50, 300),(45, 301),(44, 302),(43, 305),(41, 306),(40, 308),
                (37, 309),(36, 313),(35, 310),(31, 310),(31, 309),(33, 307),(32, 306),(35, 303),(34, 302),(34, 299),
                (31, 299),(31, 301),(27, 301),(26, 303),(25, 302),(23, 301),(22, 304),(20, 302),(19, 304),(16, 304),
                (15, 305),(15, 307),(14, 308),(10, 308),(6, 306),(9, 305),(8, 304),(9, 303),(11, 303),(12, 300),
                (8, 300),(6, 302),(5, 300),(2, 301),(0, 300),(0, 297),(3, 294),(4, 295),(9, 295),(10, 294),
                (10, 293),(8, 289),(9, 288),(10, 284),(11, 288),(15, 287),(19, 285),(19, 281),(20, 280),(22, 280),
                (23, 278),(24, 280),(26, 281),(26, 286),(29, 289),(29, 290),(30, 291),(31, 291),(32, 289),(34, 288),
                (35, 292),(38, 291),(39, 290),(42, 293),(43, 292),(55, 291),(63, 288),(62, 287),(62, 285),(63, 284),
                (63, 282),(61, 282),(60, 283),(59, 282),(59, 280),(57, 278),(56, 278),(56, 280),(53, 281),(52, 282),
                (51, 281),(46, 281),(44, 283),(43, 281),(40, 277),(39, 279),(37, 277),(36, 279),(34, 277),(33, 281),
                (32, 280),(31, 283),(30, 280),(29, 280),(27, 278),(27, 274),(29, 276),(30, 274),(32, 276),(33, 273),
                (34, 272),(35, 269),(37, 270),(42, 269),(43, 267),(39, 266),(45, 266),(46, 264),(48, 266),(51, 266),
                (50, 270),(54, 270),(54, 271),(58, 273),(60, 271),(59, 269),(62, 268),(62, 267),(60, 265),(59, 262),
                (55, 264),(56, 259),(59, 260),(59, 255),(55, 256),(53, 258),(54, 260),(53, 262),(49, 263),(46, 262),
                (42, 261),(43, 258),(38, 259),(31, 259),(30, 264),(26, 266),(25, 266),(24, 268),(22, 267),(20, 261),
                (17, 261),(14, 262),(13, 260),(12, 261),(11, 263),(6, 262),(8, 260),(6, 259),(8, 258),(8, 257),
                (7, 254),(10, 255),(11, 252),(12, 255),(14, 256),(15, 253),(19, 253),(25, 252),(26, 251),(26, 250),
                (24, 249),(26, 249),(27, 245),(26, 244),(33, 244),(31, 250),(33, 250),(33, 251),(37, 250),(38, 249),
                (39, 247),(40, 250),(45, 251),(46, 249),(43, 247),(44, 246),(52, 245),(54, 246),(52, 247),(54, 248),
                (55, 249),(59, 249),(61, 248),(63, 247),(65, 247),(65, 244),(63, 244),(62, 246),(60, 245),(61, 244),
                (59, 244),(58, 246),(57, 244),(52, 244),(52, 245),(47, 246),(45, 245),(45, 242),(44, 243),(39, 241),
                (34, 241),(32, 243),(30, 242),(31, 241),(29, 241),(27, 243),(26, 241),(20, 239),(18, 240),(15, 241),
                (15, 239),(13, 239),(13, 238),(11, 237),(14, 236),(12, 235),(13, 233),(15, 234),(16, 231),(20, 232),
                (20, 234),(23, 234),(24, 232),(26, 235),(29, 235),(30, 233),(31, 235),(34, 236),(36, 234),(37, 237),
                (38, 232),(39, 236),(40, 233),(42, 235),(46, 233),(49, 236),(51, 235),(55, 237),(56, 239),(58, 234),
                (60, 235),(60, 237),(61, 236),(66, 237),(67, 229),(66, 229),(64, 231),(61, 230),(59, 232),(58, 230),
                (57, 231),(56, 229),(51, 229),(52, 227),(47, 226),(40, 229),(42, 226),(43, 226),(43, 225),(39, 224),
                (40, 223),(41, 221),(42, 222),(43, 220),(46, 222),(47, 218),(49, 219),(51, 220),(56, 221),(61, 222),
                (61, 219),(57, 218),(55, 217),(60, 216),(61, 214),(67, 215),(67, 209),(61, 208),(59, 206),(60, 202),
                (63, 202),(63, 198),(67, 198),(67, 193),(64, 195),(57, 196),(56, 198),(59, 199),(59, 201),(57, 204),
                (54, 204),(54, 202),(53, 201),(52, 204),(51, 204),(50, 202),(47, 201),(46, 199),(44, 200),(43, 202),
                (41, 201),(40, 204),(39, 203),(35, 206),(34, 203),(33, 205),(30, 205),(30, 208),(28, 207),(30, 204),
                (28, 203),(29, 201),(32, 201),(32, 199),(36, 200),(36, 196),(38, 197),(40, 196),(42, 196),(42, 195),
                (43, 195),(45, 194),(46, 193),(48, 193),(49, 191),(48, 189),(44, 191),(43, 190),(39, 190),(39, 189),
                (36, 189),(33, 188),(30, 189),(28, 188),(24, 186),(25, 184),(25, 182),(29, 182),(30, 181),(32, 182),
                (34, 182),(34, 184),(37, 183),(42, 183),(42, 179),(40, 178),(41, 174),(39, 173),(43, 172),(44, 169),
                (50, 168),(48, 169),(46, 170),(44, 176),(48, 176),(47, 177),(48, 179),(48, 180),(49, 180),(40, 183),
                (53, 181),(52, 186),(56, 186),(55, 181),(58, 182),(58, 180),(61, 181),(63, 183),(63, 188),(67, 189),
                (67, 181),(61, 181),(62, 179),(66, 178),(63, 177),(61, 176),(61, 174),(57, 174),(59, 172),(58, 168),
                (61, 169),(62, 165),(63, 163),(67, 163),(67, 148),(65, 143),(63, 145),(64, 148),(63, 149),(63, 150),
                (65, 151),(64, 153),(62, 153),(62, 156),(61, 152),(59, 153),(58, 155),(56, 154),(58, 153),(58, 152),
                (52, 152),(53, 150),(55, 151),(57, 150),(55, 146),(49, 146),(48, 148),(47, 145),(46, 145),(45, 148),
                (43, 146),(41, 147),(40, 149),(39, 145),(38, 146),(37, 148),(33, 148),(35, 146),(32, 145),(35, 144),
                (36, 141),(37, 143),(38, 142),(39, 142),(39, 138),(41, 140),(45, 140),(45, 142),(47, 140),(49, 141),
                (51, 139),(55, 140),(56, 139),(62, 139),(63, 138),(65, 139),(65, 137),(63, 136),(67, 134),(67, 131),
                (65, 130),(63, 129),(64, 128),(67, 124),(66, 123),(61, 123),(60, 131),(59, 128),(57, 129),(56, 132),
                (55, 130),(52, 131),(51, 133),(50, 132),(51, 129),(54, 128),(50, 127),(49, 126),(45, 125),(42, 126),
                (40, 123),(38, 124),(39, 121),(40, 115),(41, 113),(42, 116),(44, 117),(48, 116),(49, 113),(50, 116),
                (52, 115),(52, 118),(56, 118),(56, 114),(58, 117),(59, 116),(62, 116),(62, 114),(64, 112),(65, 110),
                (64, 108),(62, 110),(60, 109),(64, 105),(59, 106),(60, 102),(56, 103),(55, 104),(54, 102),(50, 102),
                (52, 99),(53, 93),(55, 96),(57, 96),(58, 95),(64, 95),(63, 98),(66, 97),(66, 93),(64, 92),
                (65, 89),(64, 87),(67, 86),(67, 85),(65, 84),(66, 82),(65, 78),(64, 76),(63, 74),(67, 73),
                (65, 72),(60, 70),(63, 69),(61, 68),(57, 67),(60, 66),(56, 62),(55, 58),(57, 57),(58, 55),
                (59, 57),(60, 58),(61, 62),(63, 64),(64, 67),(66, 65),(67, 66),(69, 65),(69, 63),(68, 63),
                (68, 60),(66, 59),(67, 57),(69, 59),(70, 58),(68, 56),(68, 54),(66, 52),(67, 47),(70, 46),
                (69, 45),(66, 44),(69, 43),(69, 42),(66, 40),(69, 39),(68, 35),(67, 32),(70, 31),(68, 29),
                (68, 26),(69, 25),(68, 19),(70, 19),(67, 15),(69, 13),(69, 3)]

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
        self.position=POINT(int(wf.tile_w/2-wf.tree1_w/2),wf.tile_h-wf.tree1_h)

    def Target_box(self,x_shift,y_shift):
        ##Return the shifted target box
        shiftedboxUL=POINT(self.tboxUL.x+x_shift,self.tboxUL.y+y_shift)
        shiftedboxUR=POINT(self.tboxUR.x+x_shift,self.tboxUR.y+y_shift)
        shiftedboxLL=POINT(self.tboxLL.x+x_shift,self.tboxLL.y+y_shift)
        shiftedboxLR=POINT(self.tboxLR.x+x_shift,self.tboxLR.y+y_shift)
        return [shiftedboxUL,shiftedboxUR,shiftedboxLL,shiftedboxLR]

    def Draw_Tree(self,hdc,object_string,x_shift,y_shift,player_selection,player):
        ##IF TILE NEEDS OBJECT THEN ADD##
        text=["E","9"]
        if object_string[2]=="T":
            ##Shift the reference position to desired tile 
            position_new=POINT(self.position.x+x_shift,self.position.y+y_shift)
            ##Copy Object onto tile
            windll.gdi32.OffsetRgn(self.Region,position_new)                                                ##Shift the region to draw the tree
            windll.gdi32.SelectClipRgn(hdc,self.Region)                                                     ##Select the shifted region for copying the tree
            windll.gdi32.BitBlt(hdc,position_new,wf.tree1_w,wf.tree1_h,self.hdc,0,0,wf.SRCCOPY)             ##Add tree to background
            ##Reset class object and hdc
            windll.gdi32.SelectClipRgn(hdc,None)                                                            ##Remove Clipping Region
            windll.gdi32.OffsetRgn(self.Region,-position_new.x,-position_new.y)                             ##Return the region back
            ##CHECK TO SEE IF BUTTON NEEDS TO BE DRAWN##
            if object_string[4]=="B" and player_selection==wf.Axe and player==int(object_string[5]):
                ##Position the button##
                position_new.x=position_new.x+int(wf.tile_w/2)
                position_new.y=position_new.y+wf.tile_h-40
                ##DRAW BUTTON##
                self.button.Draw_Button(hdc,position_new.x,position_new.y,text[player])
                ##Return 1 if button was drawn
                return 1
            else:
                ##Return 0 if object was drawn
                return 0
        else:
            ##Return -1 if nothing was drawn
            return -1
            
##        for i in range(int(len(tree1_region_points)/10)+1):
##            temp=str(tree1_region_points[i*10])
##            for j in range(1,10):
##                if i*10+j<len(tree1_region_points):
##                    temp=temp+","+str(tree1_region_points[i*10+j])
##            print(temp)
        
##test=Tree_Sprite_1(None,"C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\")
##box=test.Target_box(10,0,)
##print(test.Draw_Tree(None,"W-",0,0,wf.Axe))