# xSAGA Dwarf Analysis

## Overview

This project focuses on the study of dwarf satellite galaxies using xSAGA data. We analyze how environmental factors of host galaxies affect the formation of satellite galaxies in paired and isolated Milky Way analogs.

## Repository Structure

- **`/data`**: Contains raw and processed data files
- **`/experiments`**: Jupyter notebooks with detailed analysis (bulk of the research)
- **`/src`**: Source code for data processing and analysis
- **`main.py`**: Main script to run the analysis pipeline

## Key Features

- Analysis of environmental factors influencing dwarf galaxy formation
- Comparison between paired and isolated Milky Way analogs using statistical methods such as bootstrapping, MCMC fitting, and more
- Utilization of xSAGA dataset for comprehensive galactic study of satellites

## Methodology

Our analysis is primarily conducted using Jupyter notebooks, stored in the `experiments` folder. The methods and code used in these experiments have been refactored into classes, providing an easy-to-use framework for future analysis.

## Findings

Our analysis reveals several key insights into how host environment affects satellite populations:

- **Paired vs. Isolated Galaxies:**
  - Paired galaxies consistently host more satellites than isolated galaxies across all mass bins
  - The satellite abundance difference between paired and isolated hosts increases with host mass
  - Satellites in paired systems show redder average G-R colors, suggesting older populations

- **Impact of LMC Analogs:**
  - Systems with LMC-like satellites (LMC=1 or LMC=2) have higher overall satellite abundances
  - The presence of LMC analogs correlates with a steeper increase in satellite numbers as host mass increases
  - Hosts with LMC analogs show a trend towards redder satellite populations, especially at higher host masses

- **Mass Dependence:**
  - Satellite abundance increases with host mass for all environmental categories
  - The rate of increase in satellite numbers with host mass is highest for systems with multiple large galaxies

- **Color Trends:**
  - G-R color of satellites increases with host mass across all environmental categories
  - Paired systems show redder satellites compared to isolated systems at fixed host mass

These findings suggest a complex interplay between host mass, environment, and the presence of massive satellites in shaping dwarf galaxy populations.

## Recent Updates

- Changed completeness model to exponential decay
- MCMC fitting for analysis of SSFR.
