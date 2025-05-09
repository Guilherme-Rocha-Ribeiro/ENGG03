import numpy as np
from scipy.optimize import root


def sistema_funcoes(vars: np.ndarray) -> np.ndarray:
    """
    Calcula o valor das equações do sistema para um dado vetor de variáveis.
    
    Args:
        vars: Vetor de variáveis [x, y]
    
    Returns:
        Vetor com os valores das equações [eq1, eq2]
    """

    # eq1(x,y) = x*y + y^2 - 10
    # eq2(x,y) = x^2 - ln(y + 1) - 2
    x, y = vars
    if y <= -1: #  para evitar ln(y + 1) < 0
        return [np.inf, np.inf]

    eq1 = x * y + y**2 - 10
    eq2 = x**2 - np.log(y + 1) - 2
    return np.array([eq1, eq2])

# Define o vetor de derivadas parciais (Jacobiano)
def jacobiano(vars: np.ndarray) -> np.ndarray:
    """
    Cria a matriz de derivadas parciais (Jacobiano) do sistema de equações.

    Args:
        vars: Vetor de variáveis [x, y]
    
    Returns:
        matriz das derivadas parciais
    
    """
    x, y = vars
    if y <= -1:
        print(f"Aviso: Tentativa de calcular Jacobiana para y={y} <= -1")
        return np.array([[np.nan, np.nan], [np.nan, np.nan]])

    # Derivadas parciais
    eq1dx = y
    eq1dy = x + 2 * y
    eq2dx = 2 * x
    eq2dy = - 1 / (y + 1)

    return np.array([[eq1dx, eq1dy], 
                     [eq2dx, eq2dy]])

def metodo_newton_sistemas(guess_inicial_vetor: list[float], iteracoes=100, tolerance=10**-4) -> np.ndarray:
    X = np.array(guess_inicial_vetor, dtype=float)
    for i in range(iteracoes):
        F_X = sistema_funcoes(X)
        J_X = jacobiano(X)

        # Verifica se a norma de F(X) já é próxima de zero
        if np.linalg.norm(F_X) <= tolerance:
            print(f"Solução encontrada: {X} em {i} iterações")
            return X


        # Verifica se a Jacobiana é singular (determinante próximo de zero)
        
        if abs(np.linalg.det(J_X)) <= tolerance: 
            raise ValueError("Matriz Jacobiana singular encontrada")

        # Resolve o sistema linear J_X * delta_X = -F_X // J*Δx = -F
        delta_X = np.linalg.solve(J_X, -F_X)
        X_novo = X + delta_X

        if np.linalg.norm(X_novo - X) < tolerance:
            print(f"Convergência alcançada após {i+1} iterações.")
            return X_novo
        
        X = X_novo

    print(f"Solução não encontrada após {iteracoes} iterações.")
    return None


if __name__ == '__main__':
    guess_inicial = [1.0, 2.0]  # Estimativa inicial
    raiz = metodo_newton_sistemas(guess_inicial)
    raiz_scipy = root(sistema_funcoes, guess_inicial, jac=jacobiano, method='hybr')
    
    if raiz is not None and raiz_scipy.success:
    
        print("\nComparação das soluções:")
        print(f"Solução Implementação: {raiz}")
        print(f"Solução do SciPy:      {raiz_scipy.x}")

"""
Aluno: Guilherme Rocha Ribeiro
Referencias para o codigo: https://wwwp.fc.unesp.br/~adriana/Numerico/SNLinear.pdf , https://sistemas.eel.usp.br/docentes/arquivos/519033/LOM3026/Metodos_numericos_calculo_sistemas_equacoes_nao_lineares.pdf
"""
