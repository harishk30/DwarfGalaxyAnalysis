import numpy as np
from astropy import units as u
from astropy.cosmology import Planck15 as cosmo
from astropy.coordinates import SkyCoord
from colossus.halo import mass_so
from colossus.cosmology import cosmology

cosmology.setCosmology('planck15')

# Fixed completeness parameters
_a = 0.04310515091442428
_b = -1.100233264077512

def process_hosts(hosts):
    hosts = hosts.sort_values('mass_NSA', ascending=False)
    hosts['g-r'] = hosts['M_g_NSA'] - hosts['M_r_NSA']
    return hosts

def combine_hosts_galspec(hosts, gse):
    hosts_comb = hosts.join(gse.set_index(["PLATE", "MJD", "FIBERID"]), on=["PLATE", "MJD", "FIBERID"], how="left")
    hosts_comb['SSFR'] = hosts_comb['SFR'] - hosts_comb['mass_NSA']
    return hosts_comb

def find_paired_hosts(hosts):
    host_coords = SkyCoord(hosts['ra_NSA'], hosts['dec_NSA'], unit='deg')
    paired_hosts = {}
    assigned_hosts = set()

    for id, host_coord in enumerate(host_coords):
        if hosts.index[id] not in assigned_hosts:
            vr = 1000 / np.sqrt(3)
            va = r_to_deg(vr, hosts.iloc[id]['z_NSA'])
            host_coord = SkyCoord(ra=[host_coord.ra], dec=[host_coord.dec])
            host_idx, paired_idx, angsep, _ = host_coord.search_around_sky(host_coords, va)
            sep = (angsep * cosmo.kpc_proper_per_arcmin(hosts.iloc[id].z_NSA)).to(u.kpc)
            
            paired_hosts[hosts.index[id]] = []
            for i, paired_val in enumerate(paired_idx):
                relative_v = relative_velocity(hosts.iloc[paired_val]['z_NSA'], hosts.iloc[id]['z_NSA'])
                mass_diff = abs(hosts.iloc[paired_val]['mass_NSA'] - hosts.iloc[id]['mass_NSA'])
                if (relative_v < 500 and 
                    sep[i] > (700 / np.sqrt(3)) * u.kpc and 
                    mass_diff < 0.5 and 
                    paired_val not in assigned_hosts):
                    paired_hosts[hosts.index[id]].append(hosts.index[paired_val])
                    assigned_hosts.add(hosts.index[paired_val])
                    assigned_hosts.add(hosts.index[id])
    
    return paired_hosts

def virial_mass(sm):
    halo_masses = np.arange(11, 15, 0.001)
    stellar_masses = SHMR(halo_masses, UniverseMachine_params)
    return halo_masses[np.argmin((sm - stellar_masses)**2)]

def virial_radius(sm, z):
    vm = virial_mass(sm)
    return mass_so.M_to_R(10 ** vm, z, 'vir')

def r_to_deg(r, z):
    return (r * u.kpc / cosmo.kpc_proper_per_arcmin(z)).to(u.arcmin)

def corrected_sats(sats, z, sm):
    sq_deg_per_sq_kpc = (cosmo.arcsec_per_kpc_proper(z).to(u.deg / u.kpc).value) ** 2
    virial_rad = virial_radius(sm, z) * u.kpc
    radius_diff = ((virial_rad)**2 - (36 * u.kpc)**2).to(u.kpc**2).value
    surface_area = np.pi * radius_diff * sq_deg_per_sq_kpc
    vol = volume(z)
    return (sats / completeness(z)) - 3.04 * surface_area - vol

def volume(z, delta_z=0.005):
    z_upper = min(z + delta_z, 0.03)
    z_lower = max(z - delta_z, 0)
    total_volume = (
        (cosmo.comoving_volume(0.03) - cosmo.comoving_volume(z_upper)) / 1.03**3 +
        (cosmo.comoving_volume(z_lower)) / (1 + z_lower)**3
    )
    volume = (
        ((cosmo.kpc_proper_per_arcmin(z) / (300 * u.kpc))**-2)
        .to(u.steradian)
        .value
        / (4 * np.pi)
        * total_volume
    )
    return (0.0142 * u.Mpc**-3) * volume

def completeness(z):
    global _a, _b
    return _a / z + _b

def relative_velocity(z1, z2, c=299792.458):
    return c * abs(z1 - z2) / (1 + (z1 + z2) / 2)

# SHMR function and UniverseMachine_params should be defined here
UniverseMachine_params = {
    "alpha": 1.957,
    "beta": 0.474,
    "gamma": -1.065,
    "delta": 0.386,
    "epsilon": -1.435,
    "M0": 12.081,
}

def SHMR(M_halo, params):
    x = M_halo - params["M0"]
    return (
        params["M0"] + params["epsilon"]
        - np.log10(10**(-params["alpha"]*x) + 10**(-params["beta"]*x))
        + 10**params["gamma"]*np.exp(-0.5 * (x / params["delta"])**2)
    )