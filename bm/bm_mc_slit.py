import math as m
import random
import matplotlib.pyplot as plt

### modified code from the original written by Erik Knudsen

#bending magnet's parameters
B=2.84 #Tesla magnet field strength
Ee=2.75 #GeV storage ring electron energy
Ie=0.5 #A ring current
Ec=0.665*Ee*Ee*B #critical energy

#1 to 50 keV energy range
E0=25.5
dE=24.5
emin=E0-dE
emax=E0+dE

#photon count
ncount=1e7
p0=1/ncount

#convert kev to angstrom and the reverse
E2K=0.506773091264796 
K2E=1.97326972808327

MELE=9.10938291e-31 #electron mass
CELE=1.602176487e-19 #electron charge
alpha=7.2973525664e-3 #fine structure constant
c=299792458 #m/s speed of light
oneoverc=1.0/c

k_c=Ec*E2K
mu_c = k_c*c/(2*m.pi) #critical angular frequency

#compute gamma
gamma=(Ee*1e9)/(MELE/CELE*c*c);#the extra CELE is to convert to eV
gamma2=gamma*gamma
igamma=1.0/gamma

dist=1 #metres

#electron ring beam size in horizontal and vertical plane in metres (rms)
sigex=54.9e-6
sigey=20.2e-6

#electron ring beam divergence horizontal and vertical in radians (rms)
sigepx=126.3e-6
sigepy=1.8e-6

#beam's size at dist (convolution of sigex/sigey and igamma)
s1x=m.sqrt(sigex*sigex + igamma*igamma*dist*dist)
s1y=m.sqrt(sigey*sigey + igamma*igamma*dist*dist)

DBL_EPSILON=2.22e-16

#slit width and height m
xwdith_slit=13e-3
yheight_slit=2.4e-3

#constants of Schwinger's equation (1)
cte_mult = (3*alpha/(4*m.pi**2))*(gamma**2)*(Ie/CELE)

#bessel function
def besselKnu(nu, x):
    h=0.5
    KK=0
    r=0
    maxiter=1000
    KK=m.exp(-x)/2.0
    dK=1
    while(dK>DBL_EPSILON and r<maxiter):
        r+=1
        dK=m.exp(-x*m.cosh(r*h))*m.cosh(nu*r*h)
        KK+=dK
    KK*=h
    return KK       

#integral(borne_inf, infinity) K(5/3,x) 
def integral_inf(borne_inf):
    h=0.01
    KK=0
    r=0
    maxiter=1000
    KK=0 #besselKnu(1.666666666666666666666666667,borne_inf), shouldn't the initial value be this?
    dK=1
    while(dK>DBL_EPSILON and r<maxiter):
        r+=1
        dK=besselKnu(1.666666666666666666666666667,borne_inf+r*h)
        KK+=dK
    KK*=h
    return KK

#generate a random number from normal law centered on 0
def randnorm():
    s=0
    while(s==0 or s>=1):
        u1 = random.random()
        u2 = random.random()
        v1 = 2*u1-1
        v2 = 2*u2-1
        s  = v1*v1+v2*v2
    X = v1*m.sqrt(-2*m.log(s)/s)
    return X

#propagate ray
def prop_dl(dl,x,y,z,kx,ky,kz,oneoverk,t):
    x = x+(dl)*kx*oneoverk
    y = y+(dl)*ky*oneoverk
    z = z+(dl)*kz*oneoverk
    t = t+(dl)*oneoverc
    return x,y,z,t

#backup to detector positionned at 8.7 m
def backup_to_detector(x,y,z,kx,ky,kz,oneoverk,k,t):    
    backup_dl = k*(z-8.7)/kz
    x = x-(backup_dl)*kx*oneoverk
    y = y-(backup_dl)*ky*oneoverk
    z = z-(backup_dl)*kz*oneoverk
    t = t-(backup_dl)*oneoverc
    return x,y,z,t

energy_vector_1D = []
itsy_vector_1D = []
itsy_vector_1D_slit = []
nbins=500
counter=0
e_bin=(emax-emin)/(nbins)

while counter<nbins:
    itsy_vector_1D.append(0)
    itsy_vector_1D_slit.append(0)
    energy_vector_1D.append(emin+counter*e_bin)
    counter+=1

photon_counter=0
photon_counter_slit=0

while photon_counter<=ncount:
    #initial source area
    t=0
    xx=0.33333333333*randnorm() #multiply by 1/3 to have a normal law between -1 and 1
    yy=0.33333333333*randnorm()
    x=xx*sigex
    y=yy*sigey
    z=0

    #pick random energy
    #uniform random number generation between emin and emax
    rand_0_1 = random.random()
    rand_0_2=rand_0_1*2
    rand_minus1_1=rand_0_2-1 #rand_minus1_1 is between -1 and 1
    e=E0+rand_minus1_1*dE
    k=e*E2K    
    oneoverk=1.0/k    
    k_kc=k/k_c
    mu = k*c/(2*m.pi)
    mu_muc = mu/mu_c
        
    #generate random vertical and horizontal angle of the ray
    angle=0.5*4e-3 #angle is the angle psi and theta will be generated over. Range of (-angle,angle).
    psi = 0.33333333333*randnorm()*angle
    theta = 0.33333333333*randnorm()*angle
    
    X = gamma*psi
    one_plus_xsquared = 1+X**2
    
    chi = mu_muc*(one_plus_xsquared)**(3/2)*(1/2)
    K2_3 = besselKnu(0.666666666666666666666666667,chi)
    K1_3 = besselKnu(0.333333333333333333333333334,chi)
    
    x1=theta #previously, this was multiplied by igamma
    y1=psi
    z1=dist

    dx=x1-x
    dy=y1-y
    dz=z1-z
    
    dl = m.sqrt(dx*dx+dy*dy+dz*dz)
    
    kx=(k*dx)/dl
    ky=(k*dy)/dl
    kz=(k*dz)/dl

    #origin point (xx*sigex,yy*sigey,0) then moved to (x1,y1,z1)
    x,y,z,t = prop_dl(dl,x,y,z,kx,ky,kz,oneoverk,t)

    while(z<=9):
        x,y,z,t = prop_dl(dl,x,y,z,kx,ky,kz,oneoverk,t)
        
    #backup to detector's exact position
    x,y,z,t = backup_to_detector(x,y,z,kx,ky,kz,oneoverk,k,t)
       
    p=p0    
    #Schwinger's equation (1), over the whole solid angle
    p*=cte_mult*mu_muc*mu_muc*(one_plus_xsquared)**2*(K2_3*K2_3+(X**2/(one_plus_xsquared))*K1_3*K1_3)
    bin_pos=m.floor((e-emin)/e_bin)
        
    itsy_vector_1D[bin_pos]+=p
    
    #photon goes through the slit if condition is met
    if(abs(x)<xwdith_slit/2.0 and abs(y)<yheight_slit/2.0):
        itsy_vector_1D_slit[bin_pos]+=p
        photon_counter_slit+=1
    
    photon_counter+=1
    print(photon_counter)

with open('bm_mc_eq1.txt', 'w') as f:
    i = 0
    for elt in energy_vector_1D:
        f.write(str(elt)+' '+str(itsy_vector_1D[i]))
        f.write('\n')
        i+=1

with open('bm_mc_slit_eq1.txt', 'w') as f:
    i = 0
    for elt in energy_vector_1D:
        f.write(str(elt)+' '+str(itsy_vector_1D_slit[i]))
        f.write('\n')
        i+=1

plt.plot(energy_vector_1D, itsy_vector_1D, marker='x', color="r", label='bm flux')
plt.plot(energy_vector_1D, itsy_vector_1D_slit, marker='x', color="y", label='bm flux through slit')
plt.legend(fontsize=10)
plt.xlabel("Energy (keV)")
plt.ylabel("Flux (ph/s/0.1%bw)")
plt.show()

print(photon_counter,photon_counter_slit)