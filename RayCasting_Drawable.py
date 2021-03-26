import numpy as np
import pygame
Grid_Size = 32
H = 512
W = H * 2
BG_Color = (75,75,75)
Floor_Color = (137,69,0)
Sky_Color = (153,235,255)
Wall_ColorX = (0,230,77) #Wall Color when the Ray Collide with X axis
Wall_ColorY = (230,230,0) #Wall Color when the Ray Collide with Y axis
Wall_ColorMidleMouse = (200,0,200) #Wall Color when you put a Block with the middle mouse button
Wall_ColorMidleMouse2 = (200,0,0) #Another Color to the middle mouse block to add depth
DarkMax = 0.5 #Maximum Darkness when you get far from a block, 0,5 means the color will be 50% darker 
Grid_Color = (255,255,255) 
Win = pygame.display.set_mode((W,H))
pygame.display.set_caption("")
FPS = 60
StartPos = [40,40] #Player Start_Position

Map = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #1 for a block 0 for nothing and 2 for the middle mouse block
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,1],
        [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
        [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
        [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
        [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
        [1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,0,0,0,0,0,0,0,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]


class Player():
    x = StartPos[0]
    y = StartPos[1]
    Angle = 0
    Angular_Spd =  2 * np.pi/180
    Spd = 1.5
    Size = 15 
    Color = (255,255,0)
    Line_Color = (0,200,0)

    def draw(self):
        pygame.draw.rect(Win,self.Color,[self.x,self.y,self.Size,self.Size])

    def GridPos(self): #Get player Position on the Grid Map
        return [int(self.x/Grid_Size),int(self.y/Grid_Size)]

    def Im_GridPos(self,X,Y): #Get the Grid Map position of Custom Coordinates
        return [int(np.round(X/Grid_Size)),int(np.round(Y/Grid_Size))]

    def Move(self,Dir):
        Vect = [np.cos(self.Angle),np.sin(self.Angle)]
        #Collision By checking if the next Position is Available
        if Dir < 0:
            if Vect[0] > 0:
                if Vect[1] < 0:
                    TMPX = Vect[0] * (5) * Dir + self.x
                    TMPY = Vect[1] * (5) * Dir + self.y
                else:
                    TMPX = Vect[0] * (19) * Dir + self.x
                    TMPY = Vect[1] * (19) * Dir + self.y
            else:
                TMPX = Vect[0] * (5) * Dir + self.x
                TMPY = Vect[1] * (5) * Dir + self.y
                
        else:    
            TMPX = Vect[0] * self.Spd * Dir + self.x
            TMPY = Vect[1] * self.Spd * Dir + self.y
        ImPos = self.Im_GridPos(TMPX,TMPY)
        
        if not Map[ImPos[1]][ImPos[0]] > 0:
            self.x += Vect[0] * self.Spd * Dir
            self.y += Vect[1] * self.Spd * Dir
    
    def RayCast(self,Ang):
        MaxDist = [len(Map[0]),len(Map)]
        Vect = [np.cos(Ang),np.sin(Ang)]
        MapPos = self.GridPos()
        A = Vect[1]/Vect[0]
        B = (self.y + self.Size/2) - A * (self.x + self.Size/2)
        Dirs = [0,0]
        Init = [self.x + self.Size/2,self.y + self.Size/2]
        IsS = False #To Check if the Cube is the middle click cube to give it special color
        #Get the unit circle quadrant where the ray is in
        if Vect[0] < 0:
            Dirs[0] = -1
        else:
            Dirs[0] = 1
        if Vect[1] < 0:
            Dirs[1] = -1
        else:
            Dirs[1] = 1

        #ray Collision with X axis
        CollX = False
        if Dirs[1] > 0:
            for i in range(MapPos[1]+1,MaxDist[1]+1):
                Y = i*Grid_Size 
                X = (Y-B)/A
                if not np.abs(X) == np.inf and not np.abs(Y) == np.inf :
                    YMPos = int(Y/Grid_Size)
                    XMPos = int(X/Grid_Size)
                    if YMPos < MaxDist[1] and XMPos < MaxDist[0] and XMPos >= 0 and YMPos >= 0:
                        if Map[YMPos][XMPos] > 0:
                            RSLTX = [X,Y]
                            CollX = True
                            if Map[YMPos][XMPos] == 2:
                                IsS = True
                            else:
                                IsS = False
                            break
        else:
            for i in range(MapPos[1],0,-1):
                Y = i*Grid_Size
                X = (Y-B)/A
                if not np.abs(X) == np.inf and not np.abs(Y) == np.inf :
                    YMPos = int(Y/Grid_Size)-1
                    XMPos = int(X/Grid_Size)
                    if YMPos < MaxDist[1] and XMPos < MaxDist[0] and XMPos >= 0 and YMPos >= 0:
                        if Map[YMPos][XMPos] > 0:
                            RSLTX = [X,Y] 
                            CollX = True  
                            if Map[YMPos][XMPos] == 2:
                                IsS = True       
                            else:
                                IsS = False           
                            break
                        
        #ray Collision with Y axis
        CollY = False
        if Dirs[0] > 0:
            for i in range(MapPos[0]+1,MaxDist[0]+1):
                X = i*Grid_Size
                Y = A*X+B
                if not np.abs(X) == np.inf and not np.abs(Y) == np.inf :
                    YMPos = int(Y/Grid_Size)
                    XMPos = int(X/Grid_Size)

                    if YMPos < MaxDist[1] and XMPos < MaxDist[0] and XMPos >= 0 and YMPos >= 0:
                        if Map[YMPos][XMPos] > 0:
                            RSLTY = [X,Y]
                            CollY = True
                            if Map[YMPos][XMPos] == 2:
                                IsS = True
                            else:
                                IsS = False
                            break
                            
        else:
            for i in range(MapPos[0],0,-1):
                X = i*Grid_Size
                Y = A*X+B
                if not np.abs(X) == np.inf and not np.abs(Y) == np.inf :
                    YMPos = int(Y/Grid_Size)
                    XMPos = int(X/Grid_Size)-1
                    if YMPos < MaxDist[1] and XMPos < MaxDist[0] and XMPos >= 0 and YMPos >= 0:
                        if Map[YMPos][XMPos] > 0: 
                            RSLTY = [X,Y]
                            CollY = True
                            if Map[YMPos][XMPos] == 2:
                                IsS = True
                            else:
                                isS = False
                            break
        #Remove rays if they are in the wrong direction and replace it with the same dir
        if CollX: 
            VECTX = [RSLTX[0]-Init[0],RSLTX[1]-Init[1]]
            HYP = np.linalg.norm(VECTX)
            VECTX = [VECTX[0]/HYP,VECTX[1]/HYP]
            DirsX = [0,0]
            if VECTX[0] < 0:
                DirsX[0] = -1
            else:
                DirsX[0] = 1
            if VECTX[1] < 0:
                DirsX[1] = -1
            else:
                DirsX[1] = 1
            if not (DirsX[0] == Dirs[0] and DirsX[1] == Dirs[1]):
                if CollY:
                    CollX = False
                else:
                    self.RayCast(Ang-0.5*(np.pi/180))
        if CollY:
            VECTY = [RSLTY[0]-Init[0],RSLTY[1]-Init[1]]
            HYP = np.linalg.norm(VECTY)
            VECTY = [VECTY[0]/HYP,VECTY[1]/HYP]
            DirsY = [0,0]
            if VECTY[0] < 0:
                DirsY[0] = -1
            else:
                DirsY[0] = 1
            if VECTY[1] < 0:
                DirsY[1] = -1
            else:
                DirsY[1] = 1
            if not (DirsY[0] == Dirs[0] and DirsY[1] == Dirs[1]):
                if CollX:
                    CollY = False
                else:
                    self.RayCast(Ang-0.5*(np.pi/180))

        if not CollX: 
            if CollY:
                pygame.draw.line(Win,self.Line_Color,Init,RSLTY)
                DistY = np.linalg.norm(np.array(RSLTY)-np.array(Init))
                if IsS:
                   return [RSLTY,DistY,'SY',Ang] #S stands for special, this indicates that the block is a middle button block
                return [RSLTY,DistY,'Y',Ang]
        elif not CollY:
            pygame.draw.line(Win,self.Line_Color,Init,RSLTX)
            DistX = np.linalg.norm(np.array(RSLTX)-np.array(Init))
            if IsS:
                return [RSLTX,DistX,'SX',Ang]
            return [RSLTX,DistX,'X',Ang]
        else:
            #Check wich ray is shorter,the shorter is the one colliding with the wall
            DistX = np.linalg.norm(np.array(RSLTX)-np.array(Init))
            DistY = np.linalg.norm(np.array(RSLTY)-np.array(Init))
            if DistX < DistY:
                pygame.draw.line(Win,self.Line_Color,Init,RSLTX)
                if IsS:
                    return [RSLTX,DistX,'X',Ang]
                return [RSLTX,DistX,'X',Ang]
            else:
                pygame.draw.line(Win,self.Line_Color,Init,RSLTY)
                if IsS:
                    return [RSLTY,DistY,'SY',Ang]
                return [RSLTY,DistY,'Y',Ang]
        return[[448,448],448,'NoColl',Ang]
    
            
            

def DrawBackground():
    Win.fill(BG_Color)
    pygame.draw.rect(Win,Floor_Color,[H,H/2,H,H/2])
    pygame.draw.rect(Win,Sky_Color,[H,0,H,H/2])

def DrawMap(Map):
    x = 0
    y = 0
    for Line in Map:
        for Cube in Line:
            if Cube == 1:
                pygame.draw.rect(Win,Grid_Color,[x,y,Grid_Size-1,Grid_Size-1])
            elif Cube == 2:
                pygame.draw.rect(Win,Wall_ColorMidleMouse,[x,y,Grid_Size-1,Grid_Size-1])
            else:
                pygame.draw.rect(Win,(0,0,0),[x,y,Grid_Size,Grid_Size])
            x += Grid_Size
        y += Grid_Size
        x = 0

def Draw3D(View,P):
    Line_Width = int(H/len(View))
    i = 0
    for Line in View:
        #reduce the fisheye effect
        FishEye_Ang = P.Angle - Line[3] 
        if FishEye_Ang < 0:
            FishEye_Ang += np.pi*2
        elif FishEye_Ang > 2*np.pi:
            FishEye_Ang -= np.pi*2

        LineH = (Grid_Size*H/Line[1]) 
        if LineH > H:
            LineH = H

        LineH *= np.cos(FishEye_Ang)

        Off = H/2 - LineH/2 #Calculate the offset to have the rendering in the middle of the screen

        Shade = (Line[1]*DarkMax)/385 #Calculate how darker we should make the color depending on the distance of the wall
        if Line[2] == 'X':
            Actual_Color = [Wall_ColorX[0]-Wall_ColorX[0]*Shade,Wall_ColorX[1]-Wall_ColorX[1]*Shade,Wall_ColorX[2]-Wall_ColorX[2]*Shade]
        elif Line[2] == 'Y':
            Actual_Color = [Wall_ColorY[0]-Wall_ColorY[0]*Shade,Wall_ColorY[1]-Wall_ColorY[1]*Shade,Wall_ColorY[2]-Wall_ColorY[2]*Shade]
        elif Line[2][0] == 'S':
            if Line[2][1] == 'X':
                Actual_Color = [Wall_ColorMidleMouse[0]-Wall_ColorMidleMouse[0]*Shade,Wall_ColorMidleMouse[1]-Wall_ColorMidleMouse[1]*Shade,Wall_ColorMidleMouse[2]-Wall_ColorMidleMouse[2]*Shade]
            else:
                Actual_Color = [Wall_ColorMidleMouse2[0]-Wall_ColorMidleMouse2[0]*Shade,Wall_ColorMidleMouse2[1]-Wall_ColorMidleMouse2[1]*Shade,Wall_ColorMidleMouse2[2]-Wall_ColorMidleMouse2[2]*Shade]
        
        if not Line[2] == 'NoColl': 
            pygame.draw.line(Win,Actual_Color,[i*Line_Width+H,Off],[i*Line_Width+H,LineH+Off],Line_Width)
        i += 1
        

 

def main():
    run = True
    clock = pygame.time.Clock()
    P1 = Player()
    CanMove = True
    Coll = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_Pressed = pygame.key.get_pressed()
        Mouse_Pressed = pygame.mouse.get_pressed()
        Dir = 0
        if key_Pressed[pygame.K_LEFT]:
            P1.Angle -= P1.Angular_Spd
            Coll = False
        if key_Pressed[pygame.K_RIGHT]:
            P1.Angle += P1.Angular_Spd
            Coll = False
        if key_Pressed[pygame.K_DOWN]:
            Dir = -1
            Coll = False
        if key_Pressed[pygame.K_UP] and CanMove:
            Dir = 1
        
        if Mouse_Pressed[0]:
            Pos = pygame.mouse.get_pos()
            MapPos = [int(Pos[0]/Grid_Size),int(Pos[1]/Grid_Size)]
            if MapPos[0] < len(Map[0]) and MapPos[1] < len(Map):
                Map[MapPos[1]][MapPos[0]] = 1
        if Mouse_Pressed[2]:
            Pos = pygame.mouse.get_pos()
            MapPos = [int(Pos[0]/Grid_Size),int(Pos[1]/Grid_Size)]
            if MapPos[0] < len(Map[0]) and MapPos[1] < len(Map):
                Map[MapPos[1]][MapPos[0]] = 0
        if Mouse_Pressed[1]:
            Pos = pygame.mouse.get_pos()
            MapPos = [int(Pos[0]/Grid_Size),int(Pos[1]/Grid_Size)]
            if MapPos[0] < len(Map[0]) and MapPos[1] < len(Map):
                Map[MapPos[1]][MapPos[0]] = 2
        
        if not Dir == 0:
            P1.Move(Dir)
          
        DrawBackground()
        DrawMap(Map)
        P1.draw()
        StartAng = P1.Angle - 32*np.pi/180
        EndAng = P1.Angle + 32*np.pi/180
        Ang = StartAng
        View = []
        
        while Ang < EndAng:
                V = P1.RayCast(Ang)
                Ang += 0.5*(np.pi/180)
                View.append(V)
                if not Coll:
                    if V[1] < 15:
                        CanMove = False
                        Coll = True
                    else:
                        CanMove = True 

        if not len(View) % 2 == 0: #Making sure that the number of rays will divide the screen size correctly
            View.pop()
        Draw3D(View,P1)
        pygame.display.update()

    pygame.quit()
    

if __name__ == "__main__":
    main()