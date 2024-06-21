from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from numpy import pi

bits = 5

bit1 = "11111"
bit2 = "00111"

qreg_q = QuantumRegister(bits*3+1, 'q')
creg_c = ClassicalRegister(bits+1, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# First bit is different so it must be hard coded
# It must have a designated empty carry bit because it receives not carry bit from the prior adder
d1 = 0
d2 = 1
s = 2
cOut = 3
if bit1[-1] == "1":
    circuit.x(qreg_q[d1])
if bit2[-1] == "1":
    circuit.x(qreg_q[d2])
circuit.ccx(qreg_q[d1], qreg_q[d2], qreg_q[cOut])
circuit.cx(qreg_q[d1], qreg_q[d2])
circuit.ccx(qreg_q[d2], qreg_q[s], qreg_q[cOut])
circuit.cx(qreg_q[d2], qreg_q[s])
circuit.cx(qreg_q[d1], qreg_q[d2])
circuit.measure(qreg_q[2], creg_c[0])


# Adds another adder to match the number of bits
for i in range(bits-1):
    i += 1
    d1 = 3*i+1
    d2 = 3*i+2
    s = 3*i
    cOut = 3*i+3

    if bit1[-(i+1)] == "1":
        circuit.x(qreg_q[d1])
    if bit2[-(i+1)] == "1":
        circuit.x(qreg_q[d2])

    circuit.ccx(qreg_q[d1], qreg_q[d2], qreg_q[cOut])
    circuit.cx(qreg_q[d1], qreg_q[d2])
    circuit.ccx(qreg_q[d2], qreg_q[s], qreg_q[cOut])
    circuit.cx(qreg_q[d2], qreg_q[s])
    circuit.cx(qreg_q[d1], qreg_q[d2])
    circuit.measure(qreg_q[3*i], creg_c[i])

circuit.measure(qreg_q[3*bits], creg_c[bits])
# print(circuit)

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
plot_histogram(counts)
matplotlib.pyplot.show()