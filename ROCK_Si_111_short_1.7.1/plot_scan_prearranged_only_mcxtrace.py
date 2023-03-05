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

########### For now only the data for the short cc has been done, we plot both McXtrace data and ROCK's data

data_mcxtrace = np.loadtxt("./data/data_mcxtrace/si_111_short/mccode_"+material_choice+".dat")
size_data_mcxtrace = len(data_mcxtrace)
X_mcxtrace = np.zeros(size_data_mcxtrace)
Y_mcxtrace = np.zeros(size_data_mcxtrace)
i=0
for elt in data_mcxtrace:
    X_mcxtrace[i] = elt[0]
    Y_mcxtrace[i] = elt[5] #I0
    i+=1
    
#same start(xmin) and end(xmax) for both plots so the x axis aligns
x_min_rock = float(m.floor(X_rock[0]))
x_max_rock = float(m.floor(X_rock[-1]))
pos_x_min_rock, =  np.where(np.isclose(X_mcxtrace, x_min_rock)) 
pos_x_max_rock, = np.where(np.isclose(X_mcxtrace, x_max_rock)) 

plt.plot(X_mcxtrace[pos_x_min_rock[0]:pos_x_max_rock[0]], Y_mcxtrace[pos_x_min_rock[0]:pos_x_max_rock[0]], marker='.', markersize=4, color="b", label='McXtrace')
plt.legend(fontsize=10)
plt.title("I0 McXtrace data")
plt.xlabel("E")
plt.ylabel("I0")

plt.show()
print("McXtrace and ROCK data plotted.")
