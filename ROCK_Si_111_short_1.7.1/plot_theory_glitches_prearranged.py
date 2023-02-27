import numpy as np
import matplotlib.pyplot as plt
import math as m

########### Get data from theory_itsty_firstxtal.dat, the theory glitches
data_theory_glitches = np.loadtxt("./data/data_from_theory_glitches/Si_111_short/theory_itsty_firstxtal.dat")
size_data_theory_glitches = len(data_theory_glitches)
X_theory_glitches = np.zeros(size_data_theory_glitches)
Y_theory_glitches = np.zeros(size_data_theory_glitches)
i=0

list_of_glitches = []

for elt in data_theory_glitches:
    X_theory_glitches[i] = elt[0]
    Y_theory_glitches[i] = -elt[1]
    if (elt[1]!=0):        
        list_of_glitches.append(elt[0])
    i+=1    

#ask start(xmin) and end(xmax)
print("Chose an xmin and xmax between 5323 and 18914 eV")
x_min =int(input("Input xmin(integer):"))
x_max = int(input("Input xmax(integer):"))
plt.xlim(x_min,x_max)    

#select the glitches in the [xmin,xmax] interval
list_of_glitches_in_interval = []
for elt in list_of_glitches:
    if(elt>=x_min and elt<=x_max):
        list_of_glitches_in_interval.append(elt)
        
plt.plot(X_theory_glitches, Y_theory_glitches, marker='x', color="y", label='theory')
plt.legend(fontsize=10)
plt.title("Theory glitches data")
plt.xlabel("E")
plt.ylabel("Arbitrary units")
plt.show()

print("glitches between "+str(x_min)+" eV and "+str(x_max)+" eV are found for the following energies(eV):\n",list_of_glitches_in_interval)    
