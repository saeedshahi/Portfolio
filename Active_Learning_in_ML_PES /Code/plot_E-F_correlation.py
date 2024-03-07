import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_and_process_data():
    data = pd.read_csv('model_devi.out', sep='\s+', header=None, skiprows=1)
    data_f1 = np.genfromtxt("test1.f.out", delimiter=" ")
    data_f1 = np.reshape(data_f1, (4000, 192, 6))

    # Calculate RMSE for forces
    diff1 = np.reshape(data_f1[:, :, :3] - data_f1[:, :, 3:], (4000, 192*3))
    rmse1 = np.sqrt(np.mean(diff1**2, axis=1))

    max_std_f = data[4]  # Max standard deviation of forces
    max_std_e = data[1]  # Max standard deviation of energies, identical for each system due to singular value

    data_F = pd.read_csv('force.raw', sep='\s+', header=None)
    data_E = pd.read_csv('energy.raw', sep='\s+', header=None)

    energy = data_E[0]
    avg_fx = data_F.iloc[:, ::3].mean(axis=1)
    avg_fy = data_F.iloc[:, 1::3].mean(axis=1)
    avg_fz = data_F.iloc[:, 2::3].mean(axis=1)

    avg_aimd_f = np.linalg.norm(np.vstack((avg_fx, avg_fy, avg_fz)), axis=0)

    return rmse1, max_std_f, max_std_e, energy, avg_aimd_f

def plot_relationships(rmse1, max_std_f):
    plt.plot(rmse1, max_std_f, 'o', markersize=3, color='b', alpha=0.5)
    plt.rcParams['font.size'] = 13
    plt.rcParams['axes.linewidth'] = 4
    plt.xlabel('Avg. of error on predicted Forces (norm) (eV/Å)')
    plt.ylabel('Max. STD of ML Atomic Forces (norm) (eV/Å)')
    plt.legend(frameon=False)
    plt.savefig('Maxstd_F_avg_error_F.png', dpi=300)
    plt.show()

# Main function to orchestrate the data loading, processing, and plotting
def main():
    rmse1, max_std_f, max_std_e, energy, avg_aimd_f = load_and_process_data()
    plot_relationships(rmse1, max_std_f)

if __name__ == '__main__':
    main()