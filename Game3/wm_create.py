##THIS FUNCTION INITIALIZES THE VARIABLES##
#Also known as wm_create.py
import window_functions as wf
import window_structures as ws
from Tree1_Sprite import Tree_Sprite_1
from Wall_Sprite_1 import Wall_Sprite_1
from Player1_Sprite import Player1_Sprite
from Player2_Sprite import Player2_Sprite
from ctypes import *
from ctypes.wintypes import *

def WM_CREATE(cs,hwnd,map_all):##USE CLASS VARIABLES
    file_path_main="C:\\Users\\fredstile\\Documents\\GitHub\\openGL\\images\\"
    ###################
    ##IMPORT PICTURES##
    ###################
    cs.variables.hdc_show=windll.user32.GetDC(hwnd)    ##Create the reference hdc from the window
    #Find CHARACTER Files#
    character1_down_file="Face_forward_1a.bmp"
    character1_up_file="Face_backward_1a.bmp"
    character1_right_file="Face_right_1a.bmp"
    character1_left_file="Face_left_1a.bmp"
    character2_down_file="Face_forward_2a.bmp"
    character2_up_file="Face_backward_2a.bmp"
    character2_right_file="Face_right_2a.bmp"
    character2_left_file="Face_left_2a.bmp"
    cs.dict_character_files={"character1_down":character1_down_file,"character1_up":character1_up_file,"character1_right":character1_right_file,"character1_left":character1_left_file,
                     "character2_down":character2_down_file,"character2_up":character2_up_file,"character2_right":character2_right_file,"character2_left":character2_left_file}
    #Load character files, assign pointers, and store pointers in dictionary
    for i in range(8):
        file=cs.dict_character_index[i]
        hbmp=cs.dict_character_index[i]
        hdc=cs.dict_character_index[i]
        cs.dict_character_hbmp[hbmp]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+cs.dict_character_files[file]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        ##Create HDC##
        cs.dict_character_hdc[hdc]=windll.gdi32.CreateCompatibleDC(cs.variables.hdc_show)   #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(cs.dict_character_hdc[hdc],cs.dict_character_hbmp[hbmp])  #Copy image into hdc
        
    cs.Player1=Player1_Sprite(cs.variables.hdc_show,file_path_main,hwnd)
    cs.Player2=Player2_Sprite(cs.variables.hdc_show,file_path_main)
    #Find GRASS files#
    grass_block1_file="Grass_1.bmp"
    grass_block2_file="Grass_2.bmp"
    grass_block1_build_file="Grass_1_build.bmp"
    cs.dict_grass_files={"grass_block1":grass_block1_file,"grass_block2":grass_block2_file,"grass_block1_build":grass_block1_build_file}
    #Load grass files, assign pointers, and store pointers in dictionary
    for i in range(3):
        file=cs.dict_grass_index[i]
        hbmp=cs.dict_grass_index[i]
        hdc=cs.dict_grass_index[i]
        cs.dict_grass_hbmp[hbmp]=wf.LoadImage(c_void_p(),LPCWSTR(file_path_main+cs.dict_grass_files[file]),wf.IMAGE_BITMAP,0,0,8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)
        ##Create HDC##
        cs.dict_grass_hdc[hdc]=windll.gdi32.CreateCompatibleDC(cs.variables.hdc_show)   #Make hdc similar to the reference hdc
        windll.gdi32.SelectObject(cs.dict_grass_hdc[hdc],cs.dict_grass_hbmp[hbmp])      #Copy image into hdc

    #Load OBJECTS#
    cs.Tree1=Tree_Sprite_1(cs.variables.hdc_show,file_path_main)
    cs.Wall1=Wall_Sprite_1(cs.variables.hdc_show,file_path_main)

    #Find Button and Token files#
    red_button_file="Red_button.bmp"
    purple_button_file="Purple_button.bmp"
    tree_token_file="Tree_token.bmp"
    axe_token_file="Axe_token_2.bmp"
    empty_hand_token_file="Empty_hand_token.bmp"
    cs.dict_token_files={"red_button":red_button_file,"purple_button":purple_button_file,"tree_token":tree_token_file,"axe_token":axe_token_file,"empty_hand_token":empty_hand_token_file}
    #Load button and token files, assign pointers, and store pointers in dictionary
    for i in range(5):
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
    Points=wf.REGION(34)
    cs.variables.Object_Rgn.Region_wall[0]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)
    Points=wf.REGION(35)
    cs.variables.Object_Rgn.Region_wall[1]=wf.CreatePolygonRgn(Points,len(Points),wf.WINDING)

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
                map_all[i][j]="G1T---"
            elif i==5 and j>10 and j<20:
                map_all[i][j]="G1--B1"
            else:
                map_all[i][j]="G1----"
    map_all[5][5]="G1T---"                      ##Temporary tree for testing
    cs.variables.player_window[0]=False           #backgrounds have not been updated
    cs.variables.player_window[1]=False
    cs.variables.player_window_ULtile[0]=POINT()
    cs.variables.player_window_ULtile[1]=POINT()
    cs.variables.tree_token=False

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
    windll.user32.SetRect(pointer(cs.variables.rcStats[0]),0,0,wf.button_w+30, wf.button_h+18)   #For tree resource counter
    wf.ShiftRect(cs.variables.rcStats[0],wf.token_w*2,int(wf.token_h/3))
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
    ##CREATE TARGET BOXES##
    ##Facing right
    cs.variables.Wall_target_boxes[0].WallUL=POINT(0,0)
    cs.variables.Wall_target_boxes[0].WallUR=POINT(wf.wall_vertical_w,0)
    cs.variables.Wall_target_boxes[0].WallLL=POINT(0,wf.tile_h)
    cs.variables.Wall_target_boxes[0].WallLL=POINT(wf.wall_vertical_w,wf.tile_h)
    ##Facing left
    cs.variables.Wall_target_boxes[1].WallUL=POINT(wf.tile_w-wf.wall_vertical_w,0)
    cs.variables.Wall_target_boxes[1].WallUR=POINT(wf.tile_w,0)
    cs.variables.Wall_target_boxes[1].WallLL=POINT(wf.tile_w-wf.wall_vertical_w,wf.tile_h)
    cs.variables.Wall_target_boxes[1].WallLL=POINT(wf.tile_w,wf.tile_h)
    ##Facing up
    cs.variables.Wall_target_boxes[2].WallUL=POINT(0,wf.tile_h-int(wf.wall_horizontal_h/4))
    cs.variables.Wall_target_boxes[2].WallUR=POINT(wf.tile_w,wf.tile_h-int(wf.wall_horizontal_h/4))
    cs.variables.Wall_target_boxes[2].WallLL=POINT(0,wf.tile_h)
    cs.variables.Wall_target_boxes[2].WallLL=POINT(wf.tile_w,wf.tile_h)
    ##Facing down
    cs.variables.Wall_target_boxes[3].WallUL=POINT(0,0)
    cs.variables.Wall_target_boxes[3].WallUR=POINT(wf.tile_w,0)
    cs.variables.Wall_target_boxes[3].WallLL=POINT(0,int(wf.wall_horizontal_h/4))
    cs.variables.Wall_target_boxes[3].WallLL=POINT(wf.tile_w,int(wf.wall_horizontal_h/4))
    
    return
    
##
##test2=ws.Variables_and_dictionaries()
##map_all=wf.ARRAY_CREATE(int(wf.map_w/200),int(wf.map_h/200))
##test=WM_CREATE(test2,None,map_all)

