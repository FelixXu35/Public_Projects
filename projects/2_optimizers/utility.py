import numpy as np

def symmetric_matrix_generator(dim: int) -> np.array:
    """
    Generate a random symmetric matrix with a give dimension.
    args:
        dim: the number of dimension
    return:
        mat: a symmetric matrix
    """
    mat = np.random.rand(dim**2)
    mat = (mat - 0.5) * 2
    mat = mat.reshape(dim, dim)
    mat = np.triu(mat)
    mat += mat.T - np.diag(mat.diagonal())

    return mat

from qiskit.quantum_info import SparsePauliOp

def Q_to_paulis(Q):
    n_qubits = np.shape(Q)[0]
    offset = np.triu(Q, 0).sum() / 2
    pauli_terms = []
    coeffs = []

    coeffs = -np.sum(Q, axis=1) / 2

    for i in range(n_qubits):
        pauli = ['I' for i in range(n_qubits)]
        pauli[i] = 'Z'
        pauli_terms.append(''.join(pauli))

    for i in range(n_qubits - 1):
        for j in range(i + 1, n_qubits):
            pauli = ['I' for i in range(n_qubits)]
            pauli[i] = 'Z'
            pauli[j] = 'Z'
            pauli_terms.append(''.join(pauli))

            coeff = Q[i][j] / 2
            coeffs = np.concatenate((coeffs, coeff), axis=None)

    return SparsePauliOp(pauli_terms, coeffs=coeffs), offset