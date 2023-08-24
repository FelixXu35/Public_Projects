import numpy as np


def integer_QAOA_transformation(integers: list):
    """
    return the transformation matrix
    the input should be a list of integer, where each integer indicates the upper limit of each stock
    the way of dividing upper limits are from
    Quantum Portfolio Optimization: Binary encoding of discrete variables for QAOA with hard constraint
    the way of building transformation matrix is from
    Integer Programming from Quantum Annealing and Open Quantum Systems
    """
    n_qubits = np.shape(integers)[0] # the dimension of the Q-matrix before transformation
    matrix = np.array([[] for _ in integers], dtype=int)  # the transformation matrix
    for i, R in enumerate(integers):
        n = int(np.floor(np.log2(R + 1)))
        
        binary_number = np.binary_repr(R - 2**n + 1, width=n)
        l = [1 for _ in range(n)]
        for index, number in enumerate(binary_number):
            if number == "1":
                l[index] += 1
        single_matrix = np.zeros((n_qubits, sum(l)), dtype=int)
        position = 0
        for power, repetition in enumerate(l):
            for _ in range(repetition):
                single_matrix[i][position] = int(2**power)
                position += 1
        print(n, l, binary_number, single_matrix)
        matrix = np.concatenate((matrix, single_matrix), axis=1)
    return matrix
