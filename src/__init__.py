# src/__init__.py

from .data_loading import load_saga_hosts, load_satellites, load_galspec_extra, load_satellite_host_pairs
from .data_processing import (
    process_hosts,
    combine_hosts_galspec,
    find_paired_hosts,
    corrected_sats,
    virial_mass,
    virial_radius,
    r_to_deg,
    volume,
    completeness,
    relative_velocity,
    SHMR,
    UniverseMachine_params
)
from .analysis import (
    calculate_bootstrap_statistics,
    bin_data,
    calculate_avg_std,
    fit_completeness_correction,
    apply_completeness_correction
)
from .plotting import plot_satellites_vs_mass, plot_satellites_vs_property
from .utils import (
    define_mass_bins,
    define_color_bins,
    define_metallicity_bins,
    define_sfr_bins,
    define_ssfr_bins
)

__all__ = [
    'load_saga_hosts',
    'load_satellites',
    'load_galspec_extra',
    'load_satellite_host_pairs',
    'process_hosts',
    'combine_hosts_galspec',
    'find_paired_hosts',
    'corrected_sats',
    'virial_mass',
    'virial_radius',
    'r_to_deg',
    'volume',
    'completeness',
    'relative_velocity',
    'SHMR',
    'UniverseMachine_params',
    'calculate_bootstrap_statistics',
    'bin_data',
    'calculate_avg_std',
    'fit_completeness_correction',
    'apply_completeness_correction',
    'plot_satellites_vs_mass',
    'plot_satellites_vs_property',
    'define_mass_bins',
    'define_color_bins',
    'define_metallicity_bins',
    'define_sfr_bins',
    'define_ssfr_bins'
]