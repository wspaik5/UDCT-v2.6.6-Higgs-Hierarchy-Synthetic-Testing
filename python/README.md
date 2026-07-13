# UDCT v2.6.6 - Synthetic Testing (Python Module)

This folder contains the core Python modules for synthetic plaquette testing of the Memory Kernel, developed as part of UDCT v2.6.6 research on **Higgs Hierarchy Stabilization**.

## Purpose

These modules are designed to test the robustness and adaptation capability of the Memory Kernel under controlled synthetic conditions before integrating with full Monte Carlo simulations. This approach allows systematic validation of:

- Outlier (spike) detection and damping
- Response to sudden mean shifts (Phase Jump-like behavior)
- Long-term numerical stability

## Files

| File | Description |
|------|-------------|
| `memory_kernel.py` | Improved Memory Kernel implementation using Welford's online algorithm with strong outlier damping and adaptation to state changes. |
| `synthetic_plaquette_generator.py` | Flexible generator for creating synthetic plaquette time series with controllable noise, autocorrelation, artificial spikes, and phase jumps. |
| `README.md` | This file. |

## Usage Example

```python
from memory_kernel import MemoryKernel
from synthetic_plaquette_generator import SyntheticPlaquetteGenerator

# Generate synthetic data with spike and phase jump
gen = SyntheticPlaquetteGenerator(n_steps=128, noise_level=0.005)
gen.generate_baseline()
gen.add_spikes(positions=[40], magnitudes=[0.008])
gen.add_phase_jump(position=80, delta_mean=0.003)

# Apply Memory Kernel
kernel = MemoryKernel()
smoothed = [kernel.apply(val) for val in gen.get_sequence()]
