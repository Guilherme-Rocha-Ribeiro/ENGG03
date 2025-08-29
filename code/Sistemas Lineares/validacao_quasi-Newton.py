import numpy as np
from scipy.optimize import root

# Defina a função que representa o sistema de equações
def equations(vars):
    x, y = vars
    # Certifique-se de que y + 1 > 0 para evitar erros no logaritmo
    if y <= -1:
        # Retornar valores grandes para penalizar soluções inválidas
        # Isso pode ajudar o solver a se afastar de regiões ruins,
        # embora o ideal seja que o solver respeite limites se possível
        # ou que a estimativa inicial seja boa.
        return [np.inf, np.inf]

    eq1 = x * y + y**2 - 10
    eq2 = x**2 - np.log(y + 1) - 2
    return [eq1, eq2]

# Estimativa inicial para as variáveis [x, y]
# A escolha da estimativa inicial pode ser crucial para a convergência
# e para qual solução é encontrada (se houver múltiplas).
# Vamos tentar algumas estimativas:
initial_guesses = [
    [2.0, 2.0],  # Estimativa 1
    [1.0, 3.0],  # Estimativa 2
    [-3.0, 2.0], # Estimativa 3 (pode levar a outra solução)
    [2.0, 0.5]   # Estimativa 4
]

# Métodos que podemos tentar (alguns são Quasi-Newton ou relacionados)
# 'hybr' (padrão, usa uma modificação do método de Powell)
# 'lm' (Levenberg-Marquardt, bom para problemas de mínimos quadrados, mas pode ser usado aqui)
# 'broyden1' (Quasi-Newton)
# 'broyden2' (Quasi-Newton)
# 'anderson' (Quasi-Newton)
# 'diagbroyden' (Quasi-Newton)
methods_to_try = ['hybr', 'broyden1', 'broyden2', 'anderson']

for i, x0 in enumerate(initial_guesses):
    print(f"--- Testando com estimativa inicial: {x0} ---")
    for method_name in methods_to_try:
        print(f"  Usando método: {method_name}")
        try:
            # Chama a função root
            # 'args' não é necessário aqui, pois 'equations' já pega 'vars' diretamente
            solution = root(equations, x0, method=method_name)

            if solution.success:
                print(f"    Solução encontrada para x0={x0}, método={method_name}:")
                print(f"      x = {solution.x[0]:.6f}")
                print(f"      y = {solution.x[1]:.6f}")
                # Verificando os valores das equações na solução
                final_values = equations(solution.x)
                print(f"      f1(x,y) = {final_values[0]:.2e}")
                print(f"      f2(x,y) = {final_values[1]:.2e}")
            else:
                print(f"    A solução não convergiu para x0={x0}, método={method_name}.")
                print(f"      Mensagem: {solution.message}")
        except Exception as e:
            print(f"    Ocorreu um erro durante a solução com x0={x0}, método={method_name}: {e}")
    print("-" * 40)