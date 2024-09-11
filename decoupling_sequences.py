# decoupling_sequences.py

import cirq
import numpy as np
from qubit_characterization import characterize_noise
from dynamic_decoupling import *

def choose_decoupling_sequence(qubit, noise_profile):
    """
    Chooses an optimal decoupling sequence based on the qubit's noise profile.

    Parameters:
    - qubit: The target qubit to apply the decoupling sequence.
    - noise_profile: Dictionary containing noise types and strengths.

    Returns:
    - chosen_sequence: A cirq.Circuit object representing the chosen decoupling sequence.
    """
    if noise_profile["low_frequency_noise"] > noise_profile["high_frequency_noise"]:
        chosen_sequence = udd_sequence(qubit, n=5, total_duration=1000)
    elif noise_profile["high_frequency_noise"] > noise_profile["low_frequency_noise"]:
        chosen_sequence = cdd_sequence(qubit, levels=3)
    else:
        chosen_sequence = cpmg_sequence(qubit, n=10, tau=100)

    return chosen_sequence
