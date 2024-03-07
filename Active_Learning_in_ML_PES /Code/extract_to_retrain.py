import dpdata
import numpy as np
from pathlib import Path

def load_model_deviations(file_path='model_devi.out'):
    """Load model deviation data from a file."""
    return np.genfromtxt(file_path).transpose()

def compute_statistics(data, column, filter_multiplier_low=1, filter_multiplier_high=2, use_iqr=False, iqr_multiplier=1.5):
    """Compute basic statistics and filter data based on standard deviation or IQR."""
    if use_iqr:
        Q1, Q3 = np.percentile(data[column], [25, 75], interpolation='midpoint')
        IQR = Q3 - Q1
        lower_bound = Q1 - iqr_multiplier * IQR
        upper_bound = Q3 + iqr_multiplier * IQR
    else:
        std_dev = np.std(data[column])
        avg = np.mean(data[column])
        lower_bound = avg + filter_multiplier_low * std_dev
        upper_bound = avg + filter_multiplier_high * std_dev

    filter_cond = np.logical_and(data[column] > lower_bound, data[column] < upper_bound)
    filtered_indices = data[0][filter_cond]
    return filtered_indices

def select_snapshots(indices, max_snapshots=50):
    """Randomly select a specified maximum number of snapshots if necessary."""
    if len(indices) > max_snapshots:
        indices = np.random.choice(indices, max_snapshots, replace=False)
    return indices.astype(int)

def extract_and_save_system(indices, base_path='../explore_data', save_path='combined_data/selected_data'):
    """Extract a subsystem based on provided indices and save it."""
    suffix = Path().resolve().suffix[1:]
    dsys = dpdata.LabeledSystem(file_name=f'{base_path}/data{suffix}', fmt='deepmd/npy').sub_system(indices)
    dsys.to('deepmd/raw', save_path)

def process_snapshots(column, use_iqr=False, iqr_multiplier=1.5):
    """Process snapshots based on deviation in forces or energies."""
    data = load_model_deviations()
    filtered_indices = compute_statistics(data, column=column, use_iqr=use_iqr, iqr_multiplier=iqr_multiplier)
    selected_snapshots = select_snapshots(filtered_indices)
    print(selected_snapshots)
    extract_and_save_system(selected_snapshots)

process_snapshots(column=4) # For force deviations
# process_snapshots(column=1) # For energy deviations
# process_snapshots(column=4, use_iqr=True, iqr_multiplier=3) # Using IQR for force
