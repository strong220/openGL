##THIS FUNCTION DEFINES HOW THE PLAYERS WILL MOVE##
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *
def MOVE(cs,map_all):

    ##Temporarly store player positions before move##
    windowULt=POINT(cs.variables.Player1_window.windowUL.x,cs.variables.Player1_window.windowUL.y)
    windowLRt=POINT(cs.variables.Player1_window.windowLR.x,cs.variables.Player1_window.windowLR.y)
    windowULt_2=POINT(cs.variables.Player2_window.windowUL.x,cs.variables.Player2_window.windowUL.y)
    windowLRt_2=POINT(cs.variables.Player2_window.windowLR.x,cs.variables.Player2_window.windowLR.y)
    
    ##PLAYER1 KEYS##
    if  cs.variables.S_key_last==wf.S_KEY_DOWN:
        windowULt.y=windowULt.y+10
        windowLRt.y=windowLRt.y+10
        cs.variables.player1_direction="down"
    if cs.variables.A_key_last==wf.A_KEY_DOWN:
        windowULt.x=windowULt.x-10
        windowLRt.x=windowLRt.x-10
        cs.variables.player1_direction="left"
    if cs.variables.D_key_last==wf.D_KEY_DOWN:
        windowULt.x=windowULt.x+10
        windowLRt.x=windowLRt.x+10
        cs.variables.player1_direction="right"
    if cs.variables.W_key_last==wf.W_KEY_DOWN:
        windowULt.y=windowULt.y-10
        windowLRt.y=windowLRt.y-10
        cs.variables.player1_direction="up"

    ##PLAYER2 KEYS##
    if cs.variables.NUM5_key_last==wf.NUM5_KEY_DOWN:
       windowULt_2.y=windowULt_2.y+10
       windowLRt_2.y=windowLRt_2.y+10
       cs.variables.player2_direction="down"
    if cs.variables.NUM4_key_last==wf.NUM4_KEY_DOWN:
        windowULt_2.x=windowULt_2.x-10
        windowLRt_2.x=windowLRt_2.x-10
        cs.variables.player2_direction="left"
    if cs.variables.NUM6_key_last==wf.NUM6_KEY_DOWN:
        windowULt_2.x=windowULt_2.x+10
        windowLRt_2.x=windowLRt_2.x+10
        cs.variables.player2_direction="right"
    if cs.variables.NUM8_key_last==wf.NUM8_KEY_DOWN:
        windowULt_2.y=windowULt_2.y-10
        windowLRt_2.y=windowLRt_2.y-10
        cs.variables.player2_direction="up"

    #################
    ##CHECK PLAYERS##
    #################
    gridposition=RECT()                                ##Use to determine what tiles are being viewed on the map##
    windowLRts={0:windowLRt,1:windowLRt_2}
    windowULts={0:windowULt,1:windowULt_2}
    windowLRs={0:cs.variables.Player1_window.windowLR,1:cs.variables.Player2_window.windowLR}
    windowULs={0:cs.variables.Player1_window.windowUL,1:cs.variables.Player2_window.windowUL}
    player_directions={0:cs.variables.player1_direction,1:cs.variables.player2_direction}
    ##Check for object collisions in x or y directions##
    check_x=[True,True]
    check_y=[True,True]
    ##Create dictionary for what tools players are currently using
    Player_selection={0:cs.variables.Tool_Sel.Player1_selection,1:cs.variables.Tool_Sel.Player2_selection}
    ##Use to limit to one button per player##
    Button=[False,False]
    
    ##DEFINE RECTANGLES FOR COLLISIONS WITH OBJECTS##
    rcTreeUL,rcTreeUR,rcTreeLL,rcTreeLR=POINT(),POINT(),POINT(),POINT()
    rcWallUL,rcWallUR,rcWallLL,rcWallLR=POINT(),POINT(),POINT(),POINT()

    ##REPEAT PROCESS FOR BOTH PLAYERS
    for player in range(2):
        ##Convert player rectangle into grid position
        gridposition.left=int(windowULts[player].x/wf.tile_w)
        gridposition.top=int(windowULts[player].y/wf.tile_h)
        gridposition.right=int(windowLRts[player].x/wf.tile_w)
        gridposition.bottom=int(windowLRts[player].y/wf.tile_h)
        
        ##LOOK AT TILES COVERED BY PLAYER CHARACTER AND ALL ADJACENT TILES##
        for i in range(gridposition.left-1,gridposition.right+2):
            if i>=0:
                for j in range(gridposition.top-1,gridposition.bottom+2):
                    if j>=0:
                        ##IF THE PLAYER IS IN THE TILE CHECK FOR COLLISION##
                        if (i>=gridposition.left and i<=gridposition.right) and (j>=gridposition.top and j<=gridposition.bottom):
                            ##map strings are GGOOBP check for objects
                            if map_all[i][j][2]!="-": ##First
                                rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=POINT(),POINT(),POINT(),POINT()
                                if map_all[i][j][2]=="T":
                                    ##Mark shifted tree rectangle
                                    rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=cs.Tree1.Target_box(i*wf.tile_w,j*wf.tile_h)
                                elif map_all[i][j][2]=="W":
                                    rcWallUL=cs.variables.Wall_target_boxes[int(map_all[i][j][3])].WallUL
                                    rcWallUR=cs.variables.Wall_target_boxes[int(map_all[i][j][3])].WallUR
                                    rcWallLL=cs.variables.Wall_target_boxes[int(map_all[i][j][3])].WallLL
                                    rcWallLR=cs.variables.Wall_target_boxes[int(map_all[i][j][3])].WallLR
                                    ##Define shifted wall rectangle
                                    rcCollisionULt.x,rcCollisionURt.x,rcCollisionLLt.x,rcCollisionLRt.x,=[rcWallUL.x+i*wf.tile_w,rcWallUR.x+i*wf.tile_w,rcWallLL.x+i*wf.tile_w,rcWallLR.x+i*wf.tile_w]
                                    rcCollisionULt.y,rcCollisionURt.y,rcCollisionLLt.y,rcCollisionLRt.y,=[rcWallUL.y+j*wf.tile_h,rcWallUR.y+j*wf.tile_h,rcWallLL.y+j*wf.tile_h,rcWallLR.y+j*wf.tile_h]
                                else:
                                    continue
                                ##CHECK X and Y direction for collision##
                                if rcCollisionULt.x>windowULts[player].x and rcCollisionULt.x<windowLRts[player].x:
                                    if (rcCollisionULt.y>windowULs[player].y and rcCollisionULt.y<windowLRs[player].y) or (rcCollisionLLt.y>windowULs[player].y and rcCollisionLLt.y<windowLRs[player].y) or (rcCollisionULt.y<windowULs[player].y and rcCollisionLLt.y>windowLRs[player].y):
                                        check_x[player]=False
                                        windowULts[player].x=windowULs[player].x
                                        windowLRts[player].x=windowLRs[player].x
                                elif rcCollisionURt.x>windowULts[player].x and rcCollisionURt.x<windowLRts[player].x:
                                    if (rcCollisionULt.y>windowULs[player].y and rcCollisionULt.y<windowLRs[player].y) or (rcCollisionLLt.y>windowULs[player].y and rcCollisionLLt.y<windowLRs[player].y) or (rcCollisionULt.y<windowULs[player].y and rcCollisionLLt.y>windowLRs[player].y):
                                        check_x[player]=False
                                        windowULts[player].x=windowULs[player].x
                                        windowLRts[player].x=windowLRs[player].x
                                if rcCollisionULt.y>windowULts[player].y and rcCollisionULt.y<windowLRts[player].y:
                                    if (rcCollisionULt.x>windowULs[player].x and rcCollisionULt.x<windowLRs[player].x) or (rcCollisionURt.x>windowULs[player].x and rcCollisionURt.x<windowLRs[player].x) or (rcCollisionULt.x<windowULs[player].x and rcCollisionURt.x>windowLRs[player].x) :
                                        check_y[player]=False
                                elif rcCollisionLLt.y>windowULts[player].y and rcCollisionLLt.y<windowLRts[player].y:
                                    if (rcCollisionULt.x>windowULs[player].x and rcCollisionULt.x<windowLRs[player].x) or (rcCollisionURt.x>windowULs[player].x and rcCollisionURt.x<windowLRs[player].x) or (rcCollisionULt.x<windowULs[player].x and rcCollisionURt.x>windowLRs[player].x) :
                                        check_y[player]=False

                                ##REMOVE ALL BUTTONS THAT BELONG TO THE PLAYER##
                                if map_all[i][j][4:]=="B"+str(player):
                                    map_all[i][j]=map_all[i][j][0:4]+"--"
                                    ##If the player has a collision with the axe then allow for a button but check that no other buttons for that player have been made
                                if (check_y[player]==False or check_x[player]==False) and Button[player]==False:
                                ##If no button in direction faced add it, all other directions remove
                                    if player_directions[player]=="down":
                                        ##Check to see if this is bottom tile##
                                        if j==gridposition.bottom:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j][4]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True
                                    elif player_directions[player]=="up":
                                        ##Check to see if this is bottom tile##
                                        if j==gridposition.top:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j][4]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True
                                    elif player_directions[player]=="left":
                                        ##Check to see if this is bottom tile##
                                        if i==gridposition.left:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True
                                    elif player_directions[player]=="right":
                                        ##Check to see if this is bottom tile##
                                        if i==gridposition.right:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True
                        ##IF THE PLAYER HAD THE EMPTY HAND FOR BUILDING##
                        if Player_selection[player]==wf.Empty_Hand:
                            ##IF THE TILE HAS NO OBJECT IN IT##
                            if map_all[i][j][2]=="-":
                                ##Remove previous buttons##
                                if map_all[i][j][4]=="B":
                                    map_all[i][j]=map_all[i][j][0:4]+"--"
                                #If the button has not been placed
                                if Button[player]==False:
                                    if player_directions[player]=="down":
                                        ##Check to see if this is bottom tile##
                                        if j==gridposition.bottom+1 and i==gridposition.left:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j][4]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True
                                    elif player_directions[player]=="up":
                                        ##Check to see if this is bottom tile##
                                        if j==gridposition.top-1 and i==gridposition.left:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j][4]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True
                                    elif player_directions[player]=="left":
                                        ##Check to see if this is bottom tile##
                                        if i==gridposition.left-1 and j==gridposition.bottom-1:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j][4]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True
                                    elif player_directions[player]=="right":
                                        ##Check to see if this is bottom tile##
                                        if i==gridposition.right+1 and j==gridposition.bottom-1:
                                            ##If this is bottom tile check to see if there is a button, if there is do nothing
                                            if map_all[i][j][4]!="B":
                                                ##If no button add it and remove button from all other tiles
                                                map_all[i][j]=map_all[i][j][0:4]+"B"+str(player)
                                                Button[player]=True

    cs.variables.Player1_button=Button[0]
    cs.variables.Player2_button=Button[1]

    ##########################
    ##UPDATE PLAYER POSITION##
    ##########################

    ##PLAYER1##
    if check_x[0]==True:
        if windowULt.x>=0+wf.shiftx and windowLRt.x<=(wf.map_w-wf.shiftx):
            cs.variables.Player1_window.windowUL.x=windowULt.x
            cs.variables.Player1_window.windowLR.x=windowLRt.x
    if check_y[0]==True:
        if windowULt.y>=0+wf.shifty and windowLRt.y<=wf.map_h-wf.shifty:
            cs.variables.Player1_window.windowUL.y=windowULt.y
            cs.variables.Player1_window.windowLR.y=windowLRt.y
     ##PLAYER2##
    if check_x[1]==True:
        if windowULt_2.x>=0+wf.shiftx and windowLRt_2.x<=(wf.map_w-wf.shiftx):
            cs.variables.Player2_window.windowUL.x=windowULt_2.x
            cs.variables.Player2_window.windowLR.x=windowLRt_2.x
    if check_y[1]==True:
        if windowULt_2.y>=0+wf.shifty and windowLRt_2.y<=wf.map_h-wf.shifty:
            cs.variables.Player2_window.windowUL.y=windowULt_2.y
            cs.variables.Player2_window.windowLR.y=windowLRt_2.y
    return 0

##test=ws.Variables_and_dictionaries()
##chart=wf.ARRAY_CREATE(int(wf.map_w/200),int(wf.map_h/200))
##for i in range(int(wf.map_w/200)):
##        for j in range(int(wf.map_h/200)):
##            chart[i][j]="G1----"
##MOVE(test,chart)
