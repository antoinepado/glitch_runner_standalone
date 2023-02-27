import sys
if './modules' not in sys.path:
    sys.path.append('./modules')
    
import theory_glitches_module

#Input the three hkl vectors forming the B_hkl basis here.
#Si_111_short
xyz_hkl1 = [-1,2,-1]
xyz_hkl2 = [-1,0,1]
xyz_hkl3 = [1,1,1]

#generate the B and B_hkl vectors
e1,e2,e3,hkl1,hkl2,hkl3 = theory_glitches_module.vectors_B_Bhkl(xyz_hkl1,xyz_hkl2,xyz_hkl3)

#generate the change of basis matrix
mat2 = theory_glitches_module.change_of_basis_matrix(e1,e2,e3,hkl1,hkl2,hkl3)

#read Si_parsed.lau file and save h,k,l and reflec values from it
h,k,l,reflec = theory_glitches_module.read_lau_file()

############## Loop over a range of energies, advance one eV at a time
#For the full energy range, input 4500 to 27000 eV
energy_initial = int(input("Input initial energy(eV):"))
energy_final = int(input("Input final energy(eV):"))

#Input main HKL plane here.
H_HKL = 1
K_HKL = 1
L_HKL = 1

glitch_dict={}
glitch_dict = theory_glitches_module.loop_over_energies(energy_initial,energy_final,H_HKL,K_HKL,L_HKL,{},h,k,l,mat2,reflec,"Si_111_short")

path = "./theory_glitches_data/Si_111_short/"
theory_glitches_module.write_results_to_files(energy_initial,energy_final,glitch_dict,path)
print("Theory glitches (Si 111 short) have been written in a file called 'theory_itsty_firstxtal.dat'.") 
