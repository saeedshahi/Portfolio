import numpy as np
import matplotlib.pyplot as plt

def load_data(filename='model_devi.out'):
    """Load and transpose model deviation data."""
    return np.genfromtxt(filename).transpose()

def calculate_statistics(data, column, iqr_multiplier=1.5, select_max=50, std_multiplier=2, is_force=True):
    """Calculate and filter statistics based on IQR or standard deviation."""
    # Calculate IQR or standard deviation-based thresholds
    if is_force:
        Q1, Q3 = np.percentile(data[column], [25, 75], interpolation='midpoint')
        IQR = Q3 - Q1
        upper = Q3 + iqr_multiplier * IQR
    else:
        std_dev = np.std(data[column])
        avg = np.mean(data[column])
        upper = avg + std_multiplier * std_dev
    
    lower = np.min(data[column])  # General lower bound for visibility
    
    # Filter data based on calculated thresholds
    filter_cond = np.logical_and(data[column] > lower, data[column] < upper)
    filtered_data = data[column][filter_cond]
    filtered_indices = data[0][filter_cond]
    
    # Additional filtering based on average and standard deviation for force
    if is_force:
        avg = np.mean(filtered_data)
        std_dev = np.std(filtered_data)
        filter_final = np.logical_and(filtered_data > avg + std_dev, filtered_data < upper)
        selected_indices = filtered_indices[filter_final]
    else:
        selected_indices = filtered_indices
    
    # Select a maximum number of entries if necessary
    if len(selected_indices) > select_max:
        selected_indices = np.random.choice(selected_indices, select_max, replace=False)
    
    return selected_indices, upper, lower

def plot_data_with_highlights(data, column, selected_indices, upper, lower, ylabel, is_force=True):
    """Plot all data points and highlight selected ones based on statistical analysis."""
    plt.plot(data[0], data[column], 'o', markersize=3, color='k', alpha=0.5)
    if len(selected_indices) > 0:
        selected_values = data[column][selected_indices.astype(int)]
        plt.plot(selected_indices, selected_values, 'o', markersize=3, color='r')
    if is_force:
        plt.axhline(y=upper, color='blue', linestyle='--', markersize=3)
    else:
        plt.axhline(y=lower, color='r', linestyle='--', markersize=3)
        plt.axhline(y=upper, color='blue', linestyle='--', markersize=3)
    
    plt.ylim(ymin=0, ymax=np.max(data[column])*1.1)
    plt.rcParams['font.size'] = 13
    plt.rcParams['axes.linewidth'] = 4
    plt.xlabel('AIMD Configurations')
    plt.ylabel(ylabel)
    plt.legend(['All Data', 'Selected Data'], frameon=False)
    plt.show()

def main():
    data = load_data()
    
    # Plot for forces
    selected_indices, upper, _ = calculate_statistics(data, column=4, iqr_multiplier=3, is_force=True)
    plot_data_with_highlights(data, 4, selected_indices, upper, lower=0, ylabel='Max. standard deviation of atomic forces (eV/Å)', is_force=True)
    
    # Plot for energies - uncomment to use
    # selected_indices, upper, lower = calculate_statistics(data, column=1, iqr_multiplier=1.5, is_force=False)
    # plot_data_with_highlights(data, 1, selected_indices, upper, lower, ylabel='Standard deviation of energies (eV)', is_force=False)

if __name__ == '__main__':
    main()