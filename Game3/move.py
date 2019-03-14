##THIS FUNCTION DEFINES HOW THE PLAYERS WILL MOVE##
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *
def MOVE(cs,map_all):

    ##Temporarly store player positions before move##
    position1=POINT(cs.Player1.position.x,cs.Player1.position.y)
    position2=POINT(cs.Player2.position.x,cs.Player2.position.y)

    ##PLAYER1 KEYS##
    direction=""
    if  cs.variables.S_key_last==wf.S_KEY_DOWN:
        position1.y=position1.y+10
        direction="down"
        cs.variables.player1_direction="down"
    if cs.variables.A_key_last==wf.A_KEY_DOWN:
        position1.x=position1.x-10
        direction="left"
        cs.variables.player1_direction="left"
    if cs.variables.D_key_last==wf.D_KEY_DOWN:
        position1.x=position1.x+10
        direction="right"
        cs.variables.player1_direction="right"
    if cs.variables.W_key_last==wf.W_KEY_DOWN:
        position1.y=position1.y-10
        direction="up"
        cs.variables.player1_direction="up"

    ##If player is moving update the direction and the animation step##
    if direction!="":
        cs.Player1.Update_direction(direction)
        cs.Player1.Animate_step(True)
    ##PLAYER2 KEYS##
    if cs.variables.NUM5_key_last==wf.NUM5_KEY_DOWN:
        position2.y=position2.y+10
        cs.Player2.direction="down"
        cs.variables.player2_direction="down"
    if cs.variables.NUM4_key_last==wf.NUM4_KEY_DOWN:
        position2.x=position2.x-10
        cs.Player2.direction="left"
        cs.variables.player2_direction="left"
    if cs.variables.NUM6_key_last==wf.NUM6_KEY_DOWN:
        position2.x=position2.x+10
        cs.Player2.direction="right"
        cs.variables.player2_direction="right"
    if cs.variables.NUM8_key_last==wf.NUM8_KEY_DOWN:
        position2.y=position2.y-10
        cs.Player2.direction="up"
        cs.variables.player2_direction="up"
    ##IF BUILDING##
    if cs.variables.Tool_Sel.Player2_selection==wf.Empty_Hand:
        position2=POINT(cs.Player2.position.x,cs.Player2.position.y)

    if cs.variables.Tool_Sel.Player1_selection==wf.Empty_Hand:
        position1=POINT(cs.Player1.position.x,cs.Player1.position.y)

    #################
    ##CHECK PLAYERS##
    #################
    gridposition=RECT()                                ##Use to determine what tiles are being viewed on the map##
    positions=[position1,position2]
    player_directions={0:cs.variables.player1_direction,1:cs.variables.player2_direction}
    Players={0:cs.Player1,1:cs.Player2}
    ##Check for object collisions in x or y directions##
    check_x=[True,True]
    check_y=[True,True]
    ##Create dictionary for what tools players are currently using
    Player_selection={0:cs.variables.Tool_Sel.Player1_selection,1:cs.variables.Tool_Sel.Player2_selection}
    ##Use to limit to one button per player##
    Button=[False,False]
    

    ##REPEAT PROCESS FOR BOTH PLAYERS
    for player in range(2):
        ##Convert player rectangle into grid position
        y_shift=-300
        [UL,UR,LL,LR]=Players[player].Target_Box()
        [ULt,URt,LLt,LRt]=Players[player].Target_Box_Shifted(positions[player].x,positions[player].y)
        gridposition.left=int(ULt.x/wf.tile_w)
        gridposition.top=int(ULt.y/wf.tile_h)
        gridposition.right=int(LRt.x/wf.tile_w)
        gridposition.bottom=int(LRt.y/wf.tile_h)
        ##LOOK AT TILES COVERED BY PLAYER CHARACTER AND ALL ADJACENT TILES##
        check_temp=True
        for i in range(gridposition.left-1,gridposition.right+2):
            if i>=0:
                for j in range(gridposition.top-2,gridposition.bottom+2):
                    if j>=0:
                        ##IF THE PLAYER IS IN THE TILE CHECK FOR COLLISION##
                        if (i>=gridposition.left and i<=gridposition.right) and (j>=gridposition.top-2 and j<=gridposition.bottom):
                            ##map strings are GGOOBP check for objects
                            if map_all[i][j][2]!="-": ##First
                                rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=POINT(),POINT(),POINT(),POINT()
                                if map_all[i][j][2]=="T":
                                    ##Mark shifted tree rectangle
                                    rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=cs.Tree1.Target_box(i*wf.tile_w,j*wf.tile_h)
                                elif map_all[i][j][2]=="W":
                                    ##Mark shifted wall rectangle
                                    rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt=cs.Wall1.Target_box(i*wf.tile_w,j*wf.tile_h,int(map_all[i][j][3]))
                                else:
                                    continue
                                ##CHECK X and Y direction for collision##
                                ##Check for intersection of the top and bottom of collision box and the left side of player##        
                                if wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,ULt,LLt):
                                    if wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                              POINT(UL.x,ULt.y),POINT(LL.x,LLt.y)):
                                        check_y[player]=False
                                        check_temp=False
                                    elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                                POINT(ULt.x,UL.y),POINT(LLt.x,LL.y)):
                                        check_x[player]=False
                                        check_temp=False
                                ##Check for intersection of the top and bottom of collision box and the right side of player
                                elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,URt,LRt):
                                    if wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                              POINT(UR.x,URt.y),POINT(LR.x,LRt.y)):
                                        check_y[player]=False
                                        check_temp=False
                                    elif wf.check_intersection2(rcCollisionULt,rcCollisionURt,rcCollisionLLt,rcCollisionLRt,
                                                                POINT(URt.x,UR.y),POINT(LRt.x,LR.y)):
                                        check_x[player]=False
                                        check_temp=False

                                ##Check for intersection of the left and right side of the collision box and the top side of player
                                if check_temp==True:
                                    if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,ULt,URt):
                                        if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                                  POINT(ULt.x,UL.y),POINT(URt.x,UR.y)):
                                            check_x[player]=False
                                        elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                                    POINT(UL.x,ULt.y),POINT(UR.x,URt.y)):
                                            check_y[player]=False
                                    ##Check for intersection of the left and right side of the collision box and the bottom side of player
                                    elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,LLt,LRt):
                                        if wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                                  POINT(LLt.x,LL.y),POINT(LRt.x,LR.y)):
                                            check_x[player]=False
                                        elif wf.check_intersection2(rcCollisionULt,rcCollisionLLt,rcCollisionURt,rcCollisionLRt,
                                                                    POINT(LL.x,LLt.y),POINT(LR.x,LRt.y)):
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
                                        if j==gridposition.top-2 and i==gridposition.left:
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
        if position1.x>=0+wf.shiftx and (position1.x+wf.character_width)<=(wf.map_w-wf.shiftx):
            cs.Player1.Update_Position(position1.x,cs.Player1.position.y)
            cs.variables.Player1_window.windowUL.x=position1.x
    if check_y[0]==True:
        if position1.y>=0+wf.shifty and (position1.y+wf.character_height)<=wf.map_h-wf.shifty:
            cs.Player1.Update_Position(cs.Player1.position.x,position1.y)
            cs.variables.Player1_window.windowUL.y=position1.y

     ##PLAYER2##
    if check_x[1]==True:
        if position2.x>=0+wf.shiftx and (position2.x+wf.character_width)<=(wf.map_w-wf.shiftx):
            cs.Player2.Update_Position(position2.x,cs.Player2.position.y)
            cs.variables.Player2_window.windowUL.x=position2.x
    if check_y[1]==True:
        if position2.y>=0+wf.shifty and (position2.y+wf.character_height)<=wf.map_h-wf.shifty:
            cs.Player2.Update_Position(cs.Player2.position.x,position2.y)
            cs.variables.Player2_window.windowUL.y=position2.y
    return 0

##test=ws.Variables_and_dictionaries()
##chart=wf.ARRAY_CREATE(int(wf.map_w/200),int(wf.map_h/200))
##for i in range(int(wf.map_w/200)):
##        for j in range(int(wf.map_h/200)):
##            chart[i][j]="G1----"
##MOVE(test,chart)
