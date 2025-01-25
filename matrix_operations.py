def array(data):
    if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a list of lists.")
    row_lengths = {len(row) for row in data}
    if len(row_lengths) != 1:
        raise ValueError("All rows must have the same length.")
    return data

def add(matrix1, matrix2):
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("Matrices must have the same dimensions.")
    return [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

def multiply(matrix, scalar):
    return [[element * scalar for element in row] for row in matrix]

def matmul(matrix1, matrix2):
    if len(matrix1[0]) != len(matrix2):
        raise ValueError("Number of columns in matrix1 must equal number of rows in matrix2.")
    return [[sum(matrix1[i][k] * matrix2[k][j] for k in range(len(matrix2)))
             for j in range(len(matrix2[0]))] for i in range(len(matrix1))]

def det(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError("Matrix must be square.")

    if len(matrix) == 1:
        return matrix[0][0]

    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for col in range(len(matrix)):
        submatrix = [row[:col] + row[col + 1:] for row in matrix[1:]]
        determinant += ((-1) ** col) * matrix[0][col] * det(submatrix)
    return determinant

def adjugate(matrix):
    if len(matrix) != len(matrix[0]):
        raise ValueError("Matrix must be square.")

    size = len(matrix)
    cofactors = []

    for i in range(size):
        cofactor_row = []
        for j in range(size):
            submatrix = [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]
            cofactor = ((-1) ** (i + j)) * det(submatrix)
            cofactor_row.append(cofactor)
        cofactors.append(cofactor_row)

    return transpose(cofactors)

def matrix_rank(matrix):
    temp_matrix = [row[:] for row in matrix]
    rows = len(temp_matrix)
    cols = len(temp_matrix[0])
    rank = 0

    for i in range(rows):
        if temp_matrix[i][i] == 0:
            for j in range(i + 1, rows):
                if temp_matrix[j][i] != 0:
                    temp_matrix[i], temp_matrix[j] = temp_matrix[j], temp_matrix[i]
                    break
            else:
                continue

        for j in range(i + 1, rows):
            if temp_matrix[j][i] != 0:
                factor = temp_matrix[j][i]
                for k in range(cols):
                    temp_matrix[j][k] -= factor * temp_matrix[i][k] // temp_matrix[i][i]

        rank += 1

    return rank

def solve(coefficients, constants):
    augmented = [row + [constants[i]] for i, row in enumerate(coefficients)]

    num_rows = len(augmented)
    num_cols = len(augmented[0])

    for i in range(num_rows):
        if augmented[i][i] == 0:
            for j in range(i + 1, num_rows):
                if augmented[j][i] != 0:
                    augmented[i], augmented[j] = augmented[j], augmented[i]
                    break
            else:
                raise ValueError("Matrix is singular or system is inconsistent.")

        for j in range(i + 1, num_rows):
            if augmented[j][i] != 0:
                factor = augmented[j][i]
                pivot = augmented[i][i]
                for k in range(num_cols):
                    augmented[j][k] = pivot * augmented[j][k] - factor * augmented[i][k]

    solution = [0] * num_rows
    for i in range(num_rows - 1, -1, -1):
        sum_ax = sum(augmented[i][j] * solution[j] for j in range(i + 1, num_rows))
        solution[i] = (augmented[i][-1] - sum_ax) // augmented[i][i]

    return solution

def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]