from src.data_loading import load_saga_hosts, load_satellites, load_galspec_extra, load_satellite_host_pairs
from src.data_processing import process_hosts, combine_hosts_galspec, corrected_sats, find_paired_hosts
from src.analysis import bin_data, calculate_avg_std
from src.plotting import plot_satellites_vs_mass, plot_satellites_vs_property
from src.utils import define_mass_bins, define_color_bins, define_metallicity_bins, define_sfr_bins, define_ssfr_bins

def main():
    # Load data
    hosts = load_saga_hosts()
    satellites = load_satellites()
    gse = load_galspec_extra()
    satellite_pairs = load_satellite_host_pairs()

    # Process data
    hosts = process_hosts(hosts)
    hosts_comb = combine_hosts_galspec(hosts, gse)

    # Add satellite counts to hosts dataframe
    hosts['n_sat'] = hosts.index.map(lambda x: len(satellite_pairs.get(x, [])))

    # Find paired hosts
    paired_hosts = find_paired_hosts(hosts)

    # Calculate corrected satellite counts
    hosts['n_sats_corr'] = hosts.apply(lambda row: corrected_sats(row['n_sat'], row['z_NSA'], row['mass_NSA']), axis=1)

    print(f"Using completeness correction parameters: a = 0.04310515091442428, b = -1.100233264077512")

    # Add pairing information to hosts dataframe
    hosts['pairs'] = hosts.index.map(lambda x: 3 if x in paired_hosts and len(paired_hosts.get(x, [])) >= 2 else (2 if x in paired_hosts else 0))

    # Define bins
    mass_bins = define_mass_bins()
    color_bins = define_color_bins()
    metallicity_bins = define_metallicity_bins()
    sfr_bins = define_sfr_bins()
    ssfr_bins = define_ssfr_bins()

    # Perform analysis and create plots
    for column, bins, property_name in [
        ('mass_NSA', mass_bins, 'Mass'),
        ('g-r', color_bins, 'Color'),
        ('Metalicity', metallicity_bins, 'Metallicity'),
        ('SFR', sfr_bins, 'SFR'),
        ('SSFR', ssfr_bins, 'SSFR')
    ]:
        binned_data = bin_data(hosts, column, bins)
        avg_values, std_errors = calculate_avg_std(binned_data, 'n_sats_corr')
        
        if property_name == 'Mass':
            plot_satellites_vs_mass(avg_values, std_errors, [f'{b[0]}-{b[1]}' for b in mass_bins], f'Satellites vs {property_name}')
        else:
            plot_satellites_vs_property(avg_values, std_errors, bins, property_name, mass_bins, ['blue', 'green', 'red', 'orange'], ['o', 's', '^', 'D'])

    # Additional analysis for paired vs isolated hosts could be added here

if __name__ == "__main__":
    main()