# Referencias: https://www.youtube.com/watch?v=99ABkygm2Xg&list=PLDea8VeK4MUTOBXLpvx_WKtVrMkojEh52&index=45 , https://www.youtube.com/watch?v=gHL48ePY7lk
# 
def func(x: float) -> float:
    y = 5*x**3 - 12*x**2 + 7*x - 1
    return float(y)

def func_derivada(x: float) -> float:
    y = 15*x**2 - 24*x + 7
    return float(y)

def metodo_newton_raphson(guess: float, iteracoes: int = 100, tolerance = 0.001) -> float:
    
    x = guess
    for i in range(iteracoes):
        fx = func(x)
        dfx = func_derivada(x)

        # Verifica se a |f(x)| já é proximo de zero
        if abs(fx) <= tolerance:
            print(f"Raiz encontrada: {x:.4f} em {i} iterações")
            return x

        # Verifica se a derivada é zero
        if dfx == 0:
            raise ValueError("Derivada(x) = zero encontrada")
            break

        x_novo = x - fx / dfx

        if abs(x_novo - x) < tolerance:
            print(f"Convergência alcançada após {i+1} iterações.")
            return x_novo
        
        x = x_novo

    print(f"Raiz não encontrada após {iteracoes} iterações.")
    return None

if __name__ == '__main__':
    raiz = metodo_newton_raphson(1.4)
    print(f"A raiz aproximada é: {raiz:.4f}")



