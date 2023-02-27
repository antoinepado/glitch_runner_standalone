import math as m
import numpy as np

def vectors_B_Bhkl(xyz_hkl1,xyz_hkl2,xyz_hkl3):
    ############## Express unit cell basis. The canonical basis B = {e1, e2, e3}.
    e1= np.array([[1,0,0]])

    e2= np.array([[0,1,0]])

    e3= np.array([[0,0,1]])

    ############## Express hkl1 hkl2 hkl3 in unit cell basis. The hkl basis, B_hkl = {hkl1, hkl2, hkl3}.
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
    

############## Express [xyz] vector in unit cell basis.
#[1,0,0] then [0,1,0] then [0,0,1] will be expressed.
def xyz_vector(x,y,z):
    print(x,y,z)
    xyz = np.array([[x,y,z]])
    #normalise it
    xyz_norm = m.sqrt(np.dot(xyz.reshape((1,3)),xyz.reshape((3,1))))
    xyz = xyz/xyz_norm
    return xyz


