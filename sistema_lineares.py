import numpy as np
from typing import Tuple

A = np.array([[1,1,1],[2,-1,-3],[-5,-3,1]])
B = np.array([[3],[4],[10]])


# Considerando Ax=b -> A(inversa) * Ax = A(inversa) * B
# x = A(inversa) * B
def solucao_geral(matriz_coeficientes: list[list[float]], matriz2: list[list[float]]) -> list[list[float]]:
    A_inversa = np.linalg.inv(matriz_coeficientes)
    solucao = np.dot(A_inversa, matriz2) # np.dot() é o metodo de multiplicacao de matrizes 
    return solucao
# solucao_geral([[2, 3], [1, -1]],[[4], [1]])
print(f"Metodo solucao geral " , '\n', solucao_geral(A, B))
print('\n')


# Solução usando biblioteca numpy.linalg.solve()
def linalg_solver(matriz_coeficientes: list[list[float]], matriz2: list[list[float]]) -> list[list[float]]:
    return np.linalg.solve(matriz_coeficientes, matriz2)

print(linalg_solver(A, B))


# def gauss_jordan(matriz_coeficientes: list[list[float]], matriz2: list[list[float]]) -> list[list[float]]:
    