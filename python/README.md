# UDCT v2.6.6 - Adaptive Threshold Memory Kernel (Python)

This folder contains the Python implementation of the **Adaptive Threshold Memory Kernel** developed for **UDCT v2.6.6**.

## Overview

Version 2.6.6 introduces significant improvements to the Memory Kernel:

- **Adaptive Detection Threshold**: The Phase Jump detection threshold is now dynamically computed using Welford’s running standard deviation. This allows the kernel to automatically adjust sensitivity according to the current noise level.
- **Dynamic Decay Adaptation**: When a sustained Phase Jump is detected, the kernel temporarily reduces the decay factor to converge faster to the new state (typically within 5–6 steps instead of \~15 steps).
- **Improved Balance**: Maintains strong outlier rejection while significantly improving responsiveness to genuine state changes.

These features are particularly useful for long-running Monte Carlo simulations in the context of **Higgs hierarchy stabilization via geometric back-reaction**.

## Files

| File | Description |
|------|-------------|
| `memory_kernel.py` | Core `MemoryKernel` class with adaptive threshold and dynamic decay (v2.6.6) |
| `reproduce_v2.6.6_results.py` | Script to reproduce key results from the technical note |
| `README.md` | This file |

## Quick Start

### 1. Run the reproduction script

```bash
python reproduce_v2.6.6_results.py
