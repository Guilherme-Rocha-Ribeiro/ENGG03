# Referencias https://www.youtube.com/watch?v=WqREhIYPfkQ -> Lagrange Polynomial Interpolation Introduction | Numerical Methods
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

def lagrange_interpolation(x_points, y_points):
    """Retorna o polinômio de Lagrange como um objeto Polynomial"""
    n = len(x_points)
    poly = Polynomial([0.0])
    
    for i in range(n):
        term = Polynomial([y_points[i]])
        for j in range(n):
            if i != j:
                p = Polynomial([-x_points[j], 1.0]) / (x_points[i] - x_points[j])
                term *= p
        poly += term
    
    return poly

def trapezoid_rule(func, lower_bound, upper_bound, steps):
    """Sua função original do trapézio"""
    x = np.linspace(lower_bound, upper_bound, steps+1)
    y = func(x)
    dx = (upper_bound - lower_bound) / steps
    return (dx/2) * (y[0] + 2*sum(y[1:-1]) + y[-1]), x, y  # Retorna também os pontos para plotagem

def simpsons_1_3(func, lower_bound, upper_bound, steps):
    """Sua função original de Simpson"""
    if steps % 2 != 0:
        steps += 1 

    x = np.linspace(lower_bound, upper_bound, steps+1)
    y = func(x)
    dx = (upper_bound - lower_bound) / steps
    
    sum_odd_index = sum(y[i] for i in range(1, steps, 2))
    sum_even_index = sum(y[i] for i in range(2, steps, 2))

    return (dx/3) * (y[0] + 4*sum_odd_index + 2*sum_even_index + y[-1]), x, y  # Retorna também os pontos

if __name__ == "__main__":
    # Dados experimentais
    t = np.array([0, 2, 4, 6])
    P = np.array([0, 15, 23, 30])

    # Obter o polinômio
    P_poly = lagrange_interpolation(t, P)
    P_t = P_poly
    
    # Formatar a string do polinômio
    coeffs = P_poly.coef
    poly_str = "P(t) = " + " + ".join([f"{c:.4f}t^{i}" if i > 0 else f"{c:.4f}" 
                                      for i, c in enumerate(coeffs)])
    
    # Calcular P(4.5)
    P_45 = P_t(4.5)
    
    
    n = 250  
    area_trap, x_trap, y_trap = trapezoid_rule(P_t, 0, 6, n)
    
    # Plotagem
    t_plot = np.linspace(0, 6, 100)
    P_plot = P_t(t_plot)
    
    # Curva principal
    plt.plot(t_plot, P_plot, 'b-', label='Polinômio interpolador')
    plt.scatter(t, P, c='red', label='Dados experimentais', zorder=5)
    
    plt.scatter([4.5], [P_45], c='green', label=f'P(4.5) = {P_45:.2f} W', zorder=5)
    
    # Área do trapézio
    for i in range(n):
        plt.fill_between([x_trap[i], x_trap[i+1]], [0, 0], [y_trap[i], y_trap[i+1]],
                        color='orange', alpha=0.3, label=r'$\int_0^6 P(t) dt$' if i == 0 else "")
    
    # Configurações do gráfico
    plt.title(f'Interpolação de Lagrange\n{poly_str}\n'
             r'$\int_0^6 P(t) dt$ = ' + f'{area_trap:.8f} J')
    plt.xlabel('Tempo / min')
    plt.ylabel('Potência / W')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Resultados numéricos
    print("Polinômio interpolador:")
    print(poly_str + "\n")
    print(f"P(4.5) = {P_45:.4f}")
    print(f"Energia total fornecida:")
    print(f"Método do Trapézio (n={n}): {area_trap:.4f} J")