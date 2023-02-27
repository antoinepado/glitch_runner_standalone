#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math as m
import numpy as np
import re

def vectors_B_Bhkl(xyz_hkl1,xyz_hkl2,xyz_hkl3):
    ############## Express unit cell basis. The canonical basis B = {e1, e2, e3}.
    e1= np.array([[1,0,0]])

    e2= np.array([[0,1,0]])

    e3= np.array([[0,0,1]])

    ############## Express hkl1 hkl2 hkl3 in unit cell basis. The hkl basis, B_hkl = {hkl1, hkl2, hkl3}.
    #hkl1 = np.array([[1,-1,2]]), rectified, having this is not a right handed coord system, it is left handed
    hkl1 = np.array([xyz_hkl1])
    hkl1_norm = m.sqrt(np.dot(hkl1.reshape((1,3)),hkl1.reshape((3,1))))
    hkl1 = hkl1/hkl1_norm

    hkl2 = np.array([xyz_hkl2])
    hkl2_norm = m.sqrt(np.dot(hkl2.reshape((1,3)),hkl2.reshape((3,1))))
    hkl2 = hkl2/hkl2_norm

    hkl3 = np.array([xyz_hkl3])
    hkl3_norm = m.sqrt(np.dot(hkl3.reshape((1,3)),hkl3.reshape((3,1))))
    hkl3 = hkl3/hkl3_norm

    return e1,e2,e3,hkl1,hkl2,hkl3


def change_of_basis_matrix(e1,e2,e3,hkl1,hkl2,hkl3):
    ############## change-of-basis matrix
    #https://www.youtube.com/watch?v=hVmcRYD1KFQ
    #https://www.youtube.com/watch?v=CNIN7UpyXvo
    mat2 = np.array([[np.dot(e1.reshape((1,3)),hkl1.reshape((3,1)))[0][0], np.dot(e2.reshape((1,3)),hkl1.reshape((3,1)))[0][0], np.dot(e3.reshape((1,3)),hkl1.reshape((3,1)))[0][0]],
                     [np.dot(e1.reshape((1,3)),hkl2.reshape((3,1)))[0][0], np.dot(e2.reshape((1,3)),hkl2.reshape((3,1)))[0][0], np.dot(e3.reshape((1,3)),hkl2.reshape((3,1)))[0][0]],
                     [np.dot(e1.reshape((1,3)),hkl3.reshape((3,1)))[0][0], np.dot(e2.reshape((1,3)),hkl3.reshape((3,1)))[0][0], np.dot(e3.reshape((1,3)),hkl3.reshape((3,1)))[0][0]]])
    return mat2


def read_lau_file():
    ############## get the h,k,l F squared values from Si.lau
    #number of (hkl) planes in the Si.lau file
    sizeb=33792

    h = []
    k = []
    l = []
    reflec = []
    i=0
    with open("Si_parsed.lau") as file:
        for line in file:
            aaa=line.strip(" ").strip("\n")
            aaa = re.sub(' +',' ',aaa)      
            elt = aaa.split(" ")
            h.append(float(elt[0]))
            k.append(float(elt[1]))
            l.append(float(elt[2]))
            reflec.append(elt[5])
            i+=1
    return h,k,l,reflec


def kx_ky_kz(crystal_type,bragg_angle):  
    if(crystal_type=="Si_220"): #PHI 90 Si 220
        kx_value = m.cos(bragg_angle*m.pi/180)
        ky_value = 0
        kz_value = -m.sin(bragg_angle*m.pi/180)
    else: #Si_111_long and Si_111_short
        kx_value = 0
        ky_value = -m.cos(bragg_angle*m.pi/180)
        kz_value = -m.sin(bragg_angle*m.pi/180)
    return kx_value,ky_value,kz_value


def loop_over_energies(energy_initial,energy_final,H_HKL,K_HKL,L_HKL,glitch_dict,h,k,l,mat2,reflec,crystal_type):
    for egy in range(energy_initial,energy_final,1):
        ## Bragg angle / energy we select at
        #hits main plane with this bragg angle, equivalent to that energy
        h_main_plane = H_HKL 
        k_main_plane = K_HKL 
        l_main_plane = L_HKL 
        energy = egy    
        bragg_angle = (180/m.pi)*m.asin(12398.4198/(energy*2*(5.43096/m.sqrt(h_main_plane*h_main_plane+k_main_plane*k_main_plane+l_main_plane*l_main_plane))))
        
        #print on the same line       
        try:
            print(len(text_to_print)*' ',end='\r')
        except NameError:
            pass
        text_to_print = "bragg_angle "+str(bragg_angle)+" energy "+str(energy)
        print(text_to_print,end='\r')
        
        #k directly written in basis B_hkl
        #incoming ray
        kx,ky,kz = kx_ky_kz(crystal_type,bragg_angle)
        
        k_vector = np.array([[kx,ky,kz]])
        #normalise it, though it is already normalised
        k_vector_norm = m.sqrt(np.dot(k_vector.reshape((1,3)),k_vector.reshape((3,1))))
        k_vector = k_vector/k_vector_norm
        k_vector_basis_hkl = k_vector.reshape((3,1))

        glitches=[]
        i=0
        for elt in h:
            #[hkl] vector
            hkl = np.array([[h[i],k[i],l[i]]])
            #normalise it
            hkl_norm = m.sqrt(np.dot(hkl.reshape((1,3)),hkl.reshape((3,1))))
            hkl = hkl/hkl_norm

            #express the [hkl] vector in basis B_hkl
            hkl_basis_hkl = np.dot(mat2,hkl.reshape((3,1)))
            
            #Now that we now both have our k and [hkl] vector expressed in the same basis, B_hkl
            #we can calculate with the norm to the plane (ie [hkl] vector) and our k, the angle at which k hits the (hkl) plane   
            #see https://www.youtube.com/watch?v=wtpwM2y86So
            if ((np.dot(k_vector_basis_hkl.reshape((1,3)),hkl_basis_hkl.reshape((3,1)))[0][0])>=1):
                alpha = (180/m.pi)*m.acos((1)/(1*1)) #1*1 because i have normalised them
            elif ((np.dot(k_vector_basis_hkl.reshape((1,3)),hkl_basis_hkl.reshape((3,1)))[0][0])<=-1):
                alpha = (180/m.pi)*m.acos((-1)/(1*1))
            else:
                alpha = (180/m.pi)*m.acos((np.dot(k_vector_basis_hkl.reshape((1,3)),hkl_basis_hkl.reshape((3,1)))[0][0])/(1*1)) #1*1 because i have normalised them
            
            if ((np.dot(k_vector_basis_hkl.reshape((1,3)),-hkl_basis_hkl.reshape((3,1)))[0][0])>=1):
                alpha2 = (180/m.pi)*m.acos((1)/(1*1)) #1*1 because i have normalised them
            elif ((np.dot(k_vector_basis_hkl.reshape((1,3)),-hkl_basis_hkl.reshape((3,1)))[0][0])<=-1):
                alpha2 = (180/m.pi)*m.acos((-1)/(1*1))
            else:
                alpha2 = (180/m.pi)*m.acos((np.dot(k_vector_basis_hkl.reshape((1,3)),-hkl_basis_hkl.reshape((3,1)))[0][0])/(1*1)) #1*1 because i have normalised them

            angle_alpha = min(alpha,alpha2)
            theta = 90 - angle_alpha

            d1 = 5.43096/m.sqrt(h_main_plane*h_main_plane+k_main_plane*k_main_plane+l_main_plane*l_main_plane) #in unit cell basis
            theta_1 = bragg_angle

            d2 = 5.43096/m.sqrt(h[i]*h[i]+k[i]*k[i]+l[i]*l[i]) #in unit cell basis
            theta_2 = theta

            if(theta_2!=0):
                energy_selected_main_plane = 12398.4198/(2*d1*m.sin(theta_1*m.pi/180))
                energy_selected_parisitic_plane = 12398.4198/(2*d2*m.sin(theta_2*m.pi/180))
                if((energy_selected_main_plane-1)<=energy_selected_parisitic_plane<=(energy_selected_main_plane+1)):
                    #check to see if it is the main plane or -(main plane) , if it is dont add it as glitch
                    if(not (h[i]==h_main_plane and k[i]==k_main_plane and l[i]==l_main_plane) and  not(h[i]==-h_main_plane and k[i]==-k_main_plane and l[i]==-l_main_plane)):
                        glitches.append([h[i],k[i],l[i],reflec[i],theta_2,d2])

            i+=1

        glitch_dict[energy]=glitches
    return glitch_dict


def write_results_to_files(energy_initial,energy_final,glitch_dict,path):
    x = []
    y = []

    for egy in range(energy_initial,energy_final,1):
        x.append(egy)
        if(len(glitch_dict[egy])>=1):
            y.append(1)        
        else:
            y.append(0)

    ############## Write if we have found a glitch (1) or not (0) for the different energies we looped over.
    with open(path+'glitches_positions.txt', 'w') as f:
        i = 0
        for elt in x:
            f.write(str(elt)+' '+str(y[i]))
            f.write('\n')
            i+=1
        
    ############## Write details. Ie h, k, l, F squared and finally the angle (at which our incoming k vector hits the (hkl) plane) and d_hkl for that glitch.
    with open(path+'glitches_details.txt', 'w') as f:
        i = 0
        for egy in range(energy_initial,energy_final,1):
            if(len(glitch_dict[egy])>=1):
                f.write("### "+str(egy))
                f.write('\n')        
                for elt in glitch_dict[egy]:
                    f.write(str(elt[0])+' '+str(elt[1])+' '+str(elt[2])+' '+str(elt[3])+' '+str(elt[4])+' '+str(elt[5]))
                    f.write('\n')            

    ############## Read glitches_details.txt file and for each glitch assign a deviation intensity by adding their respective `F^2` plane reflection values.
    #The resulting deviation intensity is a simplified estimation.
    egy_itsty = {}
    egy=0
    itsty_sum = 0

    with open(path+"glitches_details.txt") as file: #read glitches_details file
        for line in file:
            iii = re.sub(' +',' ',line)
            eltee = iii.strip("\n").strip(" ").split(" ")
            if(len(eltee)==2):
                if(itsty_sum!=0):
                    egy_itsty[egy]=itsty_sum
                    itsty_sum=0
                    egy=int(eltee[1])
                else:
                    egy=int(eltee[1])
                
            if(len(eltee)==6):
                itsty_sum+=float(eltee[3])

    with open(path+'theory_itsty_firstxtal.dat', 'w') as f:
        i = energy_initial
        while(i<=energy_final):
            if i in egy_itsty.keys():
                f.write(str(i)+ " "+str(egy_itsty[i]))
                f.write("\n")    
            else: 
                f.write(str(i)+ " "+"0")
                f.write("\n")        
            i+=1

