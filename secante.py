# o Metodo da secante pega dois pontos iniciais a e b 
def func(x: float) -> float:
  y = 2*x**2 - 8
  return float(y)


def secante(a, b, tolerance = 0.001, i = 100):
    for j in range(i):
        if func(a) == func(b):
           return -1
        meio = b - (func(b) * (b - a)/(func(b) - func(a)))
        print(meio)
        if abs(func(meio)) <= tolerance:
              return meio
        else:
            a = b
            b = meio

if __name__ == '__main__':
   print(secante(0, 2.1))