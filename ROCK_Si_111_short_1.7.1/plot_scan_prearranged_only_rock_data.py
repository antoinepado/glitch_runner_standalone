#!/usr/bin/env python3
# -*- coding: utf-8 -*-
########### Plot 

########### Ask what to plot
print("Give the atom(s) name you want to plot. Here is the list:")
print("For Si 111 short crystals:")
print("Ti, NiCu, Ni, FeNi, Cu, CoNi, 1_Fe, 2_Fe, 3_Fe.")
      
material_choice = str(input("Input AtomName:"))

data_rock_filename = "./data/digitalized_rock_data/si_111_court/"+material_choice+".txt"


import numpy as np
import matplotlib.pyplot as plt
import math as m
########### Get data from digitalized ROCK data.
data_rock = np.loadtxt(data_rock_filename, encoding='utf-8-sig',delimiter="\t")
size_data_rock = len(data_rock)
X_rock = np.zeros(size_data_rock)
Y_rock = np.zeros(size_data_rock)

i=0
for elt in data_rock:    
    X_rock[i] = elt[0]
    Y_rock[i] = elt[1]
    i+=1

info_plot = "Si 111 short " + material_choice



plt.plot(X_rock, Y_rock, marker='.', markersize=4, color="r", label='ROCK data '+info_plot)
plt.legend(fontsize=6)
plt.title("I0 ROCK data " + info_plot)
plt.xlabel("E")
plt.ylabel("I0")


plt.show()
print("ROCK data plotted.")
