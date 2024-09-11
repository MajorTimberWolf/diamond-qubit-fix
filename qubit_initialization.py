# qubit_initialization.py

import cirq

def create_qubit_cirq(state='0'):
    # Initialize a qubit
    qubit = cirq.GridQubit(0, 0)
    circuit = cirq.Circuit()

    # Prepare the initial state
    if state == '0':
        pass  # |0> is the default state
    elif state == '1':
        circuit.append(cirq.X(qubit))
    elif state == '+':
        circuit.append(cirq.H(qubit))
    elif state == '-':
        circuit.append(cirq.X(qubit))
        circuit.append(cirq.H(qubit))
    
    return qubit, circuit
