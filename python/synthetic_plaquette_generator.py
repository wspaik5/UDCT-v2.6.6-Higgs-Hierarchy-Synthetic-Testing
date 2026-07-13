
"""
Synthetic Plaquette Generator Module (v2.6.6)

This module provides a flexible generator for creating synthetic plaquette
time series. It supports baseline sequence generation with noise and
autocorrelation, as well as controlled injection of spikes (outliers)
and phase jump-like mean shifts. These features are designed to test
the robustness and adaptation capability of the Memory Kernel.

Author: Won Shik Paik
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional


class SyntheticPlaquetteGenerator:
    """
    Generator for synthetic plaquette sequences used in Memory Kernel testing.

    This class can create realistic-looking plaquette time series and
    introduce artificial disturbances such as spikes and sudden mean shifts
    to evaluate how well the Memory Kernel handles different scenarios.
    """

    def __init__(self,
                 n_steps: int = 128,
                 base_mean: float = 0.852,
                 noise_level: float = 0.005,
                 autocorrelation: float = 0.25,
                 random_seed: Optional[int] = 42):
        """
        Initialize the synthetic plaquette generator.

        Parameters
        ----------
        n_steps : int
            Number of time steps to generate.
        base_mean : float
            Baseline mean value of the plaquette sequence.
        noise_level : float
            Standard deviation of added Gaussian noise.
        autocorrelation : float
            Strength of temporal correlation (0.0 \~ 0.4 recommended).
        random_seed : int or None
            Seed for reproducibility. Set to None for random behavior.
        """
        self.n_steps = n_steps
        self.base_mean = base_mean
        self.noise_level = noise_level
        self.autocorrelation = autocorrelation
        self.random_seed = random_seed
        self.sequence: Optional[np.ndarray] = None

        if random_seed is not None:
            np.random.seed(random_seed)

    def generate_baseline(self) -> np.ndarray:
        """
        Generate a baseline plaquette sequence with noise and autocorrelation.
        """
        noise = np.random.normal(0, self.noise_level, self.n_steps)
        seq = np.zeros(self.n_steps)
        seq[0] = self.base_mean + noise[0]

        for i in range(1, self.n_steps):
            seq[i] = (self.autocorrelation * (seq[i-1] - self.base_mean) +
                      noise[i] + self.base_mean)

        self.sequence = seq
        return seq

    def add_spikes(self, positions: List[int], magnitudes: List[float]) -> np.ndarray:
        """
        Add artificial spikes (out
