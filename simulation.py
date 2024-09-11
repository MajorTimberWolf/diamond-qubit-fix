# simulation.py

import cirq
from qubit_characterization import measure_t1_t2, characterize_noise
from adaptive_control import real_time_feedback_control
from decoupling_sequences import choose_decoupling_sequence

def simulate_with_dynamic_feedback(qubit, simulator, initial_sequence, time_steps=100, repetitions=1000):
    """
    Simulates the qubit dynamics with real-time feedback to adjust decoupling sequences.

    Parameters:
    - qubit: The target qubit.
    - simulator: The quantum simulator.
    - initial_sequence: The initial decoupling sequence.
    - time_steps: The number of time steps for simulation.
    - repetitions: The number of repetitions for each time step simulation.

    Returns:
    - final_result: The result of the simulation with dynamic adjustments.
    """
    # Characterize the noise environment
    noise_profile = characterize_noise(qubit, simulator)
    print(f"Initial Noise Profile: {noise_profile}")

    # Measure initial T1 and T2 times
    t1, t2 = measure_t1_t2(qubit, simulator, repetitions)
    print(f"Initial T1 Time: {t1:.2f} ns, T2 Time: {t2:.2f} ns")

    # Choose an appropriate initial decoupling sequence based on noise
    chosen_sequence = choose_decoupling_sequence(qubit, noise_profile)
    circuit = cirq.Circuit(chosen_sequence)

    # Add measurement to the initial circuit
    circuit.append(cirq.measure(qubit, key='result'))

    # Run initial simulation
    measurements = simulator.run(circuit, repetitions=repetitions)
    print("Initial Measurements:", measurements)

    # Time-stepped simulation with dynamic feedback
    for step in range(time_steps):
        print(f"Time Step {step + 1}/{time_steps}")

        # Adjust the decoupling sequence based on feedback and current noise profile
        circuit = real_time_feedback_control(circuit, measurements, noise_profile, qubit)

        # Ensure a measurement gate is present in the adjusted circuit
        if not any(isinstance(op.gate, cirq.MeasurementGate) for op in circuit.all_operations()):
            circuit.append(cirq.measure(qubit, key='result'))

        # Run the simulation for this time step
        measurements = simulator.run(circuit, repetitions=repetitions)
        print(f"Measurements at Time Step {step + 1}:", measurements)

    # Return the final measurement results
    print("Final Measurements:", measurements)
    return measurements
