import numpy as np
from scipy.optimize import curve_fit
import pandas as pd

def calculate_bootstrap_statistics(data, num_resamples=10000):
    n = len(data)
    resamples = np.random.choice(data, (num_resamples, n), replace=True)
    resampled_means = np.mean(resamples, axis=1)
    mean = np.mean(resampled_means)
    std_error = np.std(resampled_means)
    return mean, std_error

def bin_data(data, column, bins):
    if isinstance(bins[0], tuple):  # For mass bins which are tuples
        binned_data = []
        for low, high in bins:
            binned_data.append(data[(data[column] >= low) & (data[column] < high)])
    else:  # For other bins which are numeric ranges
        digitized = np.digitize(data[column], bins)
        binned_data = [data[digitized == i] for i in range(1, len(bins))]
    return binned_data

def calculate_avg_std(binned_data, column):
    avg_values, std_errors = [], []
    for bin_data in binned_data:
        if len(bin_data) > 0:
            mean, std_error = calculate_bootstrap_statistics(bin_data[column])
            avg_values.append(mean)
            std_errors.append(std_error)
        else:
            avg_values.append(np.nan)
            std_errors.append(np.nan)
    return avg_values, std_errors

def completeness_model(z, a, b):
    return a / z + b

def fit_completeness_correction(hosts):
    # Create redshift bins
    redshift_quartiles = np.percentile(hosts['z_NSA'], [0, 25, 50, 75, 100])
    hosts['redshift_bin'] = pd.cut(hosts['z_NSA'], bins=redshift_quartiles, include_lowest=True)
    
    # Calculate mean redshift and corrected satellite count for each bin
    grouped = hosts.groupby('redshift_bin').agg({
        'z_NSA': 'mean',
        'n_sat': 'mean'
    }).reset_index()
    
    # Fit the completeness model
    popt, _ = curve_fit(completeness_model, grouped['z_NSA'], grouped['n_sat'])
    
    return popt

def apply_completeness_correction(hosts, a, b, target_avg=0.6):
    # Calculate current average
    current_avg = np.mean([completeness_model(z, a, b) for z in hosts['z_NSA']])
    
    # Adjust intercept to achieve target average
    adjustment = target_avg - current_avg
    new_b = b + adjustment
    
    # Apply correction to hosts
    hosts['completeness'] = hosts['z_NSA'].apply(lambda z: completeness_model(z, a, new_b))
    
    return hosts, new_b

# Add other analysis functions as needed