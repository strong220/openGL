##THIS FUNCTION DISPLAYS AN INITIAL IMAGE
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *

def WM_PAINT(cs,hwnd):              ##Take in the class variables and the handle to the main window
    ##Create the Paint variable
    ps=ws.PAINTSTRUCT()
    ##BEGIN PAINT##
    windll.user32.BeginPaint(hwnd,pointer(ps))

    ##Copy desired image to hdc for display##
    position=POINT(wf.shiftx,wf.shifty)                                                   ##Point that describes where to place the character
    windll.gdi32.OffsetRgn(cs.variables.Player1_animation_Rgn.down[0],position)             ##Offset Region for drawing character
    windll.gdi32.BitBlt(cs.dict_background_hdc["mem_main1"],0,0,wf.map_w,wf.map_h,          ##Copy background over to player1 window
                        cs.dict_background_hdc["mem_backgrnd1"],0,0,wf.SRCCOPY)
    windll.gdi32.SelectClipRgn(cs.dict_background_hdc["mem_main1"],                         ##Select Region for character
                               cs.variables.Player1_animation_Rgn.down[0])
    windll.gdi32.BitBlt(cs.dict_background_hdc["mem_main1"],position,wf.character_width,    ##Copy character image into player1 window
                        wf.character_height,cs.dict_character_hdc["character1_down"],0,0
                        ,wf.SRCCOPY)
    windll.gdi32.BitBlt(ps.hdc,0,0,wf.main_window_w,wf.main_window_h,                       ##Display player1 window
                        cs.dict_background_hdc["mem_main1"],0,0,wf.SRCCOPY)
    windll.gdi32.BitBlt(ps.hdc,wf.main_window_w-int(wf.stats_block_w/2),0,                  ##DIsplay the Stats block
                        wf.stats_block_w,wf.stats_block_h,
                        cs.dict_background_hdc["stats_block"],0,0,wf.SRCCOPY)
    windll.gdi32.SelectClipRgn(cs.dict_background_hdc["mem_main1"],None)                    ##Remove the clipping region from player1 window
    windll.gdi32.OffsetRgn(cs.variables.Player1_animation_Rgn.down[0],-wf.shiftx,-wf.shifty)##Return the region to its original position
    ##END PAINT##
    windll.user32.ReleaseDC(hwnd,ps.hdc)            ##Release the hdc back to memory
    windll.user32.EndPaint(hwnd,pointer(ps))        ##End the Paint call
    return 0
