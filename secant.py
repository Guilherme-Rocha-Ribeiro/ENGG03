# Secante toca a curva em dois pontos 

def func(x: float) -> float:
    return 2*x**2 - 8

def new_x(x0,x1):
    if func(x0) == func(x1):
        return -1
    x = x0 - func(x0) * (x1-x0) / (func(x1) - func(x0))
    return x

def secant(x0, x1, tolerance = 0.001):
    x2 = new_x(x0, x1)
    while func(x2) <= tolerance:
        x2 = new_x(x2, x1)
        
        print(f"x0=", x1)
        print(f"x1=", x0)
        print(f"x2=", x2)
    return x1, interacoes




if __name__ == '__main__':
    print(secant(-3, 2))