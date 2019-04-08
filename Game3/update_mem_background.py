##THIS FUNCTION UPDATES THE BACKGROUNDS FOR THE DIFFERENT PLAYERS##
##All tiles and objects are displayed in the background
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *

def UPDATE_MEM_BACKGROUND(player,cs,map_all):       #It takes in the class variables and the player to be updated
    ##TRANSLATOR FOR MAP CODE TO TILE INDEX##
    tiles={"G1":"grass_block1","G2":"grass_block2","G3":"grass_block3"}
    tiles_build={"G1":"grass_block1_build","G2":"grass_block2","G3":"grass_block3"}
    Player_selection={0:cs.variables.Tool_Sel.Player1_selection,1:cs.variables.Tool_Sel.Player2_selection}          ##Define dictionary for selected player tool
    Player_window={0:cs.variables.Player1_window,1:cs.variables.Player2_window}
    Player_window0={0:cs.Player1,1:cs.Player2}
    key_last={0:cs.variables.E_key_last,1:cs.variables.NUM9_key_last}                                               ##Define dictionary for keys pressed
    KEY_DOWN={0:wf.E_KEY_DOWN,1:wf.NUM9_KEY_DOWN}                                                                   ##Define dictionary for key down code
    button_text="E9"                                                                                                ##Define list of characters for printing on the buttons

    Player_direction={0:cs.variables.player1_direction,1:cs.variables.player2_direction}                            ##Define dictionary to track player directions
    ##IDENTIFY THE REFERENCE TILE IN THE UPPER LEFT CORNER
    Player_window[player].windowUL.x=Player_window0[player].position.x
    Player_window[player].windowUL.y=Player_window0[player].position.y
    shiftx=int((Player_window[player].windowUL.x-wf.shiftx)/wf.tile_w)
    shifty=int((Player_window[player].windowUL.y-wf.shifty)/wf.tile_h)
    ##STORE PREVIOUS REFERENCE TILE AND RECORD CURRENT REFERENCE
    temp_tile=POINT(cs.variables.player_window_ULtile[player].x,cs.variables.player_window_ULtile[player].y)
    cs.variables.player_window_ULtile[player]=POINT(shiftx,shifty)
    ##Decide whether an update is needed, is there an empty column or is a refresh requested
    if (abs(temp_tile.x-cs.variables.player_window_ULtile[player].x)>=1 or abs(temp_tile.y-cs.variables.player_window_ULtile[player].y)>=1) or cs.variables.player_window[player]==False:
        for i in range(int(wf.backgrnd_window_w/wf.tile_w)):
            for j in range(int(wf.backgrnd_window_h/wf.tile_h)):
                ##DEFINE CURRENT GRID POSITION##
                grid_position_x=shiftx+i
                grid_position_y=shifty+j
                ##DETERMINE TILES AND OBJECTS## GGOOBPCC
                if grid_position_x<len(map_all) and grid_position_y<len(map_all[0]):
                    temp=map_all[grid_position_x][grid_position_y]
                    ##ADD TILE##
                    position=POINT(i*wf.tile_w,j*wf.tile_h)
                    if Player_selection[player]==wf.Empty_Hand or map_all[grid_position_x][grid_position_y][6]!="-":
                        windll.gdi32.BitBlt(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],position,
                                        wf.tile_w,wf.tile_h,cs.dict_grass_hdc[tiles_build[temp[0:2]]],0,0,wf.SRCCOPY)
                    else:
                        windll.gdi32.BitBlt(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],position,
                                            wf.tile_w,wf.tile_h,cs.dict_grass_hdc[tiles[temp[0:2]]],0,0,wf.SRCCOPY)
    player1_drawn=False
    player2_drawn=False
    characters=[cs.Player1,cs.Player2,cs.Player3]
    characters2=[cs.Player1,cs.Player2,cs.Player3]
    ##Sort Characters##
    ###################################
    ####---------------------------####
    ####SORTER NEEDS TO BE IMPROVED####
    ####---------------------------####
    ###################################
    temp=None
    minimum_prev=None
    minimum=characters[0]
    for i in range(len(characters)):
        ##Find minimum then remove
        minimum=characters2[0]
        for j in characters2:
            if j.Target_box()[3].y<minimum.Target_box()[3].y:
                ##Check sorted list##
                check=False
                if temp!=None:
                    for k in temp:
                        if k.Character==j.Character:
                            check=True
                if check==False:
                    minimum=j
        ##Create sorted list
        if temp==None:
            temp=[minimum]
        else:
            temp.append(minimum)
        ##Remove from characters2
        characters2=None
        for j in range(len(characters)):
            check=False
            for k in range(len(temp)):
                if characters[j].Character==temp[k].Character:
                    check=True
            if check==False:
                if characters2==None:
                    characters2=[characters[j]]
                else:
                    characters2.append(characters[j])
                    
    ##Return temp list
    for i in range(len(temp)):
        if characters2==None:
            characters2=[temp[0]]
        else:
            characters2.append(temp[i])
    ##Initialize counter for sorting list
    count=0
    ##Object in order of layers with respect to upper box position##
    objectorder={0:cs.Wall1[3],1:cs.Tree1,2:cs.Wall1[0],3:cs.Wall1[1],4:cs.Wall1[2],5:cs.Build_Button1}
    if (abs(temp_tile.x-cs.variables.player_window_ULtile[player].x)>=1 or abs(temp_tile.y-cs.variables.player_window_ULtile[player].y)>=1) or cs.variables.player_window[player]==False:
        for j in range(int(wf.backgrnd_window_h/wf.tile_h)):
            count=0
            player1_drawn=False
            player2_drawn=False
            drawn=[False,False,False]
            grid_position_y=shifty+j
            ##Objects in order of layers with respective upper box position##
            upperbound={0:cs.Wall1[3].Target_box(0,grid_position_y*wf.tile_h,3)[3].y,1:cs.Tree1.Target_box(0,grid_position_y*wf.tile_h)[3].y,
                        2:cs.Wall1[0].Target_box(0,grid_position_y*wf.tile_h,0)[3].y,3:cs.Wall1[1].Target_box(0,grid_position_y*wf.tile_h,1)[3].y,
                        4:cs.Wall1[2].Target_box(0,grid_position_y*wf.tile_h,2)[3].y}
            for k in objectorder:
                for i in range(int(wf.backgrnd_window_w/wf.tile_w)):
                    ##DEFINE CURRENT GRID POSITION##
                    grid_position_x=shiftx+i
                    if grid_position_x<len(map_all) and grid_position_y<len(map_all[0]):
                        temp=map_all[grid_position_x][grid_position_y]
                        ##ADD OBJECTS AND BUTTONS##
                        objectorder[k].Draw(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],temp,i*wf.tile_w,j*wf.tile_w,characters[player])
                ##Draw Characters in order of the sorted list##
                while count<len(characters2):
                    if characters2[count].Target_box()[3].y>upperbound[k] and drawn[count]==False:
                        characters2[count].Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
                                                          cs.variables.player_window_ULtile[player])
                        drawn[count]=True
                        count=count+1
                    else:
                        count=count+1


        else:
            cs.variables.player1_window=True
        ##PLACE BACKGROUND IN PLAYER WINDOW##
        shiftedUL=POINT()
        shiftedUL.x=(Player_window[player].windowUL.x-wf.shiftx)%wf.tile_w                  ##Determines how much the background needs to shift in x in relation to player window
        shiftedUL.y=(Player_window[player].windowUL.y-wf.shifty)%wf.tile_h                  ##Determines how much the background needs to shift in y in relation to player window
        windll.gdi32.BitBlt(cs.dict_background_hdc["mem_main"+str(player+1)],POINT(),       ##Copy background into window
                            wf.backgrnd_window_w,wf.backgrnd_window_h,
                            cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
                            shiftedUL,wf.SRCCOPY)
        
    return 0
