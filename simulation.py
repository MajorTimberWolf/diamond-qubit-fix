# simulation.py

import cirq

def simulate_measurement_cirq(circuit, noise_strength=0.1, repetitions=1000):
    # Define a noise model using depolarizing channel
    noise = cirq.depolarize(p=noise_strength)

    # Apply the noise directly to each gate in the circuit
    noisy_circuit = circuit.with_noise(noise)
    
    # Run the simulation
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=repetitions)
    
    return result
