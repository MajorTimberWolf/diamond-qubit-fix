# plotting.py

import matplotlib.pyplot as plt
import numpy as np

def plot_results_cirq(results, labels, time_steps):
    """
    Plots the results of the simulation, showing qubit fidelity over time.

    Parameters:
    - results: List of simulation results.
    - labels: List of labels for each result set.
    - time_steps: The number of time steps for the simulation.
    """
    plt.figure(figsize=(10, 6))

    # Process and plot each result
    for result, label in zip(results, labels):
        # Convert measurement results into a probability of '0' state over time
        counts = result.histogram(key='result')
        prob_0 = counts.get(0, 0) / sum(counts.values()) if counts else 0
        times = np.arange(1, time_steps + 1)
        fidelities = [prob_0] * len(times)  # Example fidelity; adjust as needed
        plt.plot(times, fidelities, label=label)

    plt.xlabel('Time Steps')
    plt.ylabel('Probability of |0⟩')
    plt.title('Qubit Fidelity During Measurement')
    plt.legend()
    plt.grid(True)
    plt.show()
