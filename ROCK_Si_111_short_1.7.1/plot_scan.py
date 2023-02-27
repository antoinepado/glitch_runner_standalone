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
figure, axis = plt.subplots(2)
#the scan that was done by the user with McXtrace
data_mcxtrace = np.loadtxt("./running_mcxtrace/mcxtrace_rock_111/mccode.dat")
size_data_mcxtrace = len(data_mcxtrace)
X_mcxtrace = np.zeros(size_data_mcxtrace)
Y_mcxtrace = np.zeros(size_data_mcxtrace)
i=0
for elt in data_mcxtrace:
    X_mcxtrace[i] = elt[0]
    Y_mcxtrace[i] = elt[5] #I0
    i+=1

axis[0].plot(X_mcxtrace, Y_mcxtrace, marker='.', color="b", label='McXtrace')
axis[0].legend(fontsize=10)    
axis[0].set_title("I0 McXtrace data")
axis[0].set_xlabel("E")
axis[0].set_ylabel("I0")

axis[1].plot(X_rock, Y_rock, marker='.', color="r", label='ROCK data '+info_plot)
axis[1].legend(fontsize=10)
axis[1].set_title("I0 ROCK data " + info_plot)
axis[1].set_xlabel("E")
axis[1].set_ylabel("I0")

plt.subplots_adjust(hspace=0.6)
plt.show()
print("McXtrace and ROCK data plotted.")
