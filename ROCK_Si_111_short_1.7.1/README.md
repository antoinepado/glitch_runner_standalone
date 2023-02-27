# Simulations procedure 

## McXtrace simulation

### (hkl) orientations

`python3 theory_glitches_egy_selected.py`  

In the simulation of McXtrace the (hkl) planes need to be oriented properly. The script outputs the coordinates that are written in the McXtrace .instr files in parameters called ax,ay,az, bx,by,bz and cx,cy,cz.  

### Run McXtrace simulation

Run the McXtrace instrument located in the `instrument` folder by doing an energy scan and copy/paste the mccode.dat into the `/running_mcxtrace/mcxtrace_rock_111` folder.  

## Theory glitches

`python3 theory_glitches_egy_selected.py`  

The following code finds the positions of glitches on a desired range of energy by using Bragg's law `2*d*sin(θ)=n*λ`.  

# Results
 
## Plot theory glitches, ROCK and McXtrace data

### ROCK and McXtrace data

`python3 plot_scan.py`  

### Theory glitches

Need to add plot theory here. In notebook too.  

## Prearranged plots

### ROCK and McXtrace data (Si 111 short)

`python3 plot_scan_prearranged.py`  

Here are plots that have been done in advance for the Si 111 short crystal for different energy ranges and beamline settings (M2A/M2B angle ... etc).  

### Theory glitches data (Si 111 short)

`python3 plot_theory_glitches_prearranged.py`  

Here are the theory glitches found for the Si 111 short crystals.  

### Theory glitches data animation (Si 111 short)

`python3 plot_theory_glitches_animation.py`  

Here is an animation of the theory glitches between the energies 8251 and 9201 eV, with the azimuthal angle(the angle between the axis parallel to the long side of the crystal and the projection of the beam on the crystal's plane) going from -1 to 1 degrees for the Si 111 short crystals. It can be paused by simply clicking. When pausing on zero degrees, the result is the same as the above.  
