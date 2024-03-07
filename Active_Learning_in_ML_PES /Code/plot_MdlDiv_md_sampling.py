import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_data(file_path):
    """Load data from the specified file."""
    data = pd.read_csv(file_path, sep='\s+', header=None, skiprows=1)
    return data

def filter_data(data, lower_limit, upper_limit):
    """Filter configurations based on force deviation limits."""
    filter_cond = np.logical_and(data[4] > lower_limit, data[4] < upper_limit)
    filtered_step_numbers = data[0][filter_cond].to_numpy()
    filtered_max_forces = data[4][filter_cond].to_numpy()
    
    return filtered_step_numbers, filtered_max_forces

def select_samples(step_numbers, max_samples=50):
    """Select a maximum number of samples, spaced evenly."""
    sep = int(len(step_numbers) / max_samples) + 1
    return step_numbers[::sep]

def plot_data(configs, MD_F_max, step_numbers, selected_forces, upper_limit, lower_limit):
    """Plot the MD configurations and highlight selected configurations."""
    plt.plot(configs, MD_F_max, 'o', markersize=3, color='k', alpha=0.5, label='Max F')
    plt.plot(step_numbers, selected_forces, 'o', markersize=3, color='r', label='Selected Max F')
    plt.axhline(y=upper_limit, color='r', linestyle='--', markersize=3)
    plt.axhline(y=lower_limit, color='r', linestyle='--', markersize=3)
    plt.ylim(ymin=0, ymax=1)
    plt.xlabel('MD Configurations')
    plt.ylabel('Max. standard deviation of atomic forces (eV/Å)')
    plt.legend(frameon=False)
    plt.rcParams['font.size'] = 13
    plt.rcParams['axes.linewidth'] = 4
    plt.show()

def main():
    file_path = 'model_devi.out'
    data = load_data(file_path)
    configs = np.linspace(1, 1001, 1001)
    upper_limit = 0.30
    lower_limit = 0.15
    
    filtered_step_numbers, filtered_max_forces = filter_data(data, lower_limit, upper_limit)
    selected_step_numbers = select_samples(filtered_step_numbers)
    selected_max_forces = data.loc[data[0].isin(selected_step_numbers), 4].to_numpy()

    plot_data(configs, data[4], selected_step_numbers, selected_max_forces, upper_limit, lower_limit)

if __name__ == '__main__':
    main()