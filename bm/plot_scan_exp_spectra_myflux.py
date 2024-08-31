#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

########### Plot 

print("chose an angle theta and psi will be generated over")
print("type 1, 2, 3, 4 or 5 to chose the angle")
print("1: angle =   0.5 mrad")
print("2: angle =   1 mrad")
print("3: angle = 1.5 mrad")
print("4: angle =   2 mrad")
print("5: angle = 2.5 mrad")
angle_choice = str(input("Input the angle theta and psi will be generated over (-angle, angle):"))

####################################################### Calculated flux
data_mcxtrace = np.loadtxt("plot_flux_data/calc/bend_mag_calc.txt")
size_data_mcxtrace = len(data_mcxtrace)
X_mcxtrace = np.zeros(size_data_mcxtrace)
Y_mcxtrace = np.zeros(size_data_mcxtrace)
i=0
for elt in data_mcxtrace:
    X_mcxtrace[i] = elt[0]
    Y_mcxtrace[i] = elt[1] #flux is ph/s/0.1%b.w.
    i+=1

####################################################### Spectra Partial flux
data_spectra = np.loadtxt("plot_flux_data/spectra/partial_flux_parsed.txt")
size_data_spectra = len(data_spectra)
X_spectra = np.zeros(size_data_spectra)
Y_spectra = np.zeros(size_data_spectra)
i=0
for elt in data_spectra:
    X_spectra[i] = elt[0]
    Y_spectra[i] = elt[1] #flux is ph/s/0.1%b.w.
    i+=1

Y_mcxtrace = Y_mcxtrace/max(Y_mcxtrace)
Y_spectra = Y_spectra/max(Y_spectra)

####################################################### Spectra simplified flux
data_spectra_simplified = np.loadtxt("plot_flux_data/spectra/simplified_calc_parsed.txt")
size_data_spectra_simplified = len(data_spectra_simplified)
X_spectra_simplified = np.zeros(size_data_spectra_simplified)
Y_spectra_simplified = np.zeros(size_data_spectra_simplified)
i=0
for elt in data_spectra_simplified:
    X_spectra_simplified[i] = elt[0]
    Y_spectra_simplified[i] = elt[3] 
    i+=1                  #flux is ph/s/0.1%b.w.

Y_spectra_simplified = Y_spectra_simplified/max(Y_spectra_simplified)

####################################################### Schwinger's equation flux through a slit
data_eq1_slit_simplified = np.loadtxt("plot_flux_data/eq1_schwinger/"+angle_choice+"/bm_mc_slit_eq1.txt")
size_data_eq1_slit_simplified = len(data_eq1_slit_simplified)
X_eq1_slit_simplified = np.zeros(size_data_eq1_slit_simplified)
Y_eq1_slit_simplified = np.zeros(size_data_eq1_slit_simplified)
i=0
for elt in data_eq1_slit_simplified:
    X_eq1_slit_simplified[i] = elt[0]
    Y_eq1_slit_simplified[i] = elt[1] 
    i+=1                  #flux is ph/s/0.1%b.w.

Y_eq1_slit_simplified = Y_eq1_slit_simplified/max(Y_eq1_slit_simplified)

####################################################### Schwinger's equation flux 
data_eq1_simplified = np.loadtxt("plot_flux_data/eq1_schwinger/"+angle_choice+"/bm_mc_eq1.txt")
size_data_eq1_simplified = len(data_eq1_simplified)
X_eq1_simplified = np.zeros(size_data_eq1_simplified)
Y_eq1_simplified = np.zeros(size_data_eq1_simplified)
i=0
for elt in data_eq1_simplified:
    X_eq1_simplified[i] = elt[0]
    Y_eq1_simplified[i] = elt[1] 
    i+=1                  #flux is ph/s/0.1%b.w.

Y_eq1_simplified = Y_eq1_simplified/max(Y_eq1_simplified)

plt.plot(X_mcxtrace, Y_mcxtrace, marker='x', color="y", label='bending magnet flux calculated')
plt.plot(X_spectra, Y_spectra, marker='x', color="r", label='bm spectra partial flux, through slit')
plt.plot(X_spectra_simplified, Y_spectra_simplified, marker='x', color="b", label='bm spectra simplified flux')

plt.plot(X_eq1_slit_simplified*1000, Y_eq1_slit_simplified, marker='x', color="c", label='bm schwinger equation flux, through slit')
plt.plot(X_eq1_simplified*1000, Y_eq1_simplified, marker='x', color="g", label='bm schwinger equation flux')

plt.legend(fontsize=10)
plt.xlabel("Energy (eV)")
plt.ylabel("Normalized flux (ph/s/0.1%bw)")
plt.show()
print("flux plotted.")