"""
Memory Kernel Module (v2.6.6 - Adaptive Threshold Version)

This version introduces an adaptive large_diff_threshold that automatically
adjusts based on the current noise level (standard deviation) of the signal.
This makes the kernel more robust across different noise environments and
allows smaller Phase Jumps to trigger dynamic adaptation when appropriate.

Key improvements:
- Adaptive threshold using running standard deviation (Welford)
- Minimum floor for large_diff_threshold to prevent over-sensitivity
- Dynamic decay adaptation when sustained large changes are detected

Author: Won Shik Paik
"""

import numpy as np
from typing import List, Optional


class MemoryKernel:
    """
    Memory Kernel for plaquette stabilization with adaptive threshold.
    """

    def __init__(self,
                 memory_length: int = 20,
                 decay_factor: float = 0.85,
                 outlier_threshold: float = 0.008,
                 large_diff_threshold: float = 0.007,
                 min_large_diff_threshold: float = 0.004,      # ← 새로 추가 (하한선)
                 adaptive_threshold_factor: float = 2.8,       # ← 새로 추가 (표준편차 배수)
                 small_diff_threshold: float = 0.0005,
                 min_data_points: int = 5,
                 phase_jump_adaptation_steps: int = 8):
        """
        Initialize Memory Kernel parameters.
        """
        self.memory_length = memory_length
        self.decay_factor = decay_factor
        self.outlier_threshold = outlier_threshold
        self.large_diff_threshold = large_diff_threshold
        self.min_large_diff_threshold = min_large_diff_threshold
        self.adaptive_threshold_factor = adaptive_threshold_factor
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
        self.adaptation_counter: int = 0

    def _get_dynamic_large_diff_threshold(self) -> float:
        """
        Calculate dynamic large_diff_threshold based on current noise level.
        """
        if self.count < 10:
            return self.large_diff_threshold

        current_std = np.sqrt(self.variance / self.count)
        dynamic_threshold = current_std * self.adaptive_threshold_factor

        # Apply minimum floor
        return max(self.min_large_diff_threshold, dynamic_threshold)

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
        dynamic_large_diff = self._get_dynamic_large_diff_threshold()

        # === Outlier handling (Spike) ===
        if abs(raw_value - self.mean) > self.outlier_threshold or diff > dynamic_large_diff:
            damping = 0.15
            new_output = self.last_output * (1 - damping) + raw_value * damping
        else:
            # === Dynamic Adaptation for Phase Jump ===
            if diff > dynamic_large_diff:
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
    kernel = MemoryKernel()
    test_values = [0.852, 0.853, 0.851, 0.860, 0.852, 0.853]
    for val in test_values:
        out = kernel.apply(val)
        print(f"Raw: {val:.6f} -> Smoothed: {out:.6f}")
