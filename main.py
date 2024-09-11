# main.py

import cirq
from qubit_initialization import create_qubit_cirq
from qubit_characterization import measure_t1_t2, characterize_noise
from dynamic_decoupling import udd_sequence, cdd_sequence, cpmg_sequence
from decoupling_sequences import choose_decoupling_sequence
from simulation import simulate_with_dynamic_feedback
from adaptive_control import real_time_feedback_control  # Newly added import
from benchmarking import advanced_randomized_benchmarking, process_tomography
from plotting import plot_results_cirq

# Step 1: Initialize Qubit and Simulator
qubit, base_circuit = create_qubit_cirq('+')  # Initialize qubit in |+⟩ state
simulator = cirq.Simulator()

# Step 2: Characterize Qubit Interactions and Noise Profiles
t1, t2 = measure_t1_t2(qubit, simulator)
noise_profile = characterize_noise(qubit)

# Step 3: Choose Optimal Dynamical Decoupling Sequence
chosen_sequence = choose_decoupling_sequence(qubit, noise_profile)
circuit = cirq.Circuit(chosen_sequence)

# Step 4: Simulate with Dynamic Feedback Control
final_result = simulate_with_dynamic_feedback(qubit, simulator, circuit)

# Step 5: Benchmark and Validate Effectiveness
fidelity = advanced_randomized_benchmarking(circuit, simulator)
print(f"Fidelity after applying dynamical decoupling: {fidelity:.4f}")

# Optionally, conduct process tomography
process_matrix = process_tomography(circuit, simulator)

# Step 6: Plot Results
plot_results_cirq([final_result], ['Dynamic Feedback with Tailored Decoupling'])

# Step 7: Output Results
print(f"T1 Time: {t1:.2f} ns, T2 Time: {t2:.2f} ns")
print(f"Noise Profile: {noise_profile}")
print(f"Final Benchmark Fidelity: {fidelity:.4f}")
