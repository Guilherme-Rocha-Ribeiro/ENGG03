import numpy as np
import matplotlib.pyplot as plt

# Euler method
def euler(func, x0, y0, dx, numb_steps):
    xs = [x0]
    ys = [y0]

    x, y = x0, y0
    for _ in range(numb_steps):
        y += dx * func(x, y)
        x += dx
        xs.append(x)
        ys.append(y)

    return xs, ys



if __name__ == '__main__':
    # Valores iniciais
    def func(x, y):
        return -2 * x + 3 * y
    
    def solucao_model(x):
        return (2/3) * x + (2/9) + (7/9) * np.exp(3 * x)

    x0 =  0
    y0 = 1
    dx = 0.1
    numb_steps = 10
    

    x_plot = np.linspace(0, 1, 400)
    y_correta = solucao_model(x_plot)
    xs, ys = euler(func, x0, y0, dx, numb_steps)
    xs1, ys1 = euler(func, x0, y0, dx/1000, 10000)
    xs2, ys2 = euler(func, x0, y0, dx/10, 100)

    plt.plot(x_plot, y_correta, label="Solução Analítica Correta", color='black', linestyle='solid', linewidth=2.5)
    plt.plot(xs, ys, label="Euler dx = 0.1 e steps = 10", linewidth = 2.5, linestyle='--')
    plt.plot(xs1, ys1, label="Euler dx = 0.1/100 e steps = 1000", linewidth = 2.5, linestyle = 'dashed')
    plt.plot(xs2, ys2, label="Euler dx = 0.1/10 e steps = 100", linewidth = 2.5, linestyle=':')
    plt.title("Comparação: Método de Euler vs. Solução Analítica")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()

