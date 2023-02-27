import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

#examples: 
compteur=1
glitches_value=[]
list_glitches_values=[]
with open("./data/data_from_theory_glitches/Si_111_short/theory_itsty_firstxtal_animation.dat") as ffirst:
    for line in ffirst:
        if line[0]!="#":
            itsty_deviation_value = line.strip().split(" ")
            glitches_value.append(-float(itsty_deviation_value[1]))
        else:
            list_glitches_values.append(glitches_value)
            glitches_value = []
                      
sizea=len(list_glitches_values[0])
Xdeux = np.zeros(sizea)
Ydeux = np.zeros(sizea)

i=0
incr=8251
for elt in list_glitches_values[0]:
    Xdeux[i]=incr 
    Ydeux[i]=elt
    incr+=1
    i+=1

fig = plt.figure()

ax = fig.add_subplot(xlim=(8251, 9201), ylim=(-30000, 1))

line, = plt.plot([],[])
phi_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

plt.xlim(8251,9201)
plt.ylim(-30000,1)

phi_list = []
angle_init=-1
phi_list.append(angle_init)
angle_finale=1
nn=41
step=(angle_finale-angle_init)/(nn-1)
while angle_init<=angle_finale:
    angle_init+=step
    phi_list.append(angle_init)

def init():
    line.set_data([],[])
    phi_text.set_text('')
    return line, phi_text,
        
def animate(i):
    j=0
    incr=8251
    for elt in list_glitches_values[i]:
        Xdeux[j]=incr 
        Ydeux[j]=elt
        incr+=1
        j+=1
                      
    line.set_data(Xdeux,Ydeux)  # update the data.
    phi_text.set_text('phi = '+ str(phi_list[int(i)]))
    
    return line, phi_text,

# This function will toggle pause on mouse click events
def on_click(event):
    if ani.running:
        ani.event_source.stop()
    else:
        ani.event_source.start()
    ani.running ^= True
    
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=41, interval=100, blit=True)

plt.title("Theory glitches for different azimutal angles")
plt.xlabel("E keV")
plt.ylabel("Arbitrary units")

ani.running=True

# Here we tell matplotlib to call on_click if the mouse is pressed
cid = fig.canvas.mpl_connect('button_press_event', on_click)      
     
plt.show()
