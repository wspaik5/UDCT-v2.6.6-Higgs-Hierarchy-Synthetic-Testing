# UDCT v2.6.6 - Higgs Hierarchy Stabilization via Memory Kernel (Synthetic Testing)

This repository contains the synthetic testing framework for **UDCT v2.6.6**, focused on validating the Memory Kernel's performance under controlled conditions before full Monte Carlo integration.

## Background

This work is part of the ongoing UDCT (Unified Dynamical Critical Theory) research series on **Higgs Hierarchy Stabilization** using a Memory Kernel approach in geometric back-reaction.

## Repository Structure

## Key Components

- **Memory Kernel (`memory_kernel.py`)**: An improved implementation featuring Welford's online algorithm, outlier damping, and adaptation to sudden mean shifts.
- **Synthetic Generator (`synthetic_plaquette_generator.py`)**: Generates controllable plaquette-like time series with noise, spikes, and phase jump scenarios for systematic testing.

## Purpose of Synthetic Testing

Synthetic testing allows us to:
- Validate Memory Kernel behavior under known stress conditions (spikes, phase jumps)
- Ensure numerical stability over long sequences
- Prepare for integration with real U(1) lattice gauge theory Monte Carlo simulations

## Related Work

- v2.6.5: [UDCT-v2.6.5---Gauge-Field-Memory-Kernel-Higgs-Hierarchy](https://github.com/wspaik5/UDCT-v2.6.5---Gauge-Field-Memory-Kernel-Higgs-Hierarchy)
- Zenodo DOI (v2.6.5): https://doi.org/10.5281/zenodo.21320057

## Author

Won Shik Paik  
wspaik5@gmail.com
