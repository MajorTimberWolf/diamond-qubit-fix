# simulation.py

import cirq

class CustomNoiseModel(cirq.NoiseModel):
    def __init__(self, noise_strength):
        self.noise_strength = noise_strength
        self.depolarizing_noise = cirq.depolarize(p=noise_strength)  # Depolarizing noise
        self.amplitude_damping_noise = cirq.amplitude_damp(gamma=noise_strength)  # Amplitude damping noise

    def noisy_operation(self, operation):
        # Apply both depolarizing and amplitude damping noise to each operation
        if cirq.num_qubits(operation) == 1:
            return [
                self.depolarizing_noise.on(operation.qubits[0]),
                self.amplitude_damping_noise.on(operation.qubits[0]),
                operation
            ]
        else:
            return operation

def simulate_measurement_cirq(circuit, noise_strength=0.1, repetitions=1000):
    # Use the custom noise model
    noise_model = CustomNoiseModel(noise_strength)

    # Apply the custom noise model to the circuit
    noisy_circuit = cirq.Circuit(cirq.NoiseModel.from_noise_model_like(noise_model).noisy_moments(circuit.moments, circuit.all_qubits()))
    
    # Run the simulation
    simulator = cirq.Simulator()
    result = simulator.run(noisy_circuit, repetitions=repetitions)
    
    return result
