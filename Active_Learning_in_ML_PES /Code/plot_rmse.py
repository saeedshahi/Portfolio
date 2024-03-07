import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_force_data(file_name, shape=(4000, 192, 6)):
    """Load and reshape force data from a file."""
    data = np.genfromtxt(file_name, delimiter=" ")
    return np.reshape(data, shape)

def load_energy_data(file_names):
    """Load energy deviations for multiple tests and calculate standard deviation across them."""
    energies = [np.genfromtxt(file, delimiter=" ")[:, 1:] for file in file_names]
    data_mle = np.stack(energies)
    return np.std(data_mle, axis=0)

def calculate_force_deviations(force_files):
    """Load force data for multiple tests, calculate standard deviation, and find the max deviation."""
    forces = [load_force_data(file)[:, :, 3:] for file in force_files]
    data_mlf = np.stack(forces)
    fs_devi = np.linalg.norm(np.std(data_mlf, axis=0), axis=-1)
    return np.max(fs_devi, axis=-1)

def calculate_rmse(force_file):
    """Calculate RMSE for force predictions."""
    data_f = load_force_data(force_file)
    diffs = np.reshape(data_f[:, :, :3] - data_f[:, :, 3:], (4000, 192*3))
    return np.sqrt(np.mean(diffs**2, axis=1))

def rms_dict(x_ref, x_pred):
    """Calculate RMS errors between reference and predicted datasets."""
    x_ref, x_pred = np.array(x_ref), np.array(x_pred)
    if x_pred.shape != x_ref.shape:
        raise ValueError('WARNING: not matching shapes in rms')

    error_2 = (x_ref - x_pred) ** 2
    rmse_a = np.sqrt(np.average(error_2, axis=1))  # RMSE for each atom
    rmse_s = np.sqrt(np.average(error_2))  # RMSE for all atoms (system)
    std = np.sqrt(np.var(error_2))
    return {'rmse of each atom': rmse_a, 'rmse of all atoms': rmse_s, 'std': std}

# Load and process data
force_files = ["test1.f.out", "test2.f.out", "test3.f.out", "test4.f.out"]
energy_files = ["test1.e.out", "test2.e.out", "test3.e.out", "test4.e.out"]
es_devi = load_energy_data(energy_files)
fs_devi = calculate_force_deviations(force_files)

# Calculate RMSE for multiple force datasets and average them
rmses = [calculate_rmse(file) for file in force_files]
avg_rmse = np.mean(rmses, axis=0)

# Example gap RMSE calculation for the first force file
gap_rmse = rms_dict(load_force_data(force_files[0])[:, :, :3], load_force_data(force_files[0])[:, :, 3:])
print(avg_rmse)
print(gap_rmse)

# This section is prepared for future use. Uncomment and adjust as necessary for plotting.
'''
data = pd.read_csv('model_devi.out', sep='\s+', header=None, skiprows=1)
ML_FMax = data[4]

plt.plot(avg_rmse, ML_FMax, 'o', markersize=3, color='k', alpha=0.5)
plt.rcParams['font.size'] = 13
plt.rcParams['axes.linewidth'] = 4
plt.xlabel('Avg. of RMSE of Forces (eV/Å)')
plt.ylabel('Max. STD of ML Atomic Forces (norm) (eV/Å)')
plt.legend(frameon=False)
plt.savefig('MdlDev_plot.png', dpi=300)
plt.show()
'''