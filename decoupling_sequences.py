# decoupling_sequences.py

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
        # Calculate the timing for the j-th pulse using the UDD formula
        return total_duration * np.sin(np.pi * j / (2 * n + 2))**2

    last_t = 0
    for j in range(1, n + 1):
        t = int(round(tj(j)))
        delay_duration = t - last_t
        if delay_duration > 0:
            udd_circuit.append(cirq.WaitGate(cirq.Duration(nanos=delay_duration)).on(qubit))
        udd_circuit.append(cirq.X(qubit))
        last_t = t

    # Add final delay to reach total_duration
    final_delay = total_duration - last_t
    if final_delay > 0:
        udd_circuit.append(cirq.WaitGate(cirq.Duration(nanos=final_delay)).on(qubit))

    return udd_circuit

def cdd_sequence(qubit, levels):
    """
    Implements the Concatenated Dynamical Decoupling (CDD) sequence.

    Parameters:
    - qubit: The target qubit to apply the CDD sequence.
    - levels: The number of concatenation levels.

    Returns:
    - cdd_circuit: A cirq.Circuit object implementing the CDD sequence.
    """
    # Base case: simplest decoupling sequence (Carr-Purcell)
    if levels == 1:
        return cirq.Circuit(cirq.X(qubit), cirq.X(qubit))
    
    # Recursive concatenation
    base_sequence = cdd_sequence(qubit, levels - 1)
    cdd_circuit = cirq.Circuit(base_sequence, cirq.X(qubit), base_sequence)
    return cdd_circuit

def cpmg_sequence(qubit, n, tau):
    """
    Implements the Carr-Purcell-Meiboom-Gill (CPMG) sequence for a given qubit.

    Parameters:
    - qubit: The target qubit to apply the CPMG sequence.
    - n: The number of π-pulses.
    - tau: The time interval between pulses.

    Returns:
    - cpmg_circuit: A cirq.Circuit object implementing the CPMG sequence.
    """
    cpmg_circuit = cirq.Circuit()
    for _ in range(n):
        cpmg_circuit.append(cirq.WaitGate(cirq.Duration(nanos=tau)).on(qubit))
        cpmg_circuit.append(cirq.X(qubit))
    cpmg_circuit.append(cirq.WaitGate(cirq.Duration(nanos=tau)).on(qubit))
    return cpmg_circuit

def choose_decoupling_sequence(qubit, noise_profile):
    """
    Chooses an optimal decoupling sequence based on the qubit's noise profile.

    Parameters:
    - qubit: The target qubit to apply the decoupling sequence.
    - noise_profile: Dictionary containing noise types and strengths.

    Returns:
    - chosen_sequence: A cirq.Circuit object representing the chosen decoupling sequence.
    """
    # Determine dominant noise type and choose sequence accordingly
    if noise_profile["low_frequency_noise"] > noise_profile["high_frequency_noise"]:
        chosen_sequence = udd_sequence(qubit, n=5, total_duration=1000)
    elif noise_profile["high_frequency_noise"] > noise_profile["low_frequency_noise"]:
        chosen_sequence = cdd_sequence(qubit, levels=3)
    else:
        chosen_sequence = cpmg_sequence(qubit, n=10, tau=100)
    
    return chosen_sequence
