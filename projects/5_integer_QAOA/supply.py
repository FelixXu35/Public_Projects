from typing import List, Any

import numpy as np
import tensorcircuit as tc

matrix = Any


def integer_QAOA_transformation(
    Q: matrix, integers: list, budget: int | None = None, penalty: float = 1.
):
    """
    return the transformation matrix
    the input should be a list of integer, where each integer indicates the upper limit of each stock
    the way of dividing upper limits are from
    Quantum Portfolio Optimization: Binary encoding of discrete variables for QAOA with hard constraint
    the way of building transformation matrix is from
    Integer Programming from Quantum Annealing and Open Quantum Systems
    """
    n_qubits = np.shape(integers)[
        0
    ]  # the dimension of the Q-matrix before transformation
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
        matrix = np.concatenate((matrix, single_matrix), axis=1)
    diag_element = np.sum(matrix, axis=0)
    q = np.dot(matrix.T, np.dot(Q, matrix))
    if budget is not None:
        N = np.outer(diag_element, diag_element)
        eta = np.diag(diag_element)
        q += (N - 2 * eta * budget) * penalty

    return q, matrix


def print_result_cost(
    c: tc.Circuit, Q: List[list], wrap: bool = False, reverse: bool = False
) -> None:
    """
    Print the results and costs of a given quantum circuit.
    Specificly designed for the variational circuit.
    The default order is from the highest probability to the lowest one.

    :param c: The quantum circuit to print the results and probabilities.
    :param Q: The n-by-n square and symmetric Q-matrix representing the QUBO problem.
    :param wrap (optional): A flag indicating whether to wrap the output. Default is False.
    :param reverse (optional): A flag indicating whether to reverse the order of the output. Default is False.
    """
    cost_dict = {}
    states = []
    n_qubits = c._nqubits
    for i in range(2**n_qubits):
        a = f"{bin(i)[2:]:0>{n_qubits}}"
        states.append(a)
        # Generate all possible binary states for the given number of qubits
    for selection in states:
        x = np.array([int(bit) for bit in selection])
        cost_dict[selection] = np.dot(x, np.dot(Q, x))
    cost_sorted = dict(sorted(cost_dict.items(), key=lambda item: item[1]))
    if reverse == True:
        cost_sorted = dict(
            sorted(cost_dict.items(), key=lambda item: item[1], reverse=True)
        )
    num = 0
    print("\n-------------------------------------")
    print("    selection\t  |\t  cost")
    print("-------------------------------------")
    for k, v in cost_sorted.items():
        print("%10s\t  |\t%.4f" % (k, v))
        num += 1
        if (num >= 8) & (wrap == True):
            break
    print("-------------------------------------")

    def print_result_prob(c, wrap=False, reverse=False):
        states = []
        n_qubits = c._nqubits
        for i in range(2**n_qubits):
            a = f"{bin(i)[2:]:0>{n_qubits}}"
            states.append(a)
            # Generate all possible binary states for the given number of qubits

        probs = K.numpy(c.probability()).round(decimals=4)
        # Calculate the probabilities of each state using the circuit's probability method

        sorted_indices = np.argsort(probs)[::-1]
        if reverse == True:
            sorted_indices = sorted_indices[::-1]
        state_sorted = np.array(states)[sorted_indices]
        prob_sorted = np.array(probs)[sorted_indices]
        # Sort the states and probabilities in descending order based on the probabilities

        print("\n-------------------------------------")
        print("    selection\t  |\tprobability")
        print("-------------------------------------")
        if wrap == False:
            for i in range(len(states)):
                print("%10s\t  |\t  %.4f" % (state_sorted[i], prob_sorted[i]))
                # Print the sorted states and their corresponding probabilities
        elif wrap == True:
            for i in range(4):
                print("%10s\t  |\t  %.4f" % (state_sorted[i], prob_sorted[i]))
            print("               ... ...")
            for i in range(-5, -1):
                print("%10s\t  |\t  %.4f" % (state_sorted[i], prob_sorted[i]))
        print("-------------------------------------")


def all_quantum_states(n_qubits, budget=None, vec=False) -> list:
    states = []
    for i in range(2**n_qubits):
        a = f"{bin(i)[2:]:0>{n_qubits}}"
        n_ones = 0
        mark = True
        if isinstance(budget, int):
            for j in a:
                if j == "1":
                    n_ones += 1
            if n_ones >= budget:
                mark = False
        if mark is True:
            if vec == False:
                states.append(a)
            if vec == True:
                vector = [0 for i in range(n_qubits)]
                for i, j in enumerate(a):
                    if j == "1":
                        vector[i] = 1
                states.append(vector)
    return states


def print_Q_cost(Q: List[list], wrap: bool = False, reverse: bool = False) -> None:
    n_stocks = len(Q)
    states = []
    for i in range(2**n_stocks):
        a = f"{bin(i)[2:]:0>{n_stocks}}"
        n_ones = 0
        for j in a:
            if j == "1":
                n_ones += 1
        states.append(a)

    cost_dict = {}
    for selection in states:
        x = np.array([int(bit) for bit in selection])
        cost_dict[selection] = np.dot(x, np.dot(Q, x))
    cost_sorted = dict(sorted(cost_dict.items(), key=lambda item: item[1]))
    if reverse == True:
        cost_sorted = dict(
            sorted(cost_dict.items(), key=lambda item: item[1], reverse=True)
        )
    num = 0
    print("\n-------------------------------------")
    print("    selection\t  |\t  cost")
    print("-------------------------------------")
    for k, v in cost_sorted.items():
        print("%10s\t  |\t%.4f" % (k, v))
        num += 1
        if (num >= 8) & (wrap == True):
            break
    print("-------------------------------------")

def print_result_prob(c: tc.Circuit, wrap: bool = False, reverse: bool = False) -> None:
    """
    Print the results and probabilities of a given quantum circuit.
    The default order is from the highest probability to the lowest one

    :param c: The quantum circuit to print the results and probabilities.
    :param wrap (optional): A flag indicating whether to wrap the output. Default is False.
    :param reverse (optional): A flag indicating whether to reverse the order of the output. Default is False.
    """
    """try:
        K
    except NameError:
        print("select a backend and assign it to K.")"""

    states = []
    n_qubits = c._nqubits
    for i in range(2**n_qubits):
        a = f"{bin(i)[2:]:0>{n_qubits}}"
        states.append(a)
        # Generate all possible binary states for the given number of qubits

    probs = c.probability().numpy().round(decimals=4)
    # Calculate the probabilities of each state using the circuit's probability method

    sorted_indices = np.argsort(probs)[::-1]
    if reverse == True:
        sorted_indices = sorted_indices[::-1]
    state_sorted = np.array(states)[sorted_indices]
    prob_sorted = np.array(probs)[sorted_indices]
    # Sort the states and probabilities in descending order based on the probabilities

    print("\n-------------------------------------")
    print("    selection\t  |\tprobability")
    print("-------------------------------------")
    if wrap == False:
        for i in range(len(states)):
            print("%10s\t  |\t  %.4f" % (state_sorted[i], prob_sorted[i]))
            # Print the sorted states and their corresponding probabilities
    elif wrap == True:
        for i in range(4):
            print("%10s\t  |\t  %.4f" % (state_sorted[i], prob_sorted[i]))
        print("               ... ...")
        for i in range(-4, -1):
            print("%10s\t  |\t  %.4f" % (state_sorted[i], prob_sorted[i]))
    print("-------------------------------------")