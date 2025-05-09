# Referencias utilizadas: https://www.youtube.com/watch?v=PCkLz5-vo3U , https://www.youtube.com/watch?v=gAmMxdI0EKs
# Resolucao de sistemas lineares 
import numpy as np

def eliminacao_gauss(matriz_coeficientes: list[list], termos_independentes:list[list]) -> list: # lista solucao
    if matriz_coeficientes.shape[0] != matriz_coeficientes.shape[1]:
        print(f"Erro: A matriz A não é quadrada.")
        return 

    if termos_independentes.shape[1] > 1 or termos_independentes.shape[0] != matriz_coeficientes.shape[0]:
        print(f"Erro: A matriz B não é compatível com A.")
        return 
    
    # Declaração de variáveis
    n = len(termos_independentes)
    i = 0
    k = 0

    # Inicializando a matriz aumentada
    matriz_aumentada = np.concatenate((matriz_coeficientes, termos_independentes), axis=1, dtype=float)
    
    print(f"Matriz aumentada inicial:", end="\n")
    print(matriz_aumentada)

        
    # validar pivo != 0
    for i in range(n):
        if matriz_aumentada[i][i] == 0:
            valido = False
            for j in range(i + 1, n):
                if matriz_aumentada[j][i] != 0:
                    # metodo de acessar as linhas da matriz diretamente mat[[i, j]] precisa usar numpy
                    matriz_aumentada[[i, j]] = matriz_aumentada[[j, i]]
                    print(f"\nTroca linha {i} com linha {j}:")
                    print(f"{matriz_aumentada}", end="\n")
                    valido = True
                    break
            
            if not valido:
                print(f"Erro: A matriz é singular.")
                return
        # Elminando os elementos para gerar a matriz triangular superior
        for j in range(i+1, n):
            fator_escalar = matriz_aumentada[j, i] / matriz_aumentada[i, i]
            matriz_aumentada[j] -= fator_escalar * matriz_aumentada[i]
            print(f"\nEliminação na linha {j} usando linha {i}, pelo fator {fator_escalar:}:" )
            print(matriz_aumentada)

    # Encontrando a solução no vetor x
    x = np.zeros(n)
    for k in range(n-1, -1, -1):
        x[k] = matriz_aumentada[k, n]
        for j in range(k+1, n):
            x[k] -= matriz_aumentada[k][j] * x[j]
        x[k] /= matriz_aumentada[k, k]
        x[k] = round(x[k], 4) # precisao setada para cada valor da solucao 

    return x

def linalg_solver(matriz_coeficientes: list[list[float]], matriz2: list[list[float]]) -> list[list[float]]:
    return np.linalg.solve(matriz_coeficientes, matriz2)

if __name__ == '__main__':
    A = np.array([[0, 1, 2], [2, -1, 1], [1, 4, -1]])
    B = np.array([[18], [8], [10]])
    resultado = eliminacao_gauss(A, B)
    resutlado_numpy = linalg_solver(A, B)
    print("Solução pelo Método de Gauss:", resultado)
    print("\nSolução do numpy (verificação):", resutlado_numpy)
    
"""



"""
    
