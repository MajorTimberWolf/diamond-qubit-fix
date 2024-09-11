# plotting.py

import matplotlib.pyplot as plt
import numpy as np

def plot_results_cirq(results, labels):
    plt.figure(figsize=(10, 6))
    
    for result, label in zip(results, labels):
        # Calculate the probability of measuring '0' state
        counts = result.histogram(key='result')
        prob_0 = counts[0] / sum(counts.values()) if 0 in counts else 0
        plt.plot([0, 1], [prob_0, prob_0], label=label)
    
    plt.xlabel('Time')
    plt.ylabel('Probability of |0>')
    plt.title('Qubit Fidelity During Measurement')
    plt.legend()
    plt.grid(True)
    plt.show()

