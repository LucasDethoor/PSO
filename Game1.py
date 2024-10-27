import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation
#1: PSO fundamentals: minimum of x2, plot of particles on graph


# ------------------------- Initial Parameters ------------------------- 

Space_Dim = 1
Size_Grid = np.array([100])   #max of each dim
Uni_Grid_Size = Size_Grid[0]

N_part=20
Delta = 2/(N_part-1)

w = 0.7         #Inertia Weight
Phip = 1.6      #Cognitive coefficient
Phig = 1.6      #Social coefficient


N_Steps = 15
anim_time=500 #ms


def F(x):
    return (x[0]-10)**2



# ------------------------- Classes and Functions ------------------------- 

class Grid:
    def __init__(self,size=[1]) -> None:
        Grid.Dim=len(size)
        Grid.Maxs = size
        


class Part:
    def __init__(self,name,pos,vel) -> None:
        Part.Name=name
        Part.Pos = pos
        Part.bkp = pos
        Part.Vel = vel
        

class Swarm:
    def __init__(self) -> None:
        Swarm.Particles = []
        Swarm.PartPositions = np.zeros((N_part,Space_Dim))



# ------------------------- Initialization ------------------------- 

#Grid
grid = Grid(Size_Grid) #Here [-100,100] 

#Particles
swarm = Swarm()

Initial_Pos = (np.random.rand(N_part,Space_Dim)-0.5)*2*Uni_Grid_Size        #In [-100,100]
Initial_Vel = (np.random.rand(N_part,Space_Dim)-0.5)*4*Uni_Grid_Size        #In [-200,200]

print("Vel ini:", Initial_Vel)

for i in range(N_part):
    pos_i = Initial_Pos[i,:]
    vel_i = Initial_Vel[i,:]
    part_i= Part(i,pos_i,vel_i)
    
    if i==0:
        swarm.SBKP = part_i.Pos
    elif F(part_i.bkp) < F(swarm.SBKP):
        swarm.SBKP = part_i.bkp

    swarm.Particles.append(part_i)
    swarm.PartPositions[i]=pos_i
    #print(part_i.bkp)

print("PosIni = ", swarm.PartPositions)


# ------------------------- Plot 1 ------------------------- 

f0=swarm.PartPositions
y = [0]*N_part

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(autoscale_on = False, xlim=(-Uni_Grid_Size, Uni_Grid_Size), ylim = (-1, 1))
line, = ax.plot(f0,y,'o', c="r" , label="Particles")
time_text = ax.text(0.05, 0.9, '', transform = ax.transAxes)
ax.legend()

# ------------------------- Process ------------------------- 

def update(frame):
    if frame<5:
        line.set_data(swarm.PartPositions,y)
        time_text.set_text(f"Initial Position")
        return line,time_text

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
        
        swarm.PartPositions[i] = part_i.Pos
        if F(part_i.Pos) < F(part_i.bkp):
            part_i.bkp = part_i.Pos
            if F(part_i.bkp)<F(swarm.SBKP):
                swarm.SBKP = part_i.bkp
    
    line.set_data(swarm.PartPositions,y)
    time_text.set_text(f"Nb of steps : {frame-4}\n Best known position : {swarm.SBKP}")
    return line,time_text


# ------------------------- Plot 2 ------------------------- 




ani = animation.FuncAnimation(fig=fig, func=update, frames=N_Steps, interval=anim_time, blit=True, repeat=False)
plt.show()


# ------------------------- Final ------------------------- 

print(swarm.SBKP)

print("\nEnd File")


