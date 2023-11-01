A series of mini projects.

These projects are not going to be published anywhere.

# Table of Constents:

1. [Time evolution](./projects/1_evolution) ✅

2. [Behaviours of Different Optimizers](/projects/2_optimizers/random_state.py)

3. [Stock Data Converter](./projects/3_stocks_converter/converter.ipynb)

4. [Visualization of T1 error](/projects/4_T1_error/T1_error.ipynb)

5. [Integer QAOA](./projects/5_integer_QAOA/Integer_QAOA.ipynb) ✅

# Planed:

* Jaynes–Cummings model

* Calculating the ground state wavefunction of hydrogen.

# 1. Time evolution

## Problem

Using quantum circuits to simulate a quantum system is one of the original purposes of quantum computing. Please describe how to construct a quantum circuit to simulate a physical system evolution in Hamiltonian:

$$\hat{H}=\sum_{k=1}^{N-1}J_k(\sigma^x_k\sigma^x_{k+1}+\sigma^y_k\sigma^y_{k+1}), \quad J_k=\sqrt{k(N-k)}$$

For $t=\pi/2$, where the initial state is $\ket{\psi(t=0)}=\ket{10\cdots0}_N$

In this project, Qiskit will be used, and the results will be compared with analytical ones.

## Result

Trotter-Suzuki decomposition formula is used.

The time evolutions are shown below. (up: qiskit, down: Julia).

<img src="./assets/image-20230414232303710-1510988.png" alt="image-20230414232303710" width="400" height="300" /><img src="./assets/Screenshot 2023-04-14 at 23.34.34-1511699.png" alt="Screenshot 2023-04-14 at 23.34.34" width="400" height="300" />

The qiskit results used 50 layers. However, there is still slight distortion. If I increase the number of layers (like to 1000, which is not friendly to NISQ), two results will be closer to each other.

Please find the more details through the links: [↗️qiskit](./projects/1_evolution/qiskit_evolution.ipynb) and [↗️Julia](./projects/1_evolution/Julia_evolution.ipynb).

# 5. Integer QAOA

The binary encoding and amplitude encoding are respectively discussed.

## Amplitude encoding

The brute-force searching was firstly done with 0.1 accuracy. After doing QAOA, the expectation value of each qubit doesn't match the brute-force result. That means amplitude doesn't work.

## Binary encoding

With a transformation matrix $M$, a binary vector $X$ can be used to represent an integer vector $x$.

$$ MX = x $$

And then an integer QUBO problem can transformed into a binary QUBO problem as

$$ X(M^TQM)X $$

In my notebook, a ramdom QUBO problem is transformed and then solved using QAOA.
