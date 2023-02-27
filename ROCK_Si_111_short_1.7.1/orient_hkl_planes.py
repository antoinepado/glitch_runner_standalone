import sys
if './modules' not in sys.path:
    sys.path.append('./modules')
import change_basis_module
import numpy as np

#Input the three hkl vectors forming the B_hkl basis here.
#Si_111_short
xyz_hkl1 = [-1,2,-1]
xyz_hkl2 = [-1,0,1]
xyz_hkl3 = [1,1,1]

e1,e2,e3,hkl1,hkl2,hkl3 = change_basis_module.vectors_B_Bhkl(xyz_hkl1,xyz_hkl2,xyz_hkl3)

mat2 = change_basis_module.change_of_basis_matrix(e1,e2,e3,hkl1,hkl2,hkl3)

############## [1,0,0] is now expressed in the hkl basis B_hkl
xyz = change_basis_module.xyz_vector(1,0,0)
xyz_basis_hkl = np.dot(mat2,xyz.reshape((3,1)))
print("[1,0,0] vector expressed in basis hkl: ", xyz_basis_hkl)

############## [0,1,0] is now expressed in the hkl basis B_hkl
xyz = change_basis_module.xyz_vector(0,1,0)
xyz_basis_hkl = np.dot(mat2,xyz.reshape((3,1)))
print("[0,1,0] vector expressed in basis hkl: ", xyz_basis_hkl)

############## [0,0,1] is now expressed in the hkl basis B_hkl
xyz = change_basis_module.xyz_vector(0,0,1)
xyz_basis_hkl = np.dot(mat2,xyz.reshape((3,1)))
print("[0,0,1] vector expressed in basis hkl: ", xyz_basis_hkl)
