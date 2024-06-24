import matplotlib.pyplot as plt
import numpy as np

def plot_satellites_vs_mass(avg_values, std_errors, mass_bins, title):
    fig, ax = plt.subplots()
    ax.bar(mass_bins, avg_values, yerr=std_errors, capsize=5)
    ax.set_xlabel('Mass Bins (Log M$_\odot$)')
    ax.set_ylabel('Average Satellites')
    ax.set_title(title)
    plt.savefig(f'results/final/plots/{title.lower().replace(" ", "_")}.png')
    plt.close()

def plot_satellites_vs_property(avg_values, std_errors, property_bins, property_name, mass_ranges, colors, markers):
    fig, ax = plt.subplots()
    for idx, (mass_range, color, marker) in enumerate(zip(mass_ranges, colors, markers)):
        bin_centers = (property_bins[:-1] + property_bins[1:]) / 2
        bin_centers_offset = bin_centers + (idx - 1.5) * 0.02
        ax.errorbar(bin_centers_offset, avg_values[idx], yerr=std_errors[idx], fmt=marker, color=color, label=f'Mass: {mass_range}', markersize=5)
    
    ax.set_xlabel(f'{property_name} Bins')
    ax.set_ylabel('Average Number of Satellites')
    ax.set_title(f'Average Number of Satellites vs. {property_name}')
    ax.legend(title='Mass Range')
    ax.set_ylim(bottom=0)
    
    bin_labels = [f'{property_bins[i]:.2f}-{property_bins[i+1]:.2f}' for i in range(len(property_bins)-1)]
    ax.set_xticks(bin_centers)
    ax.set_xticklabels(bin_labels)
    
    plt.savefig(f'results/final/plots/satellites_vs_{property_name.lower()}.png')
    plt.close()