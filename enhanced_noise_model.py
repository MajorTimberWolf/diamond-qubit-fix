# enhanced_noise_model.py

import cirq

class AdvancedNoiseModel(cirq.NoiseModel):
    """Advanced noise model with dynamic noise suppression techniques."""

    def __init__(self, depolarizing_strength, damping_strength, phase_strength):
        # Define the noise components
        self.depolarizing_noise = cirq.depolarize(p=depolarizing_strength)
        self.amplitude_damping_noise = cirq.amplitude_damp(gamma=damping_strength)
        self.phase_damping_noise = cirq.phase_damp(gamma=phase_strength)

    def noisy_moment(self, moment, system_qubits):
        noisy_ops = []
        for op in moment:
            for qubit in op.qubits:
                # Apply all noise types to each operation
                noisy_ops.append(self.depolarizing_noise.on(qubit))
                noisy_ops.append(self.amplitude_damping_noise.on(qubit))
                noisy_ops.append(self.phase_damping_noise.on(qubit))
                noisy_ops.append(op)  # Append the original operation
        return cirq.Moment(noisy_ops)
