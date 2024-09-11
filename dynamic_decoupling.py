# dynamic_decoupling.py

import cirq
import numpy as np

def udd_sequence(qubit, n, total_duration):
    """
    Implements the Uhrig Dynamical Decoupling (UDD) sequence for a given qubit.

    Parameters:
    - qubit: The target qubit to apply the UDD sequence.
    - n: The number of pulses.
    - total_duration: The total duration for the UDD sequence.

    Returns:
    - udd_circuit: A cirq.Circuit object implementing the UDD sequence.
    """
    udd_circuit = cirq.Circuit()
    
    def tj(j):
        return np.sin(np.pi * j / (2 * n + 2))**2

    last_t = 0
    for j in range(1, n + 1):
        t = int(round(tj(j) * total_duration))
        delay_duration = t - last_t
        if delay_duration > 0:
            udd_circuit.append(cirq.WaitGate(cirq.Duration(nanos=delay_duration)).on(qubit))
        udd_circuit.append(cirq.X(qubit))
        last_t = t

    final_delay = total_duration - last_t
    if final_delay > 0:
        udd_circuit.append(cirq.WaitGate(cirq.Duration(nanos=final_delay)).on(qubit))

    return udd_circuit

def cdd_sequence(qubit, levels):
    """
    Implements the Concatenated Dynamical Decoupling (CDD) sequence for a given qubit.

    Parameters:
    - qubit: The target qubit to apply the CDD sequence.
    - levels: The number of concatenation levels.

    Returns:
    - cdd_circuit: A cirq.Circuit object implementing the CDD sequence.
    """
    cdd_circuit = cirq.Circuit()
    base_sequence = cirq.Circuit(cirq.X(qubit))

    for _ in range(levels):
        cdd_circuit += base_sequence

    return cdd_circuit

def cpmg_sequence(qubit, n, tau):
    """
    Implements the Carr-Purcell-Meiboom-Gill (CPMG) sequence for a given qubit.

    Parameters:
    - qubit: The target qubit to apply the CPMG sequence.
    - n: Number of π pulses.
    - tau: Time interval between pulses.

    Returns:
    - cpmg_circuit: A cirq.Circuit object implementing the CPMG sequence.
    """
    cpmg_circuit = cirq.Circuit()
    for _ in range(n):
        cpmg_circuit.append(cirq.WaitGate(cirq.Duration(nanos=tau)).on(qubit))
        cpmg_circuit.append(cirq.X(qubit))
        cpmg_circuit.append(cirq.WaitGate(cirq.Duration(nanos=tau)).on(qubit))
    return cpmg_circuit
