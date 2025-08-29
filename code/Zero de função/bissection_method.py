# A função bissection(a , b) precisa receber um intervalo em que ocorre a mundança de sinal para poder encontrar uma unica raiz

def func(x: float) -> float:
  y = 5*x**3 - 12*x**2 + 7*x - 1
  return float(y)


def bissection(a: float, b: float, tolerance = 10**-4):
  if func(a) * func(b) > 0:
    x = func(a)
    y = func(b)
    return  "Não ocorre mudança de sinal entre a e b", [float(x), float(y)]
  else:
    while True:
      mid_pnt = (a+b)/2
      if abs(func(mid_pnt)) <= tolerance:
        return mid_pnt

      if func(mid_pnt) * func(a) < 0:
        b = mid_pnt
      else:
        a = mid_pnt
      mid_pnt = (a+b)/2
    return mid_pnt

if __name__ == '__main__':
  zero_funcao = bissection(0, 2)
  print(f'O zero da função é no ponto {zero_funcao:.4f}')


