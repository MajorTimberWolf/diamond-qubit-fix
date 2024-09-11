import cirq
from qubit_initialization import create_qubit_cirq
from qubit_characterization import measure_t1_t2, characterize_noise
from decoupling_sequences import (
    choose_decoupling_sequence, udd_sequence, cpmg_sequence, cdd_sequence
)
from simulation import simulate_without_noise
from real_time_feedback import real_time_feedback_control
from benchmarking import advanced_randomized_benchmarking
from plotting import plot_results_cirq, print_result_info

# Step 1: Initialize Qubit and Simulator
qubit, base_circuit = create_qubit_cirq(state='+')  # Initialize qubit in |+⟩ state
simulator = cirq.Simulator()
init_result = simulator.run(base_circuit, repetitions=1000)
init_state_counts = init_result.histogram(key='init_state')
print(f"Initial state counts: {init_state_counts}")

# Step 2: Characterize Qubit Interactions
t1, t2 = measure_t1_t2(qubit, simulator)
noise_profile = characterize_noise(qubit, simulator)
print(f"Measured T1 Time: {t1:.2f} ns, T2 Time: {t2:.2f} ns")
print(f"Noise Profile: {noise_profile}")

# Step 3: Apply Different Decoupling Sequences
sequences = {
    'UDD': udd_sequence(qubit, n=5, total_duration=1000),
    'CPMG': cpmg_sequence(qubit, n=10, tau=100),
    'CDD': cdd_sequence(qubit, levels=3)
}

results = []
labels = []

# Run simulation for each sequence
for label, seq in sequences.items():
    print(f"Starting simulation for {label} sequence...")
    result = simulate_without_noise(qubit, simulator, seq)
    results.append(result)
    labels.append(label)

# Step 4: Plot Results
plot_results_cirq(results, labels, time_steps=100)
