from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi


# Initial Variable
# Bits is the number of bits for the input numbers
bits = 3

# Two numbers to be added, length must equal bits
bit1 = "011"
bit2 = "111"

# Sets up environment
qreg_q = QuantumRegister(bits*3, 'q')
creg_c = ClassicalRegister(bits+1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# First adder is different so it must be hard coded
# First adder is a half adder that does not take a carry bit as an input
# Each variable represents the index of a quantum register
# d1 - least significant digit of bit 1
# d2 - least significant digit of bit 2, d2 is also used as the sum bit
# cOut - outputs the carry bit
d1 = 0
d2 = 1
cOut = 2

# Encodes the enter input
if bit1[-1] == "1":
    circuit.x(qreg_q[d1])
if bit2[-1] == "1":
    circuit.x(qreg_q[d2])

# Code for half adder
circuit.ccx(qreg_q[d1], qreg_q[d2], qreg_q[cOut])
circuit.cx(qreg_q[cOut], qreg_q[d2])
circuit.x(qreg_q[cOut])
circuit.ccx(qreg_q[d1], qreg_q[2], qreg_q[d2])
circuit.x(qreg_q[cOut])

# Measures the sum bit
circuit.measure(qreg_q[d2], creg_c[d1])


# Adds full adders until the number of adders is equal to the number of bits
for i in range(bits-1):
    i += 1
    # Each variable represents the index of a quantum register
    # d1 - ith digit of bit 1 from the right
    # d2 - ith digit of bit 2 from the right
    # s - carry digit from previous adder and the sum digit for the current adder
    # cOut - outputs the carry bit
    d1 = 3*i
    d2 = 3*i+1
    s = 3*i-1
    cOut = 3*i+2

    # Encodes the enter input
    if bit1[-(i+1)] == "1":
        circuit.x(qreg_q[d1])
    if bit2[-(i+1)] == "1":
        circuit.x(qreg_q[d2])

    # Circuit for the full adder
    circuit.ccx(qreg_q[d1], qreg_q[d2], qreg_q[cOut])
    circuit.cx(qreg_q[d1], qreg_q[d2])
    circuit.ccx(qreg_q[d2], qreg_q[s], qreg_q[cOut])
    circuit.cx(qreg_q[d2], qreg_q[s])
    circuit.cx(qreg_q[d1], qreg_q[d2])

    circuit.measure(qreg_q[3*i-1], creg_c[i])

# Adds final measure for the carry bit of the last adder
circuit.measure(qreg_q[3*bits-1], creg_c[bits])
print(circuit)


# Simulates circuit 
from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
import matplotlib


simulator = AerSimulator()
circ = transpile(circuit, simulator)
# Run and get counts 
result = simulator.run(circ).result()
counts = result.get_counts(circ)
print(f"Bit 1: {bit1}\nBit 2: {bit2}\nSum: {list(counts.keys())[0]}")
# plot_histogram(counts)
# matplotlib.pyplot.show()


"""
OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

h q[0];
h q[1];
cx q[0], q[1];
x q[0];
cz q[1], q[0];
x q[0];
cx q[0], q[1];

h q[0];
h q[1];
x q[0];
x q[1];
cz q[0], q[1];
x q[0];
x q[1];
h q[0];
h q[1];

measure q[0] -> c[0];
measure q[1] -> c[1];

// @columns [0,0,2,3,4,5,6,14,15]

"""