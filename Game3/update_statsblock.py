##THIS FUNCTION KEEPS UPDATES THE STATISTICS BLOCK IN THE GAME##
import window_structures as ws
import window_functions as wf
from ctypes import *
from ctypes.wintypes import *

def UPDATE_STATSBLOCK(cs):
    ###################
    ##UPATE RESOURCES##
    ###################
    ##If the tree token has already been added simply update the number
    if cs.variables.tree_token==True:
        ##Draw Rectangle to white out previous numbers
##        windll.user32.FillRect(self.vwin.hdc,pointer(self.vwin.rcMessage_box),self.vwin.hbrBkgnd)
        windll.gdi32.Rectangle(cs.dict_background_hdc["stats_block"],cs.variables.rcStats[0].left-1,cs.variables.rcStats[0].top-1,
                               cs.variables.rcStats[0].right,
                               cs.variables.rcStats[0].bottom)
        ##Type in the new number
        windll.user32.DrawTextW(cs.dict_background_hdc["stats_block"],c_wchar_p(str(cs.variables.Num_trees_cut)),-1,pointer(cs.variables.rcStats[0]),0)

    ##If the tree token has not been added but the number of trees is now greater than 0 add the token
    elif cs.variables.Num_trees_cut==1 and cs.variables.tree_token==False:
        ##Update the tree token to being placed
        cs.variables.tree_token=True
        
        ##LEFT TOKEN
        windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],cs.variables.Region_token[0])                      ##Create clipping region to outline the token
        windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],POINT(),wf.token_w,wf.token_h,                            ##Add token image to stats block
                            cs.dict_token_hdc["tree_token"],0,0,wf.SRCCOPY)
        windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],None)                                              ##Clear the clipping region

        ##RIGHT TOKEN
        position=POINT(wf.stats_block_w-wf.token_w,0)                                                                       ##Create Point for defining placement of second tree token
        windll.gdi32.OffsetRgn(cs.variables.Region_token[0],position)                                                       ##Shift the clipping region
        windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],cs.variables.Region_token[0])                      ##Select the shifted clipping region
        windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],position,wf.token_w,wf.token_h,                           ##Add token image to stats block
                            cs.dict_token_hdc["tree_token"],0,0,wf.SRCCOPY)
        windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],None)                                              ##Clear the clipping region
        windll.gdi32.OffsetRgn(cs.variables.Region_token[0],-position.x,-position.y)                                        ##Shift the clipping region back to zero

        ##DISPLAY NUMBER
        ##Draw Rectangle for numbers to be placed on top of
        windll.gdi32.Rectangle(cs.dict_background_hdc["stats_block"],cs.variables.rcStats[0].left-1,cs.variables.rcStats[0].top-1,
                               cs.variables.rcStats[0].right,
                               cs.variables.rcStats[0].bottom)
        ##Type in the first number
        windll.user32.DrawTextW(cs.dict_background_hdc["stats_block"],c_wchar_p(str(cs.variables.Num_trees_cut)),-1,pointer(cs.variables.rcStats[0]),0)
    #######################
    ##UPDATE STAMINA BARS##
    #######################
    ##Clear Stamina Bars
    windll.user32.FillRect(cs.dict_background_hdc["stats_block"],pointer(cs.variables.rcStats[1]),cs.variables.Fill_color2)
    windll.user32.FillRect(cs.dict_background_hdc["stats_block"],pointer(cs.variables.rcStats[2]),cs.variables.Fill_color2)
    ##DRAW RECTANGLES FOR STAMINA BARS##
    temp1=RECT()
    windll.user32.SetRect(pointer(temp1),cs.variables.rcStats[1].left,cs.variables.rcStats[1].bottom-cs.Player1.Stamina,cs.variables.rcStats[1].right,cs.variables.rcStats[1].bottom)
    windll.user32.FillRect(cs.dict_background_hdc["stats_block"],pointer(temp1),cs.variables.Fill_color)
    windll.user32.SetRect(pointer(temp1),cs.variables.rcStats[2].left,cs.variables.rcStats[2].bottom-cs.Player2.Stamina,cs.variables.rcStats[2].right,cs.variables.rcStats[2].bottom)
    windll.user32.FillRect(cs.dict_background_hdc["stats_block"],pointer(temp1),cs.variables.Fill_color)
    ##Overlap the meter boarder##
    ##For Player1
    position=POINT(cs.variables.rcStats[1].left-2,cs.variables.rcStats[1].top-10)                         ##Top left corner of meter
    windll.gdi32.OffsetRgn(cs.variables.Region_token[3],position)                                         ##Shift the region to draw meter
    windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],cs.variables.Region_token[3])        ##Clip the region to draw the meter
    windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],position,                                   ##Draw the meter
                        cs.variables.rcStats[1].right-cs.variables.rcStats[1].left+5,
                        cs.variables.rcStats[1].bottom-cs.variables.rcStats[1].top+20,
                        cs.dict_token_hdc["stamina_meter"],
                        0,0,wf.SRCCOPY)
    windll.gdi32.OffsetRgn(cs.variables.Region_token[3],-position.x,-position.y)                                   ##Shift the region back
    windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],None)                                #Remove the region
    ##For Player2
    position=POINT(cs.variables.rcStats[2].left-2,cs.variables.rcStats[2].top-10)                         ##Top left corner of meter
    windll.gdi32.OffsetRgn(cs.variables.Region_token[3],position)                                         ##Shift the region to draw meter
    windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],cs.variables.Region_token[3])        ##Clip the region to draw the meter
    windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],position,                                   ##Draw the meter
                        cs.variables.rcStats[2].right-cs.variables.rcStats[2].left+5,
                        cs.variables.rcStats[2].bottom-cs.variables.rcStats[2].top+20,
                        cs.dict_token_hdc["stamina_meter"],
                        0,0,wf.SRCCOPY)
    windll.gdi32.OffsetRgn(cs.variables.Region_token[3],-position.x,-position.y)                                   ##Shift the region back
    windll.gdi32.SelectClipRgn(cs.dict_background_hdc["stats_block"],None)                                #Remove the region
    
    #########################
    ##UPDATE SELECTED TOOLS##
    #########################
    ##If the tokens have not been displayed yet or the selection has been changed
    if cs.variables.axe_displayed==False or cs.variables.Tool_Sel.Player1_prev_selection!=cs.variables.Tool_Sel.Player1_selection or cs.variables.Tool_Sel.Player2_prev_selection!=cs.variables.Tool_Sel.Player2_selection:
        token_shift=3
        rcSelect_player={0:cs.variables.Tool_Sel.rcSelect_player1[cs.variables.Tool_Sel.Player1_selection],                 ##Define what the selection rectangles are going to be selecting
                         1:cs.variables.Tool_Sel.rcSelect_player2[cs.variables.Tool_Sel.Player2_selection]}
        prev_rcSelect_player={0:cs.variables.Tool_Sel.rcSelect_player1[cs.variables.Tool_Sel.Player1_prev_selection],       ##Define what the previous rectangles would be selecting
                              1:cs.variables.Tool_Sel.rcSelect_player2[cs.variables.Tool_Sel.Player2_prev_selection]}
        prev_Select_player={0:cs.variables.Tool_Sel.Player1_prev_selection,                                                 ##Define what the previous selection where
                            1:cs.variables.Tool_Sel.Player2_prev_selection}
        current_Select_player={0:cs.variables.Tool_Sel.Player1_selection,1:cs.variables.Tool_Sel.Player2_selection}         ##Define what the current selections are
        ##If boxes have already been added
        if cs.variables.axe_displayed==True:
            for player in range(2):
                ##If the selection has changed
                if prev_Select_player[player]!=current_Select_player[player]:
                    windll.gdi32.SetROP2(cs.dict_background_hdc["stats_block"], wf.R2_XORPEN)                               ##CHANGES THE RED ON RECT TO BLACK
                    windll.gdi32.Rectangle(cs.dict_background_hdc["stats_block"],prev_rcSelect_player[player].left-1,       #Draws a new black rectangle to show it is deselected
                                           prev_rcSelect_player[player].top-1,prev_rcSelect_player[player].right+1,
                                           prev_rcSelect_player[player].bottom+1)

                    windll.gdi32.SetROP2(cs.dict_background_hdc["stats_block"], wf.R2_COPYPEN)                              ##USES THE PEN COLOR WHICH SHOULD BE RED
                    windll.gdi32.Rectangle(cs.dict_background_hdc["stats_block"],rcSelect_player[player].left-1,            #Draws a new red rectangle to show the selected tool
                                           rcSelect_player[player].top-1,rcSelect_player[player].right+1,
                                           rcSelect_player[player].bottom+1)
                    ##ADD THE TOOL ICONS##
                    space_between=(wf.stats_block_w-wf.token_w-20)*player                                                   ##Add the amount of shift needed depending on the player
                    windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],space_between+10,                             ##Copy the token on top of the black selection rectangle
                                        (10+prev_Select_player[player])*wf.token_h+prev_Select_player[player]*4,
                                        wf.token_w,wf.token_h,
                                        cs.dict_token_hdc[cs.dict_token_index[prev_Select_player[player]+token_shift]],
                                        0,0,wf.SRCCOPY)
                    windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],space_between+10,                             ##Copy the token on top of the red selection rectangle
                                        (10+current_Select_player[player])*wf.token_h+current_Select_player[player]*4,
                                        wf.token_w,wf.token_h,
                                         cs.dict_token_hdc[cs.dict_token_index[current_Select_player[player]+token_shift]],
                                        0,0,wf.SRCCOPY)
                    ##Update the selection tracking
                    if player==0:
                        cs.variables.Tool_Sel.Player1_prev_selection=cs.variables.Tool_Sel.Player1_selection
                    else:
                        cs.variables.Tool_Sel.Player2_prev_selection=cs.variables.Tool_Sel.Player2_selection
        ##If the tokens have not been displayed before draw the appropriate boxes                    
        else:
            ##ADD SELECTION BOX##
            windll.gdi32.SelectObject(cs.dict_background_hdc["stats_block"],cs.variables.hpenDot_black)                             ##Select the black pen
            ##Draw black rectangles for every tool
            for i in range(2):
                rcSelect_player={0:cs.variables.Tool_Sel.rcSelect_player1[i],1:cs.variables.Tool_Sel.rcSelect_player2[i]}
                for player in range(2):
                    windll.gdi32.SetROP2(cs.dict_background_hdc["stats_block"], wf.R2_COPYPEN)
                    windll.gdi32.Rectangle(cs.dict_background_hdc["stats_block"],rcSelect_player[player].left-1,                    ##Draw Black rectangle
                                           rcSelect_player[player].top-1,rcSelect_player[player].right+1,
                                           rcSelect_player[player].bottom+1)
            ##SELECT FIRST SELECTION
            windll.gdi32.SelectObject(cs.dict_background_hdc["stats_block"],cs.variables.hpenDot)                                           ##CHANGE THE PEN OUTLINE BACK TO RED
            ##Draw red rectangles for the first selections
            for player in range(2):
                rcSelect_player={0:cs.variables.Tool_Sel.rcSelect_player1[cs.variables.Tool_Sel.Player1_selection],                 ##Define Rectangles for current selections
                                 1:cs.variables.Tool_Sel.rcSelect_player2[cs.variables.Tool_Sel.Player2_selection]}
                windll.gdi32.SetROP2(cs.dict_background_hdc["stats_block"], wf.R2_COPYPEN)
                windll.gdi32.Rectangle(cs.dict_background_hdc["stats_block"],rcSelect_player[player].left-1,                        ##Draw Red rectangle
                                       rcSelect_player[player].top-1, rcSelect_player[player].right+1,
                                       rcSelect_player[player].bottom+1)
            
            
            ##ADD THE TOOLS
            space_between=wf.stats_block_w-wf.token_w-20                                                            ##Define shift between player1 and player2 tokens
            for i in range(2):
                ##LEFT TOKEN
                windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],10,(10+i)*wf.token_h+i*4,                     ##Copy tool token onto rectangle for player 1
                                    wf.token_w,wf.token_h,
                                    cs.dict_token_hdc[cs.dict_token_index[i+token_shift]]
                                    ,0,0,wf.SRCCOPY)
                ##RIGHT TOKEN##
                windll.gdi32.BitBlt(cs.dict_background_hdc["stats_block"],space_between+10,(10+i)*wf.token_h+i*4,       ##Copy tool token onto rectangle for player 2
                                    wf.token_w,wf.token_h,
                                    cs.dict_token_hdc[cs.dict_token_index[i+token_shift]]
                                    ,0,0,wf.SRCCOPY)
            cs.variables.axe_displayed=True                                                                                                 ##Update the tracker to know initial selection has been drawn
    return

##test=ws.Variables_and_dictionaries()
####test.dict_character_files
##UPDATE_STATSBLOCK(test)
