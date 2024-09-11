# main.py

import cirq 
import numpy as np
import matplotlib.pyplot as plt
from qubit_initialization import create_qubit_cirq
from decoupling_sequences import bb1_sequence_cirq, udd_sequence_cirq
from simulation import simulate_measurement_cirq
from plotting import plot_results_cirq

# Main simulation
qubit, base_circuit = create_qubit_cirq('+')  # Create a qubit in the |+⟩ state

# Experiment with different noise strengths and parameters
noise_strengths = [0.1, 0.2, 0.3]  # Different noise strengths to test
n_values = [3, 5, 7]  # Different numbers of pulses for UDD sequence

for noise_strength in noise_strengths:
    for n in n_values:
        # Simulate measurement with different decoupling sequences
        no_decoupling = cirq.Circuit(cirq.measure(cirq.GridQubit(0, 0), key='result'))
        bb1_circuit = bb1_sequence_cirq(np.pi / 2)
        udd_circuit = udd_sequence_cirq(n=n, total_duration=1000)  # Specify total_duration and pulses

        # Get simulation results
        results = [
            simulate_measurement_cirq(no_decoupling, noise_strength=noise_strength),
            simulate_measurement_cirq(bb1_circuit, noise_strength=noise_strength),
            simulate_measurement_cirq(udd_circuit, noise_strength=noise_strength)
        ]

        # Plot results
        plot_results_cirq(results, [f'No Decoupling (Noise {noise_strength})', 
                                    f'BB1 Sequence (Noise {noise_strength})', 
                                    f'UDD Sequence (n={n}, Noise {noise_strength})'])