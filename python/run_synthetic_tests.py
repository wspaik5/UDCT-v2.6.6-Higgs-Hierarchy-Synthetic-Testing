"""
run_synthetic_tests.py

Main script to run synthetic tests for Memory Kernel (v2.6.6)

This script combines SyntheticPlaquetteGenerator and MemoryKernel
to test the kernel's behavior under various controlled scenarios.

Scenarios included:
- Baseline (no disturbance)
- With artificial spikes (outliers)
- With phase jump (sudden mean shift)
- Combined spike + phase jump

Author: Won Shik Paik
"""

from memory_kernel import MemoryKernel
from synthetic_plaquette_generator import SyntheticPlaquetteGenerator
import numpy as np


def run_single_test_scenario(
    name: str,
    n_steps: int = 128,
    base_mean: float = 0.852,
    noise_level: float = 0.005,
    spike_positions: list = None,
    spike_magnitudes: list = None,
    phase_jump_position: int = None,
    phase_jump_delta: float = None
):
    """
    Run one synthetic test scenario and print results.
    """
    print(f"\n{'='*60}")
    print(f"Scenario: {name}")
    print(f"{'='*60}")

    # 1. Generate synthetic data
    gen = SyntheticPlaquetteGenerator(
        n_steps=n_steps,
        base_mean=base_mean,
        noise_level=noise_level,
        random_seed=42
    )
    gen.generate_baseline()

    # Add spikes if specified
    if spike_positions and spike_magnitudes:
        gen.add_spikes(spike_positions, spike_magnitudes)
        print(f"  - Added spikes at steps: {spike_positions}")

    # Add phase jump if specified
    if phase_jump_position and phase_jump_delta:
        gen.add_phase_jump(phase_jump_position, phase_jump_delta)
        print(f"  - Added phase jump at step {phase_jump_position} "
              f"(delta = {phase_jump_delta})")

    raw_sequence = gen.get_sequence()

    # 2. Apply Memory Kernel
    kernel = MemoryKernel(
        memory_length=20,
        decay_factor=0.85,
        outlier_threshold=0.008,
        large_diff_threshold=0.003
    )

    smoothed_sequence = []
    for val in raw_sequence:
        smoothed = kernel.apply(val)
        smoothed_sequence.append(smoothed)

    smoothed_sequence = np.array(smoothed_sequence)

    # 3. Print summary
    stats = kernel.get_statistics()
    print(f"\n  Memory Kernel Statistics:")
    print(f"    - Final mean     : {stats['mean']:.6f}")
    print(f"    - Final variance : {stats['variance']:.2e}")
    print(f"    - Final output   : {stats['final_output']:.6f}")

    # Simple comparison
    raw_std = np.std(raw_sequence)
    smoothed_std = np.std(smoothed_sequence)
    print(f"\n  Variability Reduction:")
    print(f"    - Raw std        : {raw_std:.6f}")
    print(f"    - Smoothed std   : {smoothed_std:.6f}")
    print(f"    - Reduction      : {(1 - smoothed_std/raw_std)*100:.2f}%")


def main():
    print("=" * 60)
    print("UDCT v2.6.6 - Synthetic Memory Kernel Test Suite")
    print("=" * 60)

    # Scenario 1: Baseline (no artificial disturbance)
    run_single_test_scenario(
        name="Baseline (No Disturbance)",
        n_steps=128,
        noise_level=0.005
    )

    # Scenario 2: With spikes
    run_single_test_scenario(
        name="With Artificial Spikes",
        n_steps=128,
        noise_level=0.005,
        spike_positions=[35, 72],
        spike_magnitudes=[0.008, -0.007]
    )

    # Scenario 3: With phase jump
    run_single_test_scenario(
        name="With Phase Jump",
        n_steps=128,
        noise_level=0.005,
        phase_jump_position=70,
        phase_jump_delta=0.003
    )

    # Scenario 4: Combined (spikes + phase jump)
    run_single_test_scenario(
        name="Combined: Spikes + Phase Jump",
        n_steps=128,
        noise_level=0.005,
        spike_positions=[35],
        spike_magnitudes=[0.008],
        phase_jump_position=70,
        phase_jump_delta=0.003
    )

    print("\n" + "=" * 60)
    print("All synthetic tests completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
