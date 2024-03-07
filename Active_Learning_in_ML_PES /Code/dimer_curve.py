import numpy as np
import matplotlib.pylab as plt
from ase import Atoms
from deepmd.calculator import DP


dimers = [Atoms("2O", cell=[100, 100, 100], positions=[[0,0,0], [x, 0,0]]) for x in np.linspace(2.5,6,100)]
#dimers = [Atoms("OH", cell=[100, 100, 100], positions=[[0,0,0], [x, 0,0]]) for x in np.linspace(0.35,6,100)]
#dimers = [Atoms("2H2O", cell=[100, 100, 100], positions=[[0.0, 0.817, 0.577], [0.0, -0.817, 0.577], [0, 0, 0], [0.0, 0.817, 0.577+x], [0.0, -0.817, 0.577+x], [x, 0,0]]) for x in np.linspace(2.5,6,100)]

dimer_curve300 = []
#dimer_curve400 = []
#dimer_curve600 = []

for dim300 in dimers:
    dim300.set_calculator(DP(model="graph.pb"))
    dimer_curve300.append(dim300.get_potential_energy())

plt.plot([dim300.positions[1,0] for dim300 in dimers], np.array(dimer_curve300)/2.0, color='b')
#plt.plot([dim400.positions[1,0] for dim400 in dimers], np.array(dimer_curve400)/2.0, color='blue')
#plt.plot([dim600.positions[1,0] for dim600 in dimers], np.array(dimer_curve600)/2.0, color='r')
#plt.plot(np.linspace(2.5,6,100), np.array(dimer_curve)/2.0, color='b', label = 'H2O-H2O')

plt.rcParams['font.size'] = 13
plt.rcParams['axes.linewidth'] = 4
plt.xlabel('r ($\AA$)')
plt.ylabel('Energy (eV)')
plt.xlim(xmin=0, xmax= 6)
#plt.ylim(ymin=-115, ymax= -85)
plt.savefig('dimer_curve_O-O.png', dpi=300)
plt.show()

