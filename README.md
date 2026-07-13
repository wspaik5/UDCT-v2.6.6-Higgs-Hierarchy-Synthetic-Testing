
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



---

---

## UDCT v2.6.6 Memory Kernel Improvement History

### Overview
In v2.6.6, we significantly improved the Memory Kernel's ability to respond to Phase Jumps. 
By introducing an Adaptive Threshold mechanism and Dynamic Decay Adaptation, 
we effectively resolved the trade-off between outlier rejection and fine-grained state tracking.

### Performance Evolution (Phase Jump Scenario)

| Stage | Version | Key Changes | Phase Jump Reduction Rate | Notes |
|-------|---------|-------------|---------------------------|-------|
| 1 | Initial (Fixed Threshold) | Basic Memory Kernel | 63.74% | Slow response to Phase Jumps |
| 2 | Adaptive v1 | Dynamic threshold (`std × 2.8`) + `min_large_diff_threshold=0.004` | 78.80% | Major improvement |
| **3** | **Final** | Lowered `min_large_diff_threshold` to `0.0025` | **80.45%** | **Final version** |

### Key Improvements
- Maintained Welford-based real-time mean and variance tracking
- Introduced adaptive `large_diff_threshold` based on running standard deviation
- Lowered `min_large_diff_threshold` to `0.0025` to better detect small Phase Jumps in low-noise environments
- Added Dynamic Decay Adaptation to accelerate convergence after Phase Jumps

### Final Evaluation
- Phase Jump handling performance improved by **+16.7%p** compared to the initial version
- Successfully balanced outlier rejection and micro state tracking
- Gemini's overall assessment: **Production Ready**  
  → Recommended as the main engine for v2.6.6
