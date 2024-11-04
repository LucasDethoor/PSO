import matplotlib.pyplot as plt
import numpy as np


import matplotlib.animation as animation

import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
) # No need to call with pygame.



#1: PSO fundamentals: minimum of x2, plot of particles on graph


# ------------------------- Initial Parameters ------------------------- 

Space_Dim = 2
Size_Grid = np.array([100,100])   #max of each dim
Uni_Grid_Size = Size_Grid[0]

N_part=20
Delta = 2/(N_part-1)

w = 0.7         #Inertia Weight
Phip = 1.6      #Cognitive coefficient
Phig = 1.6      #Social coefficient


N_Steps = 15
Freq_Move = 10

anim_time=500 #ms

objective = [0,0]

pygame.init()

SCREEN_WIDTH = 600


#Colors:
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

#clock = pygame.time.Clock()
block_size = 5

Ratio_Screen_Grid=SCREEN_WIDTH / Uni_Grid_Size

def Fct(x):
    res = (x[0]-objective[0])**2+(x[1]-objective[1])**2
    return res

# ------------------------- Classes and Functions ------------------------- 

class Grid:
    def __init__(self,size=[1]) -> None:
        Grid.Dim=len(size)
        Grid.Maxs = size
        


class Part:
    def __init__(self,name,pos,vel) -> None:
        Part.Name=name
        Part.Pos = []
        Part.Pos[:] = pos
        Part.bkp = []
        Part.bkp[:] = pos
        Part.Vel = vel
        

class Swarm:
    def __init__(self) -> None:
        Swarm.Particles = []
        Swarm.PartPos = np.zeros((N_part,Space_Dim))
        Swarm.PartPastPos = np.zeros((N_part,Space_Dim))
        Swarm.SBKP = []



# ------------------------- Initialization ------------------------- 

#Grid
grid = Grid(Size_Grid) #Here [-100,100] 

#Particles
swarm = Swarm()

Initial_Pos = (np.random.rand(N_part,Space_Dim)-0.5)*2*Uni_Grid_Size        #In [-100,100]
Initial_Vel = (np.random.rand(N_part,Space_Dim)-0.5)*4*Uni_Grid_Size        #In [-200,200]

#print("Vel ini:", Initial_Vel)

for i in range(N_part):
    pos_i = Initial_Pos[i,:]
    vel_i = Initial_Vel[i,:]
    part_i= Part(i,pos_i,vel_i)
    
    if i==0:
        for j in range(Space_Dim):
            swarm.SBKP.append(part_i.Pos[j])
    elif Fct(part_i.bkp) < Fct(swarm.SBKP):
        swarm.SBKP[:]=part_i.Pos[:]

    swarm.Particles.append(part_i)
    swarm.PartPos[i][:] = pos_i[:]
    swarm.PartPastPos[i][:] = pos_i[:]

print("PosIni = \n", swarm.PartPos)


# ------------------------- Plot 1 ------------------------- 

win = pygame.display
win.set_caption("Test 2")
screen = win.set_mode((SCREEN_WIDTH,SCREEN_WIDTH))
font = pygame.font.Font(None, 30)




# ------------------------- Process ------------------------- 

def update():
    
    for i in range(N_part):
        part_i=swarm.Particles[i]
        for dim_ind in range(Space_Dim):
            [rp,rg] = np.random.rand(2)
            part_i.Vel[dim_ind] = w*part_i.Vel[dim_ind] + Phip*rp*(part_i.bkp[dim_ind]-part_i.Pos[dim_ind]) + Phig*rg*(swarm.SBKP[dim_ind]-part_i.Pos[dim_ind])

            new_pos = part_i.Pos[dim_ind] + part_i.Vel[dim_ind]
            if new_pos<-Size_Grid[dim_ind]:
                part_i.Pos[dim_ind] =-Size_Grid[dim_ind]
            elif new_pos>Size_Grid[dim_ind]:
                part_i.Pos[dim_ind] = Size_Grid[dim_ind]
            else:
                part_i.Pos[dim_ind] = new_pos
        
        swarm.PartPastPos[i][:] = swarm.PartPos[i][:]
        swarm.PartPos[i][:] = part_i.Pos[:]
        Evaluation_i = Fct(part_i.Pos)

        if Evaluation_i < Fct(part_i.bkp):
            part_i.bkp[:] = part_i.Pos[:]
            if Evaluation_i<Fct(swarm.SBKP):
                swarm.SBKP[:] = part_i.bkp[:]
    

    cur_best = Fct(swarm.SBKP)
    print("cur best eval = ",cur_best)


# ------------------------- Plot 2 ------------------------- 
step=0
ind_move_video = 0

run = True

while run:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False
        
        elif event.type == QUIT:
            run = False
        
    
    
    screen.fill(WHITE)
    
    if step < 10:
        text = "Initial Positions"
    
    elif step == 19:
        run = False

    else:
        if ind_move_video == 0:
            update()
            print(f"\nStep {step-9} :")
        text = f"Step {step-9} : Best Known Position = {swarm.SBKP[0]:.2e} , {swarm.SBKP[1]:.2e} "

    for i in range(N_part):
        x = int((0.1*(9-ind_move_video)*Swarm.PartPastPos[i][0] + 0.1*(ind_move_video+1)*Swarm.PartPos[i][0])*Ratio_Screen_Grid/2)+SCREEN_WIDTH//2
        y = int((0.1*(9-ind_move_video)*Swarm.PartPastPos[i][1] + 0.1*(ind_move_video+1)*Swarm.PartPos[i][1])*Ratio_Screen_Grid/2)+SCREEN_WIDTH//2
        pygame.draw.circle(screen, BLUE, (x,y), block_size)
    
    pygame.draw.circle(screen, GREEN, (objective[0]+SCREEN_WIDTH//2,objective[1]+SCREEN_WIDTH//2), 5)


    texte_surface = font.render(text,True,BLACK)

    screen.blit(texte_surface, ((SCREEN_WIDTH - texte_surface.get_width())//2, 60))
    if ind_move_video == 0:
        step += 1
    
    ind_move_video = (ind_move_video+1)%Freq_Move
    pygame.time.delay(int(1000/Freq_Move))
    pygame.display.update()



# ------------------------- Final ------------------------- 


pygame.quit()
print("\nEnd File")


