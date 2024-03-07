from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import numpy as np
from ase.io import read, write
from ase import Atoms
from ase.geometry.analysis import Analysis
# We want RDF out to a distance of 15 Angstrom, with 200 bins
rng=4.0
bins = 100
atoms = read(filename='train_160_40.xyz', format='extxyz')
#write('Converted.xyz', atoms, format='extxyz', append=True)

CsPbI3 = Analysis(atoms)

rdf = CsPbI3.get_rdf(rmax = rng, nbins = bins, elements = ['Pb', 'I'])
rdf = [x for xs in rdf for x in xs]
print(type(rdf),len(rdf),rdf)
x = np.arange(bins) * rng / bins
Spline = make_interp_spline(x, rdf)
X = np.linspace(x.min(), x.max(), 500)
Y = Spline(X)
plt.plot(X, Y)
plt.show()
