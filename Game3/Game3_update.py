##THIS CONTAINS THE CLASS FOR UPDATING THE WINDOW##
import window_structures as ws
import window_functions as wf
import time
from ctypes import *
from ctypes.wintypes import *
import random
from wm_create import WM_CREATE as wmc
from wm_size import WM_SIZE as wms
from wm_paint import WM_PAINT as wmp
from update_statsblock import UPDATE_STATSBLOCK
from move import MOVE
from update_mem_background import UPDATE_MEM_BACKGROUND

class MainWndProc:
    def __init__(self,hwnd,uMsg,wParam,lParam,hInst):
        self.resource={"Tree":0,"Wheat":0}
        self.hwnd=hwnd
        self.uMsg=uMsg
        self.wParam=wParam
        self.lParam=ws.LPARAMS()
        temp=wf.Longsplit(lParam)
        self.lParam.x=temp[0]
        self.lParam.y=temp[1]
        self.hinst=hInst
        self.vwin=ws.Variables_and_dictionaries()
        self.map_all=wf.ARRAY_CREATE(int(wf.map_w/200),int(wf.map_h/200))
        self.call_back(hwnd,uMsg,wParam,lParam,hInst)
        self.step=0
    def call_back(self,hwnd,uMsg,wParam,lparam,hInst):
        self.hwnd=hwnd
        self.uMsg=uMsg
        self.wParam=wParam
        self.hinst=hInst
        if lparam>0:
            temp=wf.Longsplit(lparam)
            self.lParam.x=temp[0]
            self.lParam.y=temp[1]
         ##DICTIONARY FOR MESSAGE##
        inputs={1: "WM_CREATE",2: "WM_DESTROY",3:"WM_MOVE",5: "WM_SIZE",15: "WM_PAINT",
                160:"WM_NCMOUSEMOVE",161:"WM_NCLBUTTONDOWN",513: "WM_LBUTTONDOWN",
                514:"WM_LBUTTONUP", 512: "WM_MOUSEMOVE", 258:"WM_KEY_PRESS", 257:"WM_KEY_UP", 256:"WM_KEY_DOWN"}
        ##TRANSLATE MESSAGE##
        Message=inputs.get(self.uMsg,"Invalid")
        ##CALL FUNCTION RELATED TO MESSAGE##
        method=getattr(self,Message,lambda:"Invalid message")
        return method()
    def WM_CREATE(self):
        wmc(self.vwin,self.hwnd,self.map_all)
        return
   
    def WM_PAINT(self):
        ##Inititalize Stats block##
        UPDATE_STATSBLOCK(self.vwin)
        ##This is what fills the screen when it is first created or maximized.
        wmp(self.vwin,self.hwnd)
        return 0
    def ANIMATE(self):
        start=time.process_time()
        self.step=self.step+1
        self.Move()
        self.Update_Statsblock()
        self.Update_windows()
##        if self.step%30==0:# or self.step%30==25:
##            if self.vwin.Player1.step<3:
##                self.vwin.Player1.step=self.vwin.Player1.step+1
##            else:
##                self.vwin.Player1.step=0
        if self.step==100:
            self.step=0
            if self.map_all[0][0]=="G1------":
                self.map_all[0][0]="G3------"
            else:
                self.map_all[0][0]="G1------"
            self.player1_window=False
            self.player2_window=False
            ##Add random trees##
            x=int(random.random()*wf.map_w/200)
            y=int(random.random()*wf.map_h/200)
            self.map_all[x][y]="G1T-----"
        end=time.process_time()

        return (end-start)
        
    def WM_SIZE(self):
        wms(self.vwin,self.hwnd)
        return
    def WM_LBUTTONDOWN(self):
        ##Restrict the mouse cursor to the client area. This
        ##ensures that the window recieves a matching
        ##WM_LBUTTONUP message
##        windll.user32.ClipCursor(pointer(self.vwin.rcClient))
##        self.vwin.pt.x=self.lParam.x
##        self.vwin.pt.y=self.lParam.y
        print("pointx ",self.lParam.x,"pointy ",self.lParam.y)
##        print("cursor clipped")
        return
    def WM_KEY_DOWN(self):
        if self.wParam==wf.S_KEY:
            self.vwin.variables.S_key_last=wf.S_KEY
        if self.wParam==wf.A_KEY:
            self.vwin.variables.A_key_last=wf.A_KEY
        if self.wParam==wf.D_KEY:
            self.vwin.variables.D_key_last=wf.D_KEY
        if self.wParam==wf.W_KEY:
            self.vwin.variables.W_key_last=wf.W_KEY
        if self.wParam==wf.Z_KEY:
            self.vwin.variables.Z_key_last=wf.Z_KEY
        if self.wParam==wf.E_KEY:
            self.vwin.variables.E_key_last=wf.E_KEY
        if self.wParam==wf.Q_KEY:
            self.vwin.variables.Q_key_last=wf.Q_KEY
        if self.wParam==wf.NUM5_KEY:
            self.vwin.variables.NUM5_key_last=wf.NUM5_KEY
        if self.wParam==wf.NUM6_KEY:
            self.vwin.variables.NUM6_key_last=wf.NUM6_KEY
        if self.wParam==wf.NUM8_KEY:
            self.vwin.variables.NUM8_key_last=wf.NUM8_KEY
        if self.wParam==wf.NUM4_KEY:
            self.vwin.variables.NUM4_key_last=wf.NUM4_KEY
        if self.wParam==wf.NUM9_KEY:
            self.vwin.variables.NUM9_key_last=wf.NUM9_KEY
        if self.wParam==wf.NUM7_KEY:
            self.vwin.variables.NUM7_key_last=wf.NUM7_KEY
        if self.wParam==wf.NUM1_KEY:
            self.vwin.variables.NUM1_key_last=wf.NUM1_KEY
        return 0
    def WM_KEY_UP(self):
##        self.vwin.Player1.Animate_step(False)
##        self.vwin.Player2.Animate_step(False)
        
        if self.wParam==wf.S_KEY:
            self.vwin.variables.S_key_last=wf.S_KEY
        if self.wParam==wf.A_KEY:
            self.vwin.variables.A_key_last=wf.A_KEY
        if self.wParam==wf.D_KEY:
            self.vwin.variables.D_key_last=wf.D_KEY
        if self.wParam==wf.W_KEY:
            self.vwin.variables.W_key_last=wf.W_KEY
        if self.wParam==wf.Z_KEY:
            self.vwin.variables.Z_key_last=wf.Z_KEY
        if self.wParam==wf.E_KEY:
            self.vwin.variables.E_key_last=wf.E_KEY
        if self.wParam==wf.Q_KEY:
            self.vwin.variables.Q_key_last=wf.Q_KEY
        if self.wParam==wf.NUM5_KEY:
            self.vwin.variables.NUM5_key_last=wf.NUM5_KEY
        if self.wParam==wf.NUM6_KEY:
            self.vwin.variables.NUM6_key_last=wf.NUM6_KEY
        if self.wParam==wf.NUM8_KEY:
            self.vwin.variables.NUM8_key_last=wf.NUM8_KEY
        if self.wParam==wf.NUM4_KEY:
            self.vwin.variables.NUM4_key_last=wf.NUM4_KEY
        if self.wParam==wf.NUM9_KEY:
            self.vwin.variables.NUM9_key_last=wf.NUM9_KEY
        if self.wParam==wf.NUM7_KEY:
            self.vwin.variables.NUM7_key_last=wf.NUM7_KEY
        if self.wParam==wf.NUM1_KEY:
            self.vwin.variables.NUM1_key_last=wf.NUM1_KEY
        return 0
        
    def WM_KEY_PRESS(self):
        ##PLAYER1 KEYS##
        if self.wParam==wf.S_KEY_DOWN or self.vwin.variables.S_key_last==wf.S_KEY_DOWN:
            self.vwin.variables.S_key_last=wf.S_KEY_DOWN
            self.vwin.variables.player1_direction="down"
        if self.wParam==wf.A_KEY_DOWN or self.vwin.variables.S_key_last==wf.A_KEY_DOWN:
            self.vwin.variables.A_key_last=wf.A_KEY_DOWN
            self.vwin.variables.player1_direction="left"
        if self.wParam==wf.D_KEY_DOWN or self.vwin.variables.D_key_last==wf.D_KEY_DOWN:
            self.vwin.variables.D_key_last=wf.D_KEY_DOWN
            self.vwin.variables.player1_direction="right"
        if self.wParam==wf.W_KEY_DOWN or self.vwin.variables.W_key_last==wf.W_KEY_DOWN:
            self.vwin.variables.W_key_last=wf.W_KEY_DOWN
            self.vwin.variables.player1_direction="up"
        if self.wParam==wf.Z_KEY_DOWN or self.vwin.variables.Z_key_last==wf.Z_KEY_DOWN:
            self.vwin.variables.Z_key_last=wf.Z_KEY_DOWN
        if self.wParam==wf.E_KEY_DOWN or self.vwin.variables.E_key_last==wf.E_KEY_DOWN:
            self.vwin.variables.E_key_last=wf.E_KEY_DOWN
        if self.wParam==wf.Q_KEY_DOWN or self.vwin.variables.Q_key_last==wf.Q_KEY_DOWN:
            self.vwin.variables.Q_key_last=wf.Q_KEY_DOWN
            self.vwin.variables.Tool_Sel.Player1_selection=(self.vwin.variables.Tool_Sel.Player1_selection+1)%2
            self.vwin.Player1.Tool_selection=self.vwin.variables.Tool_Sel.Player1_selection                 

        ##PLAYER2 KEYS##
        if self.wParam==wf.NUM5_KEY_DOWN or self.vwin.variables.NUM5_key_last==wf.NUM5_KEY_DOWN:
            self.vwin.variables.NUM5_key_last=wf.NUM5_KEY_DOWN
            self.vwin.variables.player2_direction="down"
        if self.wParam==wf.NUM4_KEY_DOWN or self.vwin.variables.NUM4_key_last==wf.NUM4_KEY_DOWN:
            self.vwin.variables.NUM4_key_last=wf.NUM4_KEY_DOWN
            self.vwin.variables.player2_direction="left"
        if self.wParam==wf.NUM6_KEY_DOWN or self.vwin.variables.NUM6_key_last==wf.NUM6_KEY_DOWN:
            self.vwin.variables.NUM6_key_last=wf.NUM6_KEY_DOWN
            self.vwin.variables.player2_direction="right"
        if self.wParam==wf.NUM8_KEY_DOWN or self.vwin.variables.NUM8_key_last==wf.NUM8_KEY_DOWN:
            self.vwin.variables.NUM8_key_last=wf.NUM8_KEY_DOWN
            self.vwin.variables.player2_direction="up"
        if self.wParam==wf.NUM1_KEY_DOWN or self.vwin.variables.NUM1_key_last==wf.NUM1_KEY_DOWN:
            self.vwin.variables.NUM1_key_last=wf.NUM1_KEY_DOWN
        if self.wParam==wf.NUM9_KEY_DOWN or self.vwin.variables.NUM9_key_last==wf.NUM9_KEY_DOWN:
            self.vwin.variables.NUM9_key_last=wf.NUM9_KEY_DOWN
        if self.wParam==wf.NUM7_KEY_DOWN or self.vwin.variables.NUM7_key_last==wf.NUM7_KEY_DOWN:
            self.vwin.variables.NUM7_key_last=wf.NUM7_KEY_DOWN
            self.vwin.variables.Tool_Sel.Player2_selection=(self.vwin.variables.Tool_Sel.Player2_selection+1)%2
            self.vwin.Player2.Tool_selection=self.vwin.variables.Tool_Sel.Player2_selection                 
        return
    
    def Move(self):
        ##Update Player Position##
        inputs1=[self.vwin.variables.S_key_last==wf.S_KEY_DOWN,
                 self.vwin.variables.W_key_last==wf.W_KEY_DOWN,
                 self.vwin.variables.A_key_last==wf.A_KEY_DOWN,
                 self.vwin.variables.D_key_last==wf.D_KEY_DOWN,
                 self.vwin.variables.Z_key_last==wf.Z_KEY_DOWN]
        Player1_keypress=(self.vwin.variables.E_key_last==wf.E_KEY_DOWN)
        inputs2=[self.vwin.variables.NUM5_key_last==wf.NUM5_KEY_DOWN,
                 self.vwin.variables.NUM8_key_last==wf.NUM8_KEY_DOWN,
                 self.vwin.variables.NUM4_key_last==wf.NUM4_KEY_DOWN,
                 self.vwin.variables.NUM6_key_last==wf.NUM6_KEY_DOWN,
                 self.vwin.variables.NUM1_key_last==wf.NUM1_KEY_DOWN]
        Player2_keypress=(self.vwin.variables.NUM9_key_last==wf.NUM9_KEY_DOWN)
        objects=[[self.vwin.Tree1,"T"],
                 [self.vwin.Wall1[0],"W"],
                 [self.vwin.Wheat1,"F"],
                 [self.vwin.Player1,"P0-"],
                 [self.vwin.Player2,"P1-"],
                 [self.vwin.Player3,"P2-"],
                 [self.vwin.Player4,"P3-"]]
        self.vwin.Player1.resource=self.resource
        self.resource=self.vwin.Player1.Move(inputs1,self.map_all,objects,Player1_keypress)
        self.vwin.Player2.resource=self.resource
        self.resource=self.vwin.Player2.Move(inputs2,self.map_all,objects,Player2_keypress)
        self.vwin.variables.Num_trees_cut=self.resource["Tree"]
        self.vwin.variables.Num_wheat_harvested=self.resource["Wheat"]
        self.vwin.Player3.Auto_Move(self.map_all,objects)
        self.vwin.Player4.Auto_Move(self.map_all,objects)
##        MOVE(self.vwin,self.map_all)

    def Update_Statsblock(self):
        UPDATE_STATSBLOCK(self.vwin)
        return
    
    def Update_mem_background(self,player):
        UPDATE_MEM_BACKGROUND(player,self.vwin,self.map_all)
        return 0
    
    def Update_windows(self):
        ##PLAYER1##
        self.Update_mem_background(0)                           ##Update the background
        windll.gdi32.BitBlt(self.vwin.dict_background_hdc["mem_main_show"],0,0,wf.main_window_w,wf.main_window_h,                            ##Place the players window in memory
                            self.vwin.dict_background_hdc["mem_main1"],POINT(),wf.SRCCOPY)
        ##PLAYER2##
        self.Update_mem_background(1)                           ##Update the background
        windll.gdi32.BitBlt(self.vwin.dict_background_hdc["mem_main_show"],800,0,wf.main_window_w,wf.main_window_h,                          ##Copy the players window in memory
                            self.vwin.dict_background_hdc["mem_main2"],POINT(),wf.SRCCOPY)
        ##ADD STATS BLOCK##
        windll.gdi32.BitBlt(self.vwin.dict_background_hdc["mem_main_show"],800-int(wf.stats_block_w/2),0,wf.stats_block_w,wf.stats_block_h,  ##Add the stats block in memory
                            self.vwin.dict_background_hdc["stats_block"],POINT(),wf.SRCCOPY)
        windll.gdi32.BitBlt(self.vwin.variables.hdc_show,0,0,wf.main_window_w*2,wf.main_window_h,                                       ##Display the memory hdc
                            self.vwin.dict_background_hdc["mem_main_show"],POINT(),wf.SRCCOPY)
        return 0
