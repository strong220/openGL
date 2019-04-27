##THIS FUNCTION INITIALIZES THE VARIABLES##
#Also known as wm_create.py
import window_functions as wf
import window_structures as ws
from Tree1_Sprite import Tree_Sprite_1
from Wheat1_Sprite import Wheat_Sprite_1
from Wall_Sprite_1 import Wall_Sprite_1
from Barrel_Sprite import Barrel_Sprite_1
from Build_Button_Sprite_1 import Build_Button_Sprite_1
from ctypes import *
from ctypes.wintypes import *
from Character_Sprite_Main import *
from Character1 import Character1_Sprite
from Character2 import Character2_Sprite
from CPU_Character1 import CPU_Character1_Sprite

def WM_CREATE(cs,hwnd,map_all):##USE CLASS VARIABLES
    print("loading all variables")
    file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\"
    ###################
    ##IMPORT PICTURES##
    ###################
    cs.variables.hdc_show=windll.user32.GetDC(hwnd)    ##Create the reference hdc from the window
    #Find CHARACTER Files#
    cs.Player1=Character1_Sprite(cs.variables.hdc_show,file_path_main,hwnd,"0-")
    cs.Player1.Tool_selection=wf.Axe
    cs.Player1.position.x=800
    cs.Player2=Character2_Sprite(cs.variables.hdc_show,file_path_main,hwnd,"1-")
    cs.Player2.Tool_selection=wf.Axe
    cs.Player3=CPU_Character1_Sprite(cs.variables.hdc_show,file_path_main,hwnd,"2-")
    cs.Player3.Tool_selection=wf.Axe
    cs.Player4=CPU_Character1_Sprite(cs.variables.hdc_show,file_path_main,hwnd,"3-")
    cs.Player4.position=POINT(cs.Player4.position.x+600,cs.Player4.position.y)
    cs.Player4.Tool_selection=wf.Axe
    #Find GRASS files#
    grass_block1_file="Grass_1.bmp"
    grass_block2_file="Grass_2.bmp"
    grass_block3_file="Grass_3.bmp"
    grass_block1_build_file="Grass_1_build.bmp"
    dirt_block1_file="Dirt_1.bmp"
    dirt_block1_build_file="Dirt_1_build.bmp"
    cs.dict_grass_files={"grass_block1":grass_block1_file,"grass_block2":grass_block2_file,"grass_block3":grass_block3_file,"grass_block1_build":grass_block1_build_file,"dirt_block1":dirt_block1_file,"dirt_block1_build":dirt_block1_build_file}
    #Load grass files, assign pointers, and store pointers in dictionary
    for i in range(6):
        file=cs.dict_grass_index[i]
        hbmp=cs.dict_grass_index[i]
        hdc=cs.dict_grass_index[i]
        cs.dict_grass_hbmp[hbmp]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+cs.dict_grass_files[file]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        ##Create HDC##
        cs.dict_grass_hdc[hdc]=windll.gdi32.CreateCompatibleDC(cs.variables.hdc_show)   #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(cs.dict_grass_hdc[hdc],cs.dict_grass_hbmp[hbmp])      #Copy image into hdc

    #Load OBJECTS#
    cs.Tree1=Tree_Sprite_1(cs.variables.hdc_show,file_path_main)
    cs.Wheat1=Wheat_Sprite_1(cs.variables.hdc_show,file_path_main)
    cs.Wheat_Barrel=Barrel_Sprite_1(cs.variables.hdc_show,file_path_main)
    cs.Wall1=[Wall_Sprite_1(cs.variables.hdc_show,file_path_main,0),Wall_Sprite_1(cs.variables.hdc_show,file_path_main,1),Wall_Sprite_1(cs.variables.hdc_show,file_path_main,2),Wall_Sprite_1(cs.variables.hdc_show,file_path_main,3)]
    cs.Build_Button1=Build_Button_Sprite_1(cs.variables.hdc_show,file_path_main)

    #Find Button and Token files#
    red_button_file="Red_button.bmp"
    purple_button_file="Purple_button.bmp"
    tree_token_file="Tree_token.bmp"
    axe_token_file="Axe_token_2.bmp"
    wheat_token_file="Wheat_token.bmp"
    empty_hand_token_file="Empty_hand_token.bmp"
    stamina_file="Stamina_meter_1a.bmp"
    cs.dict_token_files={"red_button":red_button_file,"purple_button":purple_button_file,"tree_token":tree_token_file,"axe_token":axe_token_file,"empty_hand_token":empty_hand_token_file,"stamina_meter":stamina_file,"wheat_token":wheat_token_file}
    #Load button and token files, assign pointers, and store pointers in dictionary
    for i in range(7):
        file=cs.dict_token_index[i]
        hbmp=cs.dict_token_index[i]
        hdc=cs.dict_token_index[i]
        cs.dict_token_hbmp[hbmp]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+cs.dict_token_files[file]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        ##Create HDC##
        cs.dict_token_hdc[hdc]=windll.gdi32.CreateCompatibleDC(cs.variables.hdc_show)   #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(cs.dict_token_hdc[hdc],cs.dict_token_hbmp[hbmp])      #Copy image into hdc

    #Find background files#
    large_background_file="Total_temp.bmp"
    small_background_file="Temp_Background.bmp"
    statsblock_file="stats_background.bmp"
    cs.dict_background_files={"total_background":large_background_file,"mem_backgrnd1":small_background_file,"mem_backgrnd2":small_background_file,"mem_main1":small_background_file,
                              "mem_main2":small_background_file,"mem_main_show":large_background_file,"stats_block":statsblock_file}
    #Load background, assign pointers, and store pointers in dictionary
    for i in range(7):
        file=cs.dict_background_index[i]
        hbmp=cs.dict_background_index[i]
        hdc=cs.dict_background_index[i]
        cs.dict_background_hbmp[hbmp]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+cs.dict_background_files[file]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        ##Create HDC##
        cs.dict_background_hdc[hdc]=windll.gdi32.CreateCompatibleDC(cs.variables.hdc_show)      #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(cs.dict_background_hdc[hdc],cs.dict_background_hbmp[hbmp])    #Copy image into hdc

    ###############
    ##SET REGIONS##
    ###############
    ##For Character 1##
    Points=wf.REGION(1)
    temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    cs.variables.Player1_animation_Rgn.down[0]=temp
    for i in range(2,9):
        Points=wf.REGION(i)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(cs.variables.Player1_animation_Rgn.down[0],cs.variables.Player1_animation_Rgn.down[0],temp,wf.RGN_OR)
    Points=wf.REGION(9)
    cs.variables.Player1_animation_Rgn.right[0]= wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    for i in range(10,14):
        Points=wf.REGION(i)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(cs.variables.Player1_animation_Rgn.right[0],cs.variables.Player1_animation_Rgn.right[0],temp,wf.RGN_OR)
    Points=wf.REGION(14)
    cs.variables.Player1_animation_Rgn.left[0]= wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    for i in range(15,19):
        Points=wf.REGION(i)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(cs.variables.Player1_animation_Rgn.left[0],cs.variables.Player1_animation_Rgn.left[0],temp,wf.RGN_OR)
    Points=wf.REGION(19)
    cs.variables.Player1_animation_Rgn.up[0]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    for i in range(20,27):
        Points=wf.REGION(i)
        temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
        windll.gdi32.CombineRgn(cs.variables.Player1_animation_Rgn.up[0],cs.variables.Player1_animation_Rgn.up[0],temp,wf.RGN_OR)
    ##For character 2##
    Points=wf.REGION(27)
    temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    cs.variables.Player2_animation_Rgn.down[0]=temp
    windll.gdi32.CombineRgn(cs.variables.Player2_animation_Rgn.down[0],cs.variables.Player1_animation_Rgn.down[0],temp,wf.RGN_OR) ##add hair
    Points=wf.REGION(28)
    temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    cs.variables.Player2_animation_Rgn.up[0]=temp
    windll.gdi32.CombineRgn(cs.variables.Player2_animation_Rgn.up[0],cs.variables.Player1_animation_Rgn.up[0],temp,wf.RGN_OR) ##add hair
    Points=wf.REGION(29)
    temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    cs.variables.Player2_animation_Rgn.right[0]=temp
    windll.gdi32.CombineRgn(cs.variables.Player2_animation_Rgn.right[0],cs.variables.Player1_animation_Rgn.right[0],temp,wf.RGN_OR) ##add hair
    Points=wf.REGION(30)
    temp=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    cs.variables.Player2_animation_Rgn.left[0]=temp
    windll.gdi32.CombineRgn(cs.variables.Player2_animation_Rgn.left[0],cs.variables.Player1_animation_Rgn.left[0],temp,wf.RGN_OR) ##add hair
    ##Object Regions
    Points=wf.REGION(31)
    cs.variables.Object_Rgn.Region_tree[0]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    cs.variables.Region_button=windll.gdi32.CreateEllipticRgn(0,0,31,31)
    windll.user32.SetRect(pointer(cs.variables.rcText),0,0,wf.button_w, wf.button_h)
    Points=wf.REGION(32)
    cs.variables.Region_token[0]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    Points=wf.REGION(33)
    cs.variables.Region_token[1]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    Points=wf.REGION(37)
    cs.variables.Region_token[4]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)         ##Define Region for the wheat token
    windll.gdi32.OffsetRgn(cs.variables.Region_token[4],0,wf.token_h)                           ##Shift the clipping region
    Points=wf.REGION(34)
    cs.variables.Object_Rgn.Region_wall[0]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    Points=wf.REGION(35)
    cs.variables.Object_Rgn.Region_wall[1]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    ##Stanima Region
    Points=wf.REGION(36)
    cs.variables.Region_token[3]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)

    ##################################
    ##INITIALIZE REMAINING VARIABLES##
    ##################################
    cs.variables.player1_direction="down"
    cs.variables.player2_direction="down"

    ##INITIALIZE BACKGROUND##
    cs.variables.Bkgnd_red_button=windll.gdi32.GetPixel(cs.dict_token_hdc["red_button"],10,10)
    cs.variables.Bkgnd_purple_button=windll.gdi32.GetPixel(cs.dict_token_hdc["purple_button"],10,10)
    windll.gdi32.SetBkColor(cs.dict_background_hdc["mem_backgrnd1"],cs.variables.Bkgnd_red_button)
    windll.gdi32.SetBkColor(cs.dict_background_hdc["mem_backgrnd2"],cs.variables.Bkgnd_red_button)
    ##GGOOBP##
    for i in range(int(wf.map_w/200)):
        for j in range(int(wf.map_h/200)):
            if i==0 or j==0 or i==int(wf.map_w/200)-1 or j==int(wf.map_h/200)-1:
                map_all[i][j]="G1T-----"
            elif i==5 and j>10 and j<20:
                map_all[i][j]="D1F-----"
            else:
                map_all[i][j]="G1------"
    map_all[5][5]="G1T-----"                      ##Temporary tree for testing
    cs.variables.player_window[0]=False           #backgrounds have not been updated
    cs.variables.player_window[1]=False
    cs.variables.player_window_ULtile[0]=POINT()
    cs.variables.player_window_ULtile[1]=POINT()
    cs.variables.tree_token=False
    cs.variables.wheat_token=False

    ##INITIALIZE CHARACTER POSITIONS##
    cs.variables.Player1_window.windowUL.x=wf.shiftx+100
    cs.variables.Player1_window.windowUL.y=wf.shifty+100
    cs.variables.Player1_window.windowLR.x=wf.shiftx+wf.character_width+100
    cs.variables.Player1_window.windowLR.y=wf.shifty+wf.character_height+100
    cs.variables.Region_player1=windll.gdi32.CreateRectRgn(0,0,wf.character_width,wf.character_height)  ##Initialize hit box for collisions##
    cs.variables.Player2_window.windowUL.x=wf.shiftx+100
    cs.variables.Player2_window.windowUL.y=wf.shifty+100
    cs.variables.Player2_window.windowLR.x=wf.shiftx+wf.character_width+100
    cs.variables.Player2_window.windowLR.y=wf.shifty+wf.character_height+100
    ##INITIALIZE SELECTION BOXES##
    windll.user32.SetRect(pointer(cs.variables.rcStats[0]),0,0,30,18)   #For tree resource counter
    wf.ShiftRect(cs.variables.rcStats[0],wf.token_w*2,int(wf.token_h/3))
    windll.user32.SetRect(pointer(cs.variables.rcStats[1]),0,0,10,100)   #For Stamina Bar for player 1
    wf.ShiftRect(cs.variables.rcStats[1],int(wf.token_w/2),int(wf.token_h*5))
    windll.user32.SetRect(pointer(cs.variables.rcStats[2]),0,0,10,100)   #For Stamina Bar for player 2
    wf.ShiftRect(cs.variables.rcStats[2],wf.stats_block_w-int(wf.token_w/2),int(wf.token_h*5))
    windll.user32.SetRect(pointer(cs.variables.rcStats[3]),0,0,30,18)   #For tree resource counter
    wf.ShiftRect(cs.variables.rcStats[3],wf.token_w*2,int(wf.token_h/3)+wf.token_h)
    cs.variables.Fill_color=windll.gdi32.CreateSolidBrush(wf.RGB(150,0,0))
    cs.variables.Fill_color2=windll.gdi32.CreateSolidBrush(wf.RGB(0,0,0))
    #For Tools
    ##player1
    windll.user32.SetRect(pointer(cs.variables.Tool_Sel.rcSelect_player1[0]),10,10*wf.token_h,wf.token_w+10+1,10*wf.token_h+wf.token_h+1)
    windll.user32.SetRect(pointer(cs.variables.Tool_Sel.rcSelect_player1[1]),10,11*wf.token_h+4,wf.token_w+10+1,11*wf.token_h+wf.token_h+5)
    ##player2
    space_between=wf.stats_block_w-wf.token_w-20
    windll.user32.SetRect(pointer(cs.variables.Tool_Sel.rcSelect_player2[0]),10+space_between,10*wf.token_h+1,wf.token_w+10+space_between+1,10*wf.token_h+wf.token_h+1)
    windll.user32.SetRect(pointer(cs.variables.Tool_Sel.rcSelect_player2[1]),10+space_between,11*wf.token_h+4,wf.token_w+10+space_between+1,11*wf.token_h+wf.token_h+5)
    cs.variables.hpenDot=windll.gdi32.CreatePen(wf.PS_DOT,2,wf.RGB(150,0,0))
    cs.variables.hpenDot_black=windll.gdi32.CreatePen(wf.PS_DOT,2,wf.RGB(0,0,0))
    windll.gdi32.SelectObject(cs.dict_background_hdc["stats_block"],cs.variables.hpenDot)
    cs.variables.axe_displayed=False
    cs.variables.Tool_Sel.Player1_selection=0
    cs.variables.Tool_Sel.Player2_selection=0
    cs.variables.Tool_Sel.Player1_prev_selection=0
    cs.variables.Tool_Sel.Player2_prev_selection=0
    cs.variables.Player1_chop=False
    cs.variables.Player1_button=False
    cs.variables.Player2_button=False    
    return
    
##
##test2=ws.Variables_and_dictionaries()
##map_all=wf.ARRAY_CREATE(int(wf.map_w/200),int(wf.map_h/200))
##test=WM_CREATE(test2,None,map_all)

