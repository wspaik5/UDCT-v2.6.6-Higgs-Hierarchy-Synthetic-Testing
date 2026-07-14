#!/usr/bin/env python3
"""
UDCT v2.6.6 - Adaptive Threshold Memory Kernel
for Higgs Hierarchy Stabilization

This module implements an improved Memory Kernel with:
- Adaptive detection threshold based on Welford's running standard deviation
- Dynamic Decay Adaptation for faster response to sustained Phase Jumps
- Median-based outlier rejection
- Warm-up phase
- Numerically stable statistics via Welford's algorithm

Author: Won Shik Paik
Email: wspaik5@gmail.com

================================================================================
Copyright and Citation Requirement
================================================================================

This software is provided for academic and non-commercial research use only.

If you use this code (or any derivative work) in your research, publication,
presentation, or software, you **must cite** the following technical note:

    Won Shik Paik,
    "UDCT v2.6.6: Higgs Hierarchy – Adaptive Threshold Memory Kernel
     Technical Note",
    July 2026.
    Zenodo DOI: (to be assigned upon upload)

Commercial use or redistribution requires prior written permission from the author.

This code is distributed in the hope that it will be useful for scientific
research, but WITHOUT ANY WARRANTY.
================================================================================
"""

from typing import List, Optional
import statistics


class MemoryKernel:
    """
    Memory Kernel with Adaptive Threshold for Higgs Hierarchy Stabilization (v2.6.6).

    Key improvements over v2.6.5:
        - Dynamic Large Diff Threshold computed from running standard deviation
        - Temporary reduction of decay_factor when sustained Phase Jump is detected
        - Better balance between stability and responsiveness
    """

    def __init__(
        self,
        decay_factor: float = 0.85,
        memory_length: int = 20,
        min_large_diff_threshold: float = 0.0025,
        adaptive_threshold_factor: float = 2.8,
        phase_jump_adaptation_steps: int = 8
    ):
        """
        Initialize the Adaptive Memory Kernel.

        Args:
            decay_factor: Base exponential decay factor (default 0.85)
            memory_length: Length of history buffer for median calculation
            min_large_diff_threshold: Minimum floor for dynamic threshold
            adaptive_threshold_factor: Multiplier for std → threshold
            phase_jump_adaptation_steps: How many steps to keep reduced decay after Phase Jump
        """
        if not 0 < decay_factor < 1:
            raise ValueError("decay_factor must be between 0 and 1")
        if memory_length < 1:
            raise ValueError("memory_length must be at least 1")

        self.decay_factor = decay_factor
        self.memory_length = memory_length
        self.min_large_diff_threshold = min_large_diff_threshold
        self.adaptive_threshold_factor = adaptive_threshold_factor
        self.phase_jump_adaptation_steps = phase_jump_adaptation_steps

        # Internal state
        self.history: List[float] = []
        self.last_output: Optional[float] = None

        # Warm-up control
        self.min_data_points: int = 3

        # Adaptive state
        self._phase_jump_counter: int = 0

        # Outlier threshold (fixed for stability)
        self.outlier_threshold: float = 0.008

        # Welford's online statistics
        self._count: int = 0
        self._mean: float = 0.0
        self._M2: float = 0.0

    def set_min_data_points(self, min_points: int) -> None:
        """
        Set the number of initial data points for the warm-up phase.

        During the warm-up phase, the kernel returns raw values without applying
        any smoothing. This prevents artificial bias during the initial transient
        regime of a simulation.
        """
