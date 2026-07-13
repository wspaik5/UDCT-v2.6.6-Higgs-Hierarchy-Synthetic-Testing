"""
Memory Kernel Module (v2.6.6 - Improved)

This module implements an improved Memory Kernel designed for
stabilizing plaquette observables in lattice gauge theory simulations.

Key improvements in this version:
- Raised large_diff_threshold to reduce false phase jump detection
- Added simple dynamic adaptation (temporary lower decay) when 
  sustained large changes are detected (Phase Jump response)

Author: Won Shik Paik
"""

import numpy as np
from typing import List, Optional


class MemoryKernel:
    """
    Memory Kernel for plaquette stabilization (v2.6.6 improved version).
    """

    def __init__(self,
                 memory_length: int = 20,
                 decay_factor: float = 0.85,
                 outlier_threshold: float = 0.008,
                 large_diff_threshold: float = 0.007,      # ← 변경됨 (0.003 → 0.007)
                 small_diff_threshold: float = 0.0005,
                 min_data_points: int = 5,
                 phase_jump_adaptation_steps: int = 8):    # ← 새로 추가
        """
        Initialize Memory Kernel parameters.
        """
        self.memory_length = memory_length
        self.decay_factor = decay_factor
        self.outlier_threshold = outlier_threshold
        self.large_diff_threshold = large_diff_threshold
        self.small_diff_threshold = small_diff_threshold
        self.min_data_points = min_data_points
        self.phase_jump_adaptation_steps = phase_jump_adaptation_steps

        # Internal states
        self.history: List[float] = []
        self.last_output: Optional[float] = None
        self.count: int = 0
        self.mean: float = 0.0
        self.variance: float = 0.0
        self.smoothed_outputs: List[float] = []
        self.adaptation_counter: int = 0   # Phase Jump 적응용 카운터

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

        # === Outlier handling (Spike) ===
        if abs(raw_value - self.mean) > self.outlier_threshold or diff > self.large_diff_threshold:
            damping = 0.15
            new_output = self.last_output * (1 - damping) + raw_value * damping
        else:
            # === Dynamic Adaptation for Phase Jump ===
            if diff > self.large_diff_threshold:
                # 큰 변화가 지속되면 decay를 일시적으로 낮춤 (빠른 적응)
                current_decay = max(0.40, self.decay_factor - 0.35)
                self.adaptation_counter = self.phase_jump_adaptation_steps
            elif self.adaptation_counter > 0:
                current_decay = max(0.45, self.decay_factor - 0.25)
                self.adaptation_counter -= 1
            else:
                current_decay = self.decay_factor

            new_output = (current_decay * self.last_output +
                          (1 - current_decay) * raw_value)

        self.last_output = new_output
        self.smoothed_outputs.append(new_output)
        self._update_welford(raw_value)

        return new_output

    def get_statistics(self) -> dict:
        """Return current statistical summary."""
        return {
            "count": self.count,
            "mean": self.mean,
            "variance": self.variance / self.count if self.count > 1 else 0.0,
            "final_output": self.last_output
        }

    def reset(self):
        """Reset all internal states."""
        self.history.clear()
        self.smoothed_outputs.clear()
        self.last_output = None
        self.count = 0
        self.mean = 0.0
        self.variance = 0.0
        self.adaptation_counter = 0


if __name__ == "__main__":
    # Simple self-test
    kernel = MemoryKernel()
    test_values = [0.852, 0.853, 0.851, 0.860, 0.852, 0.853]
    for val in test_values:
        out = kernel.apply(val)
        print(f"Raw: {val:.6f} -> Smoothed: {out:.6f}")
