def func(x: float) -> float:
  y = 2*x**2 - 8
  return float(y)


def secante(a: float, b: float, tolerance = 0.001, i = 100) -> float:
    """
    Args: dois pontos iniciais a e b, um valor de tolerância e o número máximo de iterações.
    
    Returns: a raiz da função ou None se não for encontrada.
    """
    for j in range(i):
        if func(a) == func(b):
           return -1
        meio = b - (func(b) * (b - a)/(func(b) - func(a)))
        if abs(func(meio)) <= tolerance:
              return meio
        else:
            a = b
            b = meio
    print(f"Raiz não encontrada após {i} iterações.")
    return None

if __name__ == '__main__':
   print(secante(0, 2.1))
