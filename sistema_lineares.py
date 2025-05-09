import numpy as np
from typing import Tuple

# Considerando Ax=b -> A(inversa) * Ax = A(inversa) * B
# x = A(inversa) * B
def solucao_geral(matriz_coeficientes: list[list[float]], matriz2: list[list[float]]) -> list[list[float]]:
    A_inversa = np.linalg.inv(matriz_coeficientes)
    solucao = np.dot(A_inversa, matriz2) # np.dot() é o metodo de multiplicacao de matrizes 
    return solucao
# solucao_geral([[2, 3], [1, -1]],[[4], [1]])



# Solução usando biblioteca numpy.linalg.solve()
def linalg_solver(matriz_coeficientes: list[list[float]], matriz2: list[list[float]]) -> list[list[float]]:
    return np.linalg.solve(matriz_coeficientes, matriz2)




if __name__ == '__main__':
    # Testando a função com um exemplo
    matriz_coeficientes = [[3, 1, 2], 
                           [2, -1, 1], 
                           [1, 4, -1]]
    
    matriz_independetes = [[18], [8], [10]]

    A = np.array([[1,1,1],
                  [2,-1,-3],
                  [-5,-3,1]])
    B = np.array([[3],[4],[10]])
    print(f"Metodo solucao geral " , '\n', solucao_geral(A, B))



    resultado = solucao_geral(matriz_coeficientes, matriz_independetes)
    print("Resultado da solução geral:\n", resultado)
    resultado_numpy = linalg_solver(matriz_coeficientes, matriz_independetes)
    print("Resultado usando numpy:\n", resultado_numpy)