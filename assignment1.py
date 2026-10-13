import math
import pathlib

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    with open(path, "r") as file:
        arr_b = []
        arr_a = []
        for line in file:
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            arr_b.append(float(tokens[-1]))
            sign = 1.0
            row = []
            for token in tokens:
                if token == "=":
                    break
                elif token == "+":
                    sign = 1.0
                elif token == "-":
                    sign = -1.0
                else:
                    coeff_str = token[:-1]
                    coeff = float(coeff_str) if coeff_str else 1.0
                    row.append(sign * coeff)
            arr_a.append(row)

    return arr_a, arr_b

A, B = load_system(pathlib.Path("system.txt"))

print(f"{A=} {B=}")

# 2   3   -1
# 1   -1   4
# 3   1    2

# B = 5, -6, 7

def determinant(matrix: list[list[float]]) -> float:
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    matrix_copy = matrix.copy()
    matrix_copy.append(matrix_copy[0])
    matrix_copy.append(matrix_copy[1])
    sum_primary = matrix_copy[0][0] * matrix_copy[1][1] * matrix_copy[2][2] + matrix_copy[1][0] * matrix_copy[2][1] * matrix_copy[3][2] + matrix_copy[2][0] * matrix_copy[3][1] * matrix_copy[4][2]
    sum_secondary = matrix_copy[0][2] * matrix_copy[1][1] * matrix_copy[2][0] + matrix_copy[1][2] * matrix_copy[2][1] * matrix_copy[3][0] + matrix_copy[2][2] * matrix_copy[3][1] * matrix_copy[4][0]
    return sum_primary - sum_secondary

print(f"{determinant(A)=}")

def trace(matrix: list[list[float]]) -> float:
    return matrix[0][0] + matrix[1][1] + matrix[2][2]

print(f"{trace(A)=}")

def norm(vector: list[float]) -> float:
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)

print(f"{norm(B)=}")

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [[matrix[0][0], matrix[1][0], matrix[2][0]], [matrix[0][1], matrix[1][1], matrix[2][1]], [matrix[0][2], matrix[1][2], matrix[2][2]]]

print(f"{transpose(A)=}")

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [matrix[0][0]*vector[0] + matrix[0][1]*vector[1] + matrix[0][2]*vector[2],
           matrix[1][0]*vector[0] + matrix[1][1]*vector[1] + matrix[1][2]*vector[2],
           matrix[2][0]*vector[0] + matrix[2][1]*vector[1] + matrix[2][2]*vector[2]]

print(f"{multiply(A, B)=}")

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    matrix_a1 = [row.copy() for row in matrix]
    matrix_a2 = [row.copy() for row in matrix]
    matrix_a3 = [row.copy() for row in matrix]
    matrix_a1[0][0] = vector[0]
    matrix_a1[1][0] = vector[1]
    matrix_a1[2][0] = vector[2]
    matrix_a2[0][1] = vector[0]
    matrix_a2[1][1] = vector[1]
    matrix_a2[2][1] = vector[2]
    matrix_a3[0][2] = vector[0]
    matrix_a3[1][2] = vector[1]
    matrix_a3[2][2] = vector[2]
    return [determinant(matrix_a1)/determinant(matrix), determinant(matrix_a2)/determinant(matrix), determinant(matrix_a3)/determinant(matrix)]

print(f"{solve_cramer(A, B)=}")

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    matrix_elements = []
    for x in range(3):
        for y in range(3):
            if x != i and y != j:
                matrix_elements.append(matrix[x][y])
    new_matrix = [[0 for _ in range(2)] for _ in range(2)]
    k = 0
    for x in range(2):
        for y in range(2):
            new_matrix[x][y] = matrix_elements[k]
            k += 1
    return new_matrix

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    cof_matrix = [[0 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            cof_matrix[i][j] = pow(-1, i + j)*determinant(minor(matrix, i, j))
    return cof_matrix

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is singular (determinant is 0)")
    adj_times_vector = multiply(adjoint(matrix), vector)
    return [elem / det for elem in adj_times_vector]

print(f"minor: {minor(A, 1, 2)}")
print(f"cofactor: {cofactor(A)}")
print(f"adjoint: {adjoint(A)}")
print(f"{solve(A, B)=}")