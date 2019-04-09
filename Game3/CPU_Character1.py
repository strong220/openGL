##CPU CHARACTER 1##
import window_functions as wf
import window_structures as ws
import math
from Character3 import Character3_Sprite
def digitize(string,name):
    ##GGOOBPCC##
    out=0
    if len(string)>0:
        out=0
        if string[2]!="-":
            out=out+1
        if string[6]!="-" and string[6]!=name[0]:
            out=out-1
    return out
class CPU_Character1_Sprite(Character3_Sprite):
    def __init__(self,hdc_main,file_path_main,hwnd,name):
        ##BRING IN INHERITANCE CLASS##
        Character3_Sprite.__init__(self,hdc_main,file_path_main,hwnd,name)
        self.position.x=2000
        self.position.y=2000
    def Auto_Move(self,map_all,objects):
        ##DOWN,UP,LEFT,RIGHT##
        inputs=[False,False,False,False]
##        print(self.tile_position.x-2,self.tile_position.y-1)
##        print(map_all[self.tile_position.x-1])
        variables=[[self.tile_position.y],
                   [self.tile_position.x],
                   [len(map_all[0])],
                   [len(map_all)],
                   [digitize(map_all[self.tile_position.x-2][self.tile_position.y],self.Character)],
                   [digitize(map_all[self.tile_position.x-1][self.tile_position.y],self.Character)],
                   [digitize(map_all[self.tile_position.x][self.tile_position.y],self.Character)],
                   [digitize(map_all[self.tile_position.x+1][self.tile_position.y],self.Character)],
                   [digitize(map_all[self.tile_position.x+2][self.tile_position.y],self.Character)],
                   [digitize(map_all[self.tile_position.x-2][self.tile_position.y+1],self.Character)],
                   [digitize(map_all[self.tile_position.x-1][self.tile_position.y+1],self.Character)],
                   [digitize(map_all[self.tile_position.x][self.tile_position.y+1],self.Character)],
                   [digitize(map_all[self.tile_position.x+1][self.tile_position.y+1],self.Character)],
                   [digitize(map_all[self.tile_position.x+2][self.tile_position.y+1],self.Character)],
                   [digitize(map_all[self.tile_position.x-2][self.tile_position.y+2],self.Character)],
                   [digitize(map_all[self.tile_position.x-1][self.tile_position.y+2],self.Character)],
                   [digitize(map_all[self.tile_position.x][self.tile_position.y+2],self.Character)],
                   [digitize(map_all[self.tile_position.x+1][self.tile_position.y+2],self.Character)],
                   [digitize(map_all[self.tile_position.x+2][self.tile_position.y+2],self.Character)],
                   [digitize(map_all[self.tile_position.x-2][self.tile_position.y+3],self.Character)],
                   [digitize(map_all[self.tile_position.x-1][self.tile_position.y+3],self.Character)],
                   [digitize(map_all[self.tile_position.x][self.tile_position.y+3],self.Character)],
                   [digitize(map_all[self.tile_position.x+1][self.tile_position.y+3],self.Character)],
                   [digitize(map_all[self.tile_position.x+2][self.tile_position.y+3],self.Character)],
                   [digitize(map_all[self.tile_position.x-2][self.tile_position.y+4],self.Character)],
                   [digitize(map_all[self.tile_position.x-1][self.tile_position.y+4],self.Character)],
                   [digitize(map_all[self.tile_position.x][self.tile_position.y+4],self.Character)],
                   [digitize(map_all[self.tile_position.x+1][self.tile_position.y+4],self.Character)],
                   [digitize(map_all[self.tile_position.x+2][self.tile_position.y+4],self.Character)]]
        first_nodes=[[-.11,0,.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],      ##Am I at the top of the map? Yes is positive
                     [.11,0,-.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],     ##Am I at the bottom of the map? Yes is positive
                     [0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],     ##Am I at the left of the map? Yes is positive
                     [0,.11,0,-.1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],     ##Am I at the right of the map? Yes is positive
                     [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],     ##Is there a tree or object above me? Yes is positive
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],     ##Is there a tree or object below me? Yes is positive
                     [0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,1],      ##Is there a tree or object to my right? Yes is positive
                     [0,0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0]]     ##Is there a tree or object to my left? Yes is positive
        variables2=wf.MATMULT(variables,first_nodes)
        second_nodes=[[.1*0,-.1*0,0,0,1,-1,0,0],
                      [0,0,0,0,-1,1,0,0],
                      [0,0,-.1,.1,0,0,1,-1],
                      [0,0,.1,-.1,0,0,-1,1],
                      [0,0,0,0,-1,-1,-1,-1]]
        out=wf.MATMULT(variables2,second_nodes)
        for i in range(4):
            inputs[i]=(int(out[i][0]+.5)>=1)
        keypress=(int(out[4][0]+.5)>=1)
        self.Move(inputs,map_all,objects,keypress)
        return 0
        
##[[self.tile_position.y],
## [self.tile_position.x],
## [0],
## [0]]
