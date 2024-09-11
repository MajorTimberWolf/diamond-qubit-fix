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

# Simulate measurement with different decoupling sequences
no_decoupling = cirq.Circuit(cirq.measure(cirq.GridQubit(0, 0), key='result'))
bb1_circuit = bb1_sequence_cirq(np.pi / 2)
udd_circuit = udd_sequence_cirq(5, total_duration=1000)  # Specify total_duration

# Get simulation results
results = [
    simulate_measurement_cirq(no_decoupling),
    simulate_measurement_cirq(bb1_circuit),
    simulate_measurement_cirq(udd_circuit)
]

# Plot results
plot_results_cirq(results, ['No Decoupling', 'BB1 Sequence', 'UDD Sequence'])

