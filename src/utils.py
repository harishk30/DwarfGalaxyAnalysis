import numpy as np

def define_mass_bins():
    return [(9.5, 9.75), (9.75, 10), (10, 10.5), (10.5, 11)]

def define_color_bins():
    return np.linspace(0, 1, 6)

def define_metallicity_bins():
    return np.linspace(8.5, 9.5, 6)

def define_sfr_bins():
    return np.linspace(-3, 1, 6)

def define_ssfr_bins():
    return np.linspace(-13, -8.5, 6)
