##THIS CLASS IS FOR THE BUTTON SPRITE##
import window_functions as wf
import window_structures as ws
from ctypes import *
from ctypes.wintypes import *

class Button:
    def __init__(self,hdc_main,file_path,color):
        ##Initialize hdc, dictionary and load images##
        red_button_file="Red_button.bmp"
        purple_button_file="Purple_button.bmp"
        name_dict={"red":red_button_file,"purple":purple_button_file}            #Define dictionary
        self.hbmp=wf.LoadImage(c_void_p(),LPCWSTR(file_path+name_dict[color]),    #Load image
                                   wf.IMAGE_BITMAP,0,0,
                                   8192|wf.LR_DEFAULTSIZE|wf.LR_LOADFROMFILE)

        ##LOAD HDC##
        self.hdc=windll.gdi32.CreateCompatibleDC(hdc_main)                  #Make hdc_red similar to the reference hdc

        ##COPY IMAGES INTO HDC##
        windll.gdi32.SelectObject(self.hdc,self.hbmp)                   #Copy image into hdc_red

        ##GET COLOR##
        self.Bkgnd_color=windll.gdi32.GetPixel(self.hdc,10,10)

        ##LOAD REGION##
        self.Region=windll.gdi32.CreateEllipticRgn(0,0,31,31)
        self.rcText=RECT()
        windll.user32.SetRect(pointer(self.rcText),int(wf.button_w/3),int(wf.button_h/4),int(wf.button_w/3)+wf.button_w, int(wf.button_h/4)+wf.button_h)

    def Draw_Button(self,hdc,x_shift,y_shift,button_text):
        ##Draw the button in the right tile and position
        position=POINT(x_shift,y_shift)
        windll.gdi32.OffsetRgn(self.Region,position)                                                    ##Shift the region to draw the button
        windll.gdi32.SelectClipRgn(hdc,self.Region)                                                     ##Select the shifted region for copying the button
        windll.gdi32.BitBlt(hdc,position,wf.button_w,wf.button_h,self.hdc,0,0,wf.SRCCOPY)               ##Add button to background

        ##Draw Text##
        wf.ShiftRect(self.rcText,position.x,position.y)                                                 ##Shift the textbox to the desired spot on the button
        windll.gdi32.SetBkColor(hdc,self.Bkgnd_color)                                                   ##Ensure the Background color matches the button
        windll.user32.DrawTextW(hdc,c_wchar_p(button_text),-1,pointer(self.rcText),0)                   ##Write the button key
        wf.ShiftRect(self.rcText,-position.x,-position.y)                                               ##Shift the textbox back to the original position
                            
        ##Reset class object and hdc
        windll.gdi32.SelectClipRgn(hdc,None)                                                            ##Remove Clipping Region
        windll.gdi32.OffsetRgn(self.Region,-position.x,-position.y)                                     ##Return the region back
        return 0
