
"""
Memory Kernel Module (v2.6.6)

This module implements an improved Memory Kernel designed for
stabilizing plaquette observables in lattice gauge theory simulations.
It features Welford's online algorithm for numerical stability,
outlier (spike) detection with strong damping, and adaptation to
sudden mean shifts (phase jump-like behavior).

Author: Won Shik Paik
"""

import numpy as np
from typing import List, Optional


class MemoryKernel:
    """
    Memory Kernel for plaquette stabilization.

    Key improvements in v2.6.6:
    - Welford's online algorithm for stable mean and variance tracking
    - Explicit warm-up phase
    - Strong damping for outliers and large fluctuations
    - Better adaptation to sudden state changes
    """

    def __init__(self,
                 memory_length: int = 20,
                 decay_factor: float = 0.85,
                 outlier_threshold: float = 0.008,
                 large_diff_threshold: float = 0.003,
                 small_diff_threshold: float = 0.0005,
                 min_data_points: int = 5):
        """
        Initialize Memory Kernel parameters.

        Parameters
        ----------
        memory_length : int
            Size of the history buffer.
        decay_factor : float
            Smoothing strength (higher = more memory effect).
        outlier_threshold : float
            Threshold to detect large outliers (spikes).
        large_diff_threshold : float
            Threshold for detecting significant sudden changes.
        small_diff_threshold : float
            Threshold for small changes (reserved for future extension).
        min_data_points : int
            Minimum steps required before full smoothing activates.
        """
        self.memory_length = memory_length
        self.decay_factor = decay_factor
        self.outlier_threshold = outlier_threshold
        self.large_diff_threshold = large_diff_threshold
        self.small_diff_threshold = small_diff_threshold
        self.min_data_points = min_data_points

        # Internal states
        self.history: List[float] = []
        self.last_output: Optional[float] = None
        self.count: int = 0
        self.mean: float = 0.0
        self.variance: float = 0.0
        self.smoothed_outputs: List[float] = []

    def _update_welford(self, new_value: float):
        """Update running mean and variance using Welford's method."""
        self.count += 1
        if self.count == 1:
            self.mean = new_value
            self.variance = 0.0
        else:
            old_mean = self.mean
            self.mean += (new_value - old_mean) / self.count
            self.variance += (new_value - old_mean) * (new_value - self.mean)

    def apply(self, raw_value: float) -> float:
        """
        Apply memory kernel to a raw value and return smoothed result.

        Parameters
        ----------
        raw_value : float
            Raw plaquette value at current time step.

        Returns
        -------
        float
            Smoothed output after applying memory effects.
        """
        self.history.append(raw_value)
        if len(self.history) > self.memory_length:
            self.history.pop(0)

        # Warm-up phase
        if len(self.history) < self.min_data_points:
            self.last_output = raw_value
            self.smoothed_outputs.append(raw_value)
            self._update_welford(raw_value)
            return raw_value

        diff = abs(raw_value - self.last_output) if self.last_output is not None else 0.0

        # Outlier / Large fluctuation handling
        if abs(raw_value - self.mean) > self.outlier_threshold or diff > self.large_diff_threshold:
            damping = 0.15
            new_output = self.last_output * (1 - damping) + raw_value * damping
        else:
            new_output = (self.decay_factor * self.last_output +
                          (1 - self.decay_factor) * raw_value)

        self.last_output = new_output
        self.smoothed_outputs.append(new_output)
        self._update_welford(raw_value)

        return new_output

    def get_statistics(self) -> dict:
        """Return current statistical summary."""
        return {
            "count": self.count,
