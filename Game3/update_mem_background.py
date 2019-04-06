##THIS FUNCTION UPDATES THE BACKGROUNDS FOR THE DIFFERENT PLAYERS##
##All tiles and objects are displayed in the background
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *

def UPDATE_MEM_BACKGROUND(player,cs,map_all):       #It takes in the class variables and the player to be updated
    ##TRANSLATOR FOR MAP CODE TO TILE INDEX##
    tiles={"G1":"grass_block1","G2":"grass_block2"}
    tiles_build={"G1":"grass_block1_build","G2":"grass_block2"}
    Player_selection={0:cs.variables.Tool_Sel.Player1_selection,1:cs.variables.Tool_Sel.Player2_selection}          ##Define dictionary for selected player tool
    Player_window={0:cs.variables.Player1_window,1:cs.variables.Player2_window}
    Player_window0={0:cs.Player1,1:cs.Player2}
    key_last={0:cs.variables.E_key_last,1:cs.variables.NUM9_key_last}                                               ##Define dictionary for keys pressed
    KEY_DOWN={0:wf.E_KEY_DOWN,1:wf.NUM9_KEY_DOWN}                                                                   ##Define dictionary for key down code
    button_text="E9"                                                                                                ##Define list of characters for printing on the buttons
    direction={"right":wf.r_build,"left":wf.l_build,"up":wf.u_build,"down":wf.d_build}                              ##Define dictionary for button placement when building
    wall_direction={"right":"0","left":"1","up":"2","down":"3"}                                                     ##Define dictionary for marking walls
    wall_placement={"0":POINT(0,wf.tile_h-wf.wall_vertical_h),                                                      ##Define dictionary for where to put the walls
                   "1":POINT(wf.tile_w-wf.wall_vertical_w,wf.tile_h-wf.wall_vertical_h),
                   "2":POINT(0,wf.tile_h-wf.wall_horizontal_h),
                   "3":POINT(0,-int(wf.wall_horizontal_h*3/4))}
    wall_type={"0":"wall_vertical","1":"wall_vertical","2":"wall_horizontal","3":"wall_horizontal"}                 ##Define dictionary for choosing the correct wall hdc
    wall_width={"0":wf.wall_vertical_w,"1":wf.wall_vertical_w,"2":wf.wall_horizontal_w,"3":wf.wall_horizontal_w}
    wall_height={"0":wf.wall_vertical_h,"1":wf.wall_vertical_h,"2":wf.wall_horizontal_h,"3":wf.wall_horizontal_h}
    Player_animation_Rgn={0:cs.variables.Player1_animation_Rgn,1:cs.variables.Player2_animation_Rgn}                ##Define dictionary for character regions
    Player_Rgn={"right":Player_animation_Rgn[(player+1)%2].right,"left":Player_animation_Rgn[(player+1)%2].left,    ##Define dictionary for access directional regions
                "up":Player_animation_Rgn[(player+1)%2].up,"down":Player_animation_Rgn[(player+1)%2].down}
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
                ##DETERMINE TILES AND OBJECTS## GGOOBP
                if grid_position_x<len(map_all) and grid_position_y<len(map_all[0]):
                    temp=map_all[grid_position_x][grid_position_y]
                    ##ADD TILE##
                    position=POINT(i*wf.tile_w,j*wf.tile_h)
                    if Player_selection[player]==wf.Empty_Hand or map_all[grid_position_x][grid_position_y][6]!="-":
                        windll.gdi32.BitBlt(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],position,
                                        wf.tile_w,wf.tile_h,cs.dict_grass_hdc[tiles_build[temp[0:2]]],0,0,wf.SRCCOPY)
##                        map_all[grid_position_x][grid_position_y]=map_all[grid_position_x][grid_position_y][:6]+"--"
                    else:
                        windll.gdi32.BitBlt(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],position,
                                            wf.tile_w,wf.tile_h,cs.dict_grass_hdc[tiles[temp[0:2]]],0,0,wf.SRCCOPY)
##                        map_all[grid_position_x][grid_position_y]=map_all[grid_position_x][grid_position_y][:6]+"--"
##    cs.Player1.Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
##                                                  cs.variables.player_window_ULtile[player])
##    cs.Player2.Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
##                                                  cs.variables.player_window_ULtile[player])
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
##        print(minimum.Character,minimum_prev)
        
    count=0
##    print("list")
##    for i in range(len(characters2)):
##        print(characters2[i].Character)
    if (abs(temp_tile.x-cs.variables.player_window_ULtile[player].x)>=1 or abs(temp_tile.y-cs.variables.player_window_ULtile[player].y)>=1) or cs.variables.player_window[player]==False:
        for j in range(int(wf.backgrnd_window_h/wf.tile_h)):
            count=0
            player1_drawn=False
            player2_drawn=False
            drawn=[False,False,False]
            grid_position_y=shifty+j
            ##Objects in order of layers with respective upper box position##
            objectorder={0:"W3",1:"T-",2:"W0",3:"W1",4:"W2"}
            upperbound={0:cs.Wall1.Target_box(0,grid_position_y*wf.tile_h,3)[3].y,1:cs.Tree1.Target_box(0,grid_position_y*wf.tile_h)[3].y,2:cs.Wall1.Target_box(0,grid_position_y*wf.tile_h,0)[3].y,3:cs.Wall1.Target_box(0,grid_position_y*wf.tile_h,1)[3].y,4:cs.Wall1.Target_box(0,grid_position_y*wf.tile_h,2)[3].y}
            for k in objectorder:
                for i in range(int(wf.backgrnd_window_w/wf.tile_w)):
                    ##DEFINE CURRENT GRID POSITION##
                    grid_position_x=shiftx+i
                    if grid_position_x<len(map_all) and grid_position_y<len(map_all[0]):
                        temp=map_all[grid_position_x][grid_position_y]
                        ##ADD OBJECTS AND BUTTONS##
                        if temp[2:4]==objectorder[k]:
                            ##CHECK FOR TREE OBJECT##
                            tree_check=cs.Tree1.Draw_Tree(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],temp,i*wf.tile_w,j*wf.tile_h,Player_selection[player],player)
                            if tree_check>0:
                                ##If button has been placed check for key press if button has been drawn and remove button from map_all##
                                ##GGOOBPCC##
                                map_all[grid_position_x][grid_position_y]=temp[0:4]+"--"+temp[6:]
                                if key_last[player]==KEY_DOWN[player] and tree_check==1:
                                    map_all[grid_position_x][grid_position_y]=temp[0:2]+"----"+temp[6:]
                                    cs.variables.Num_trees_cut=cs.variables.Num_trees_cut+1
                            ##CHECK CPU##
                            tree_check=cs.Tree1.Draw_Tree(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],temp,i*wf.tile_w,j*wf.tile_h,wf.Axe,3)
                            if tree_check>0:
                                ##If button has been placed check for key press if button has been drawn and remove button from map_all##
                                ##GGOOBPCC##
                                map_all[grid_position_x][grid_position_y]=temp[0:4]+"--"+temp[6:]
##                                if key_last[player]==KEY_DOWN[player] and tree_check==1:
##                                    map_all[grid_position_x][grid_position_y]=temp[0:2]+"----"+temp[6:]
##                                    cs.variables.Num_trees_cut=cs.variables.Num_trees_cut+1
                            ##CHECK FOR WALL OBJECT##
                            wall_check=cs.Wall1.Draw_Wall(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],temp,i*wf.tile_w,j*wf.tile_w,Player_selection[player],player)
                ##Draw Characters##
                while count<len(characters2):
                    if characters2[count].Target_box()[3].y>upperbound[k] and drawn[count]==False:
                        characters2[count].Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
                                                          cs.variables.player_window_ULtile[player])
                        drawn[count]=True
                        count=count+1
                    else:
                        count=count+1
##                        print("here")
####                if cs.Player1.Target_box()[3].y>upperbound[k] and player1_drawn==False:# and (cs.Player1.Target_box()[3].y>cs.Player2.Target_box()[3].y or player2_drawn==True):
####                    cs.Player1.Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
####                                          cs.variables.player_window_ULtile[player])
####                    player1_drawn=True
##                    if cs.Player2.Target_box()[3].y>upperbound[k] and player2_drawn==False:
##                        cs.Player2.Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
##                                              cs.variables.player_window_ULtile[player])
##                        player2_drawn=True
##                else:
##                    if cs.Player2.Target_box()[3].y>upperbound[k] and player2_drawn==False:
##                        cs.Player2.Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
##                                              cs.variables.player_window_ULtile[player])
##                        player2_drawn=True
##                    if cs.Player1.Target_box()[3].y>upperbound[k] and player1_drawn==False:
##                        cs.Player1.Draw_Character(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],
##                                              cs.variables.player_window_ULtile[player])
##                        player1_drawn=True

        if Player_selection[player]==wf.Empty_Hand:
            for j in range(int(wf.backgrnd_window_h/wf.tile_h)):
                for i in range(int(wf.backgrnd_window_w/wf.tile_w)):
                    ##DEFINE CURRENT GRID POSITION##
                    grid_position_x=shiftx+i
                    grid_position_y=shifty+j
                    if grid_position_x<len(map_all) and grid_position_y<len(map_all[0]):
                        ##If there is no object and the player is building
                        temp=map_all[grid_position_x][grid_position_y]
                        if temp[2:5]=="--B":
                            ##Update position for button depending on where player is facing
                            position=POINT(direction[Player_direction[player]].x+i*wf.tile_w,
                                           direction[Player_direction[player]].y+j*wf.tile_h)
                            ##Draw Button##
                            windll.gdi32.OffsetRgn(cs.variables.Region_button,position)                                 ##Shift the region to the desired position
                            windll.gdi32.SelectClipRgn(cs.dict_background_hdc["mem_backgrnd"+str(player+1)]             ##Select the region for drawing the button
                                                       ,cs.variables.Region_button)
                            windll.gdi32.BitBlt(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],position,          ##Draw the button
                                                wf.button_w,wf.button_h,cs.dict_token_hdc["purple_button"]
                                                ,0,0,wf.SRCCOPY)
                            ##Draw Text##
                            windll.gdi32.SetBkColor(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],               ##Ensure the Background color matches the button
                                                    cs.variables.Bkgnd_purple_button)                   
                            wf.ShiftRect(cs.variables.rcText,position.x+int(wf.button_w/3),                             ##Shift the textbox to the desired spot on the button
                                         position.y+int(wf.button_h/4))
                            windll.user32.DrawTextW(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],               ##Write the button key
                                                    c_wchar_p(button_text[player]),-1,pointer(cs.variables.rcText),0)
                            wf.ShiftRect(cs.variables.rcText,-position.x-int(wf.button_w/3),                            ##Return the text box to the correct spot
                                         -position.y-int(wf.button_h/4))
                            windll.gdi32.SelectClipRgn(cs.dict_background_hdc["mem_backgrnd"+str(player+1)],None)       ##Remove the Clipping Region
                            windll.gdi32.OffsetRgn(cs.variables.Region_button,-position.x,-position.y)                  ##Return the region back to its original spot
                            ##CHECK FOR KEY PRESS##
                            if key_last[player]==KEY_DOWN[player]:
                                ##Build command##
                                if cs.variables.Num_trees_cut>=0:
                                    cs.variables.Num_trees_cut=cs.variables.Num_trees_cut-0                            ##Remove the resource needed for the wall
                                    map_all[grid_position_x][grid_position_y]=temp[0:2]+"W"+wall_direction[Player_direction[player]]+"--"+temp[6:]##Record wall placement
                            else:
                                map_all[grid_position_x][grid_position_y]=temp[0:2]+"----"+temp[6:]##Record wall placement
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
