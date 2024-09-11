# decoupling_sequences.py

import cirq
import numpy as np
from qubit_initialization import create_qubit_cirq

def bb1_sequence_cirq(phi):
    qubit, circuit = create_qubit_cirq()
    
    # Apply the BB1 sequence
    circuit.append(cirq.rz(phi)(qubit))
    circuit.append(cirq.rx(np.pi / 2)(qubit))
    circuit.append(cirq.rz(3 * phi)(qubit))
    circuit.append(cirq.rx(np.pi)(qubit))
    circuit.append(cirq.rz(3 * phi)(qubit))
    circuit.append(cirq.rx(np.pi / 2)(qubit))
    circuit.append(cirq.rz(phi)(qubit))
    
    # Add measurement
    circuit.append(cirq.measure(qubit, key='result'))
    
    return circuit

def udd_sequence_cirq(n, total_duration=1000):
    qubit, circuit = create_qubit_cirq()
    
    def tj(j):
        return np.sin(np.pi * j / (2 * n + 2))**2
    
    last_t = 0
    for j in range(1, n + 1):
        t = int(round(tj(j) * total_duration))
        delay_duration = t - last_t
        if delay_duration > 0:
            circuit.append(cirq.Z(qubit) ** (delay_duration / total_duration))
        circuit.append(cirq.X(qubit))
        last_t = t

    # Add final delay to reach total_duration
    final_delay = total_duration - last_t
    if final_delay > 0:
        circuit.append(cirq.Z(qubit) ** (final_delay / total_duration))
    
    # Add measurement
    circuit.append(cirq.measure(qubit, key='result'))
    
    return circuit
