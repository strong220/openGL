##THIS FILE CONTAINS ALL THE STRUCTURES FOR UPDATING THE WINDOW
from ctypes import *
from ctypes.wintypes import *
from Tree1_Sprite import Tree_Sprite_1

class PAINTSTRUCT(Structure):
    _fields_=[("hdc",HDC),
              ("fErase",c_bool),
              ("rcPaint", RECT),
              ("fRestore",c_bool),
              ("fIncUpdate",c_bool),
              ("rgbReserved", BYTE*32)]

class Main_variables(Structure):
    _fields_=[("hdc_show",HDC),         #This hdc is the handle for the window display
              ("hdc_mem_show",HDC),     #Compiles the image just before showing
              ("hdc_mem_main",HDC),      #This hdc is the handle for the memory hdc which holds the entire image from which hdc_show views
              ("hdc_mem_main2",HDC),      #This hdc is the handle for the memory hdc which holds the entire image from which hdc_show views
              ("hdc_mem_backgrnd",HDC),      #This hdc is the handle for the memory hdc which holds the entire image from which hdc_show views
              ("hdc_mem_backgrnd2",HDC),      #This hdc is the handle for the memory hdc which holds the entire image from which hdc_show views
              ("hdc_grass",HDC*4),       #Holds the different grass blocks
              ("hdc_grass2",HDC*4),       #Holds the different grass blocks
              ("hdc_tree",HDC*4),       #Holds the different grass blocks
              ("hdc_tree2",HDC*4),       #Holds the different grass blocks
              ("hdc_wall",HDC*2),       #Holds different wall directions
              ("hdc_stats_block",HDC),   #The block contains both the background and the data for player stats
              ("hdc_tree_token",HDC),   #Contains the token for trees in the stats block
              ("hdc_axe_token",HDC),   #Contains the token for trees in the stats block
              ("hdc_empty_hand_token",HDC),   #Contains the token for trees in the stats block
              ("hdc_button",HDC*2),       #For buttons that are displayed
              ("player1_direction",c_wchar_p),  #Remembers what the latest direction player1 is facing as a string
              ("player2_direction",c_wchar_p),  #Remembers what the latest direction player2 is facing as a string
              ("hdc_player1_up",HDC*4),  #Holds the positions of character moving up
              ("hdc_player1b_up",HDC*4),  #Holds the positions of character moving up
              ("hdc_player1_down",HDC*4),  #Holds the positions of character moving down
              ("hdc_player1b_down",HDC*4),  #Holds the positions of character moving down
              ("hdc_player1_left",HDC*4),  #Holds the positions of character moving left
              ("hdc_player1b_left",HDC*4),  #Holds the positions of character moving left
              ("hdc_player1_right",HDC*4),  #Holds the positions of character moving right
              ("hdc_player1b_right",HDC*4),  #Holds the positions of character moving right
              ("hdc_player2_up",HDC*4),  #Holds the positions of character moving up
              ("hdc_player2b_up",HDC*4),  #Holds the positions of character moving up
              ("hdc_player2_down",HDC*4),  #Holds the positions of character moving down
              ("hdc_player2b_down",HDC*4),  #Holds the positions of character moving down
              ("hdc_player2_left",HDC*4),  #Holds the positions of character moving left
              ("hdc_player2b_left",HDC*4),  #Holds the positions of character moving left
              ("hdc_player2_right",HDC*4),  #Holds the positions of character moving right
              ("hdc_player2b_right",HDC*4),  #Holds the positions of character moving right
              ("Region_player1",HRGN),      #Rectangle Region
              ("Region_player1_up",HRGN*4),  #Holds the positions of character moving up
              ("Region_player1_down",HRGN*4),  #Holds the positions of character moving down
              ("Region_player1_right",HRGN*4),  #Holds the positions of character moving down
              ("Region_player1_left",HRGN*4),  #Holds the positions of character moving down
              ("Region_player2_up",HRGN*4),  #Holds the positions of character moving up
              ("Region_player2_down",HRGN*4),  #Holds the positions of character moving down
              ("Region_player2_right",HRGN*4),  #Holds the positions of character moving down
              ("Region_player2_left",HRGN*4),  #Holds the positions of character moving down
              ("Region_tree",HRGN*4),     #Holds the regions of various trees
              ("Region_wall",HRGN*2),     #Holds the regions of various trees
              ("Region_button",HRGN),    #The Region of buttons
              ("Region_token",HRGN*4),    #The Regions for the different tokens
              ("hdc_wheat",HDC*5),       #Holds the different types of Wheat
              ("hdc_wall",HDC*8),        #Contains the different shapes of wall
              ("hdc_house",HDC),         #Contains the different homes
              ("ptClientUL",POINT),      #Client area upper left corner
              ("ptClientLR",POINT),      #Client area lower right corner
              ("windowUL",POINT),        #Upper left corner of rectangle view
              ("windowLR",POINT),        #Lower right corner of rectangle view
              ("windowUL_2",POINT),        #Upper left corner of rectangle view
              ("windowLR_2",POINT),        #Lower right corner of rectangle view
              ("rcClient",RECT),         #Rectangle describing the window
              ("rcText",RECT),          #For describing a rectangle for text
              ("rcStats",RECT*4),          #For describing a rectangle for stats
              ("rcSelect_player1",RECT*4),          #For describing a rectangle for stats
              ("rcSelect_player2",RECT*4),          #For describing a rectangle for stats
              ("Player1_prev_selection",c_int),  #Tracks which tool the player has selected
              ("Player2_prev_selection",c_int),  #Tracks which tool the player has selected
              ("Player1_selection",c_int),  #Tracks which tool the player has selected
              ("Player2_selection",c_int),  #Tracks which tool the player has selected
              ("D_key_last",c_int),
              ("S_key_last",c_int),
              ("A_key_last",c_int),
              ("W_key_last",c_int),
              ("E_key_last",c_int),
              ("Q_key_last",c_int),
              ("Player1_chop",c_bool),
              ("Player1_button",c_bool),
              ("Player2_button",c_bool),
              ("Num_trees_cut",c_int),  #Tracks the number of trees chopped
              ("NUM5_key_last",c_int),
              ("NUM6_key_last",c_int),
              ("NUM8_key_last",c_int),
              ("NUM4_key_last",c_int),
              ("NUM9_key_last",c_int),
              ("NUM7_key_last",c_int),
              ("player1_window",c_bool),
              ("player2_window",c_bool),
              ("player1_window_ULtile",POINT),
              ("player2_window_ULtile",POINT),
              ("tree_token",c_bool)]
class Character_Region(Structure):  #This lists the various fields for animation movement
    _fields_=[("up",HRGN*4),     #Holds the positions of character1 moving up
              ("down",HRGN*4),   #Holds the positions of character1 moving down
              ("right",HRGN*4),  #Holds the positions of character1 moving right
              ("left",HRGN*4)]   #Holds the positions of character1 moving left

class Object_Regions(Structure):            #This lists all the regions needed for objects used in the game other than players
    _fields_=[("Region_tree",HRGN*4),     #Holds the regions of various trees
              ("Region_wall",HRGN*2)]     #Holds the regions of various Wall segments

class Client_window(Structure):            #This holds the coordinates of the window being used
    _fields_=[("ptClientUL",POINT),      #Client area upper left corner
              ("ptClientLR",POINT),      #Client area lower right corner
              ("rcClient",RECT)]         #Rectangle describing the window

class Player_window(Structure):        #This defines the player1 window
    _fields_=[("windowUL",POINT),        #Upper left corner of rectangle view
              ("windowLR",POINT)]        #Lower right corner of rectangle view

class Tool_selection(Structure):        #This class is for tracking the tool selection
    _fields_=[("rcSelect_player1",RECT*4),          #For describing a rectangle for stats
              ("rcSelect_player2",RECT*4),          #For describing a rectangle for stats
              ("Player1_prev_selection",c_int),     #Tracks which tool the player has selected
              ("Player2_prev_selection",c_int),     #Tracks which tool the player has selected
              ("Player1_selection",c_int),          #Tracks which tool the player has selected
              ("Player2_selection",c_int)]          #Tracks which tool the player has selected

class FourPoint(Structure):
    _fields_=[("WallUL",POINT),
             ("WallUR",POINT),
             ("WallLL",POINT),
             ("WallLR",POINT)]
    
class Main_variables2(Structure):
    _fields_=[("hdc_show",HDC),                                     #This hdc is the handle for the window display
              ("player1_direction",c_wchar_p),                      #Remembers what the latest direction player1 is facing as a string
              ("player2_direction",c_wchar_p),                      #Remembers what the latest direction player2 is facing as a string
              ("Region_player1",HRGN),                              #Rectangle Region hit box
              ("Player1_animation_Rgn",Character_Region),           #This holds all regions needed for drawing player1
              ("Player2_animation_Rgn",Character_Region),           #This holds all regions needed for drawing player2
              ("Object_Rgn",Object_Regions),                        #This holds all regions needed for drawing objects
              ("Region_button",HRGN),                               #The region for round buttons
              ("Region_token",HRGN*4),                              #The Regions for the different tokens
              ("Client_window",Client_window),                      #This defines the main window to allow clipping of the cursor
              ("Player1_window",Player_window),                     #This contains the points that define the left window
              ("Player2_window",Player_window),                     #This contains the points that define the right window
              ("rcText",RECT),                                      #For describing a rectangle for text used in buttons
              ("rcStats",RECT*4),                                   #For describing a rectangle for text in the stats block
              ("Tool_Sel",Tool_selection),                          #Contains information for displaying and tracking tools in the stats block
              ("D_key_last",c_int),
              ("S_key_last",c_int),
              ("A_key_last",c_int),
              ("W_key_last",c_int),
              ("E_key_last",c_int),
              ("Q_key_last",c_int),
              ("Player1_chop",c_bool),
              ("Player1_button",c_bool),
              ("Player2_button",c_bool),
              ("Num_trees_cut",c_int),  #Tracks the number of trees chopped
              ("NUM5_key_last",c_int),
              ("NUM6_key_last",c_int),
              ("NUM8_key_last",c_int),
              ("NUM4_key_last",c_int),
              ("NUM9_key_last",c_int),
              ("NUM7_key_last",c_int),
              ("player_window",c_bool*2),
              ("player_window_ULtile",POINT*2),
              ("tree_token",c_bool),
              ("hpenDot",HPEN),
              ("hpenDot_black",HPEN),
              ("axe_displayed",c_bool),
              ("Bkgnd_red_button",c_int),
              ("Bkgnd_purple_button",c_int),
              ("Wall_target_boxes",FourPoint*4)]                    #Contains the target box for each wall

class Variables_and_dictionaries:
    def __init__(self):
        self.variables=Main_variables2()
        self.Tree1=Tree_Sprite_1
        ##Character dictionaries##
        self.dict_character_files={"character1_down":None,"character1_up":None,"character1_right":None,"character1_left":None,
                                   "character2_down":None,"character2_up":None,"character2_right":None,"character2_left":None}
        self.dict_character_hbmp={"character1_down":None,"character1b_down":None,"character1_up":None,"character1b_up":None,"character1_right":None,"character1b_right":None,"character1_left":None,"character1b_left":None,
                    "character2_down":None,"character2b_down":None,"character2_up":None,"character2b_up":None,"character2_right":None,"character2b_right":None,"character2_left":None,"character2b_left":None}
        self.dict_character_index={0:"character1_down",1:"character1_up",2:"character1_right",3:"character1_left",
                                   4:"character2_down",5:"character2_up",6:"character2_right",7:"character2_left",
                                   8:"character1b_down",9:"character1b_up",10:"character1b_right",11:"character1b_left",
                                   12:"character2b_down",13:"character2b_up",14:"character2b_right",15:"character2b_left"}
        self.dict_character_hdc={"character1_down":None,"character1_up":None,"character1_right":None,"character1_left":None,
                                   "character2_down":None,"character2_up":None,"character2_right":None,"character2_left":None}
        ##Grass block dictionaries##
        self.dict_grass_files={"grass_block1":None,"grass_block2":None,"grass_block1_build":None}
        self.dict_grass_hbmp={"grass_block1":None,"grass_block2":None,"grass_block1_build":None}
        self.dict_grass_index={0:"grass_block1",1:"grass_block2",2:"grass_block1_build"}
        self.dict_grass_hdc={"grass_block1":None,"grass_block2":None,"grass_block1_build":None}
        ##Object dictionaries##
        self.dict_object_files={"tree1":None,"wall_vertical":None,"wall_horizontal":None}
        self.dict_object_hbmp={"tree1":None,"wall_vertical":None,"wall_horizontal":None}
        self.dict_object_index={0:"tree1",1:"wall_vertical",2:"wall_horizontal"}
        self.dict_object_hdc={"tree1":None,"wall_vertical":None,"wall_horizontal":None}
        ##Button and token dictionaries##
        self.dict_token_files={"red_button":None,"purple_button":None,"tree_token":None,"axe_token":None,"empty_hand_token":None}
        self.dict_token_hbmp={"red_button":None,"purple_button":None,"tree_token":None,"axe_token":None,"empty_hand_token":None}
        self.dict_token_index={0:"red_button",1:"purple_button",2:"tree_token",3:"axe_token",4:"empty_hand_token"}
        self.dict_token_hdc={"red_button":None,"purple_button":None,"tree_token":None,"axe_token":None,"empty_hand_token":None}
        ##Background dictionaries##
        self.dict_background_files={"total_background":None,"mem_backgrnd1":None,"mem_backgrnd2":None,"mem_main1":None,
                              "mem_main2":None,"mem_main_show":None,"stats_block":None}
        self.dict_background_hbmp={"total_background":None,"mem_backgrnd1":None,"mem_backgrnd2":None,"mem_main1":None,
                              "mem_main2":None,"mem_main_show":None,"stats_block":None}
        self.dict_background_index={0:"total_background",1:"mem_backgrnd1",2:"mem_backgrnd2",3:"mem_main1",
                              4:"mem_main2",5:"mem_main_show",6:"stats_block"}
        self.dict_background_hdc={"total_background":None,"mem_backgrnd1":None,"mem_backgrnd2":None,"mem_main1":None,
                              "mem_main2":None,"mem_main_show":None,"stats_block":None}
        ##Region dictionaries##
        self.dict_Player1_region={"down":None,"right":None,"left":None,"up":None}
        self.dict_Player2_region={"down":None,"right":None,"left":None,"up":None}
        return

class LPARAMS(Structure):
    _fields_=[("x",c_int),
              ("y",c_int)]
