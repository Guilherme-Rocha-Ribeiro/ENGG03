# Referencias: https://www.youtube.com/watch?v=WIM538MAyNA, https://www.youtube.com/watch?v=WM3GXyHGGUQ
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Function
def func(x):
    return 150 + 30*np.sin((np.pi * x)/3)


# Methods
def trapezoid_rule(func, lower_bound, upper_bound, steps):
    x = np.linspace(lower_bound, upper_bound, steps+1)
    y = func(x)
    dx = (upper_bound - lower_bound) / steps
    
    trap_area = (dx/2) * (y[0] + 2*sum(y[1:-1]) + y[-1])
    return trap_area

def simpsons_1_3(func, lower_bound, upper_bound, steps):
    if steps % 2 != 0:
        steps += 1 

    x = np.linspace(lower_bound, upper_bound, steps+1)
    y = func(x)
    
    dx = (upper_bound - lower_bound) / steps
    
    sum_odd_index = 0
    for i in range(1, steps, 2):
        sum_odd_index += y[i]

    sum_even_index = 0
    for i in range(2, steps, 2):
        sum_even_index += y[i]

    area = (dx/3) * (y[0] + 4*sum_odd_index + 2*sum_even_index + y[-1])
    return area

def simpsons_3_8(func, lower_bound, upper_bound, steps):
    x = np.linspace(lower_bound, upper_bound, steps+1)
    y = func(x)
    dx = (upper_bound - lower_bound) / steps

    area_sum = 0
    for i in range(1, steps):
        if i % 3 == 0:
            area_sum += 2 * y[i]
        else:
            area_sum += 3 * y[i]

    area = (3/8 * dx) * (y[0] + area_sum + y[-1])
    return area


def find_min_steps(func, method, lower_bound, upper_bound, tolerance=1e-5, max_steps=1e4):
    if method == simpsons_3_8:
        steps = 3
        prev_area = method(func, lower_bound, upper_bound, steps)
        while steps <= max_steps:
            steps += 3
            current_area = method(func, lower_bound, upper_bound, steps)
            
            if abs(current_area - prev_area) < tolerance:
                return steps
            
            prev_area = current_area
        return None
    else:
        steps = 2
        prev_area = method(func, lower_bound, upper_bound, steps)
        
        while steps <= max_steps:
            steps += 2
            current_area = method(func, lower_bound, upper_bound, steps)
            
            if abs(current_area - prev_area) < tolerance:
                return steps
            
            prev_area = current_area
        return None

if __name__ == '__main__':
    # Valores iniciais
    lower_bound = 0
    upper_bound = 3
    # min_steps_trapezoid = 100
    # min_steps_simpson13 = 100
    # min_steps_simpson38 = 99

    min_steps_trapezoid = find_min_steps(func, trapezoid_rule, lower_bound, upper_bound)
    area_trapezoid = trapezoid_rule(func, lower_bound, upper_bound, steps= min_steps_trapezoid)
    # print(min_steps_trapezoid)
    print(f"{area_trapezoid:.9f}")
    
    min_steps_simpson13 = find_min_steps(func, simpsons_1_3, lower_bound, upper_bound)
    area_simpson13 = simpsons_1_3(func, lower_bound, upper_bound, steps= min_steps_simpson13)
    # print(min_steps_simpson13)
    print(f"{area_simpson13:.9f}")

    min_steps_simpson38 = find_min_steps(func, simpsons_3_8, lower_bound, upper_bound)
    area_simpson38 = simpsons_3_8(func, lower_bound, upper_bound, steps= min_steps_simpson38)
    # print(min_steps_simpson38)
    print(f"{area_simpson38:.9f}") 

    # Cria a figura
    x = np.linspace(lower_bound, upper_bound, 400)
    y = func(x)

    fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5), sharex=True, sharey=True)
    fig2.suptitle("Comparação entre Métodos de Integração", fontsize=12)

    # --- Função para adicionar área à legenda ---
    def add_area_to_legend(ax, area, color, line_handle):
        from matplotlib.patches import Patch
        
        # Cria o patch para a legenda da área
        legend_patch = Patch(color=color, alpha=0.5,
                            label=rf'$\int_0^3 \left(150 + 30\sin\left(\frac{{\pi x}}{{3}}\right)\right) dx$')
        
        # <<< ALTERAÇÃO AQUI: A legenda agora inclui a linha e o patch >>>
        ax.legend(handles=[line_handle, legend_patch], fontsize=9, loc='upper right')

    # Define o rótulo da função uma vez
    label_funcao = r'$f(x) = 150 + 30\sin(\frac{\pi x}{3})$'

    # --- Plot do Trapézio ---
    ax = axes2[0]
    x_trap_points = np.linspace(lower_bound, upper_bound, min_steps_trapezoid + 1)
    y_trap_points = func(x_trap_points)
    # Adiciona um label à função e captura a linha ('line1,')
    line1, = ax.plot(x, y, color='black', linewidth=1, label=label_funcao)
    ax.fill_between(x_trap_points, y_trap_points, color='red', alpha=0.5)
    ax.set_title(f"Trapézio | n = {min_steps_trapezoid}\n Area = {area_trapezoid:.9f}", fontsize=12,)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("f(x)", fontsize=10)
    # Passa a linha capturada para a função da legenda
    add_area_to_legend(ax, area_trapezoid, 'red', line1) 
    ax.grid(True, linestyle='--', alpha=0.6)

    # --- Plot do Simpson 1/3 ---
    ax = axes2[1]
    x_s13_points = np.linspace(lower_bound, upper_bound, min_steps_simpson13 + 1)
    y_s13_points = func(x_s13_points)
    line2, = ax.plot(x, y, color='black', linewidth=1, label=label_funcao)
    ax.fill_between(x_s13_points, y_s13_points, color='green', alpha=0.5)
    ax.set_title(f"Simpson 1/3 | n = {min_steps_simpson13}\n Area = {area_simpson13:.9f}", fontsize=12)
    add_area_to_legend(ax, area_simpson13, 'green', line2)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("f(x)", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)

    # --- Plot do Simpson 3/8 ---
    ax = axes2[2]
    x_s38_points = np.linspace(lower_bound, upper_bound, min_steps_simpson38 + 1)
    y_s38_points = func(x_s38_points)
    line3, = ax.plot(x, y, color='black', linewidth=1, label=label_funcao)
    ax.fill_between(x_s38_points, y_s38_points, color='magenta', alpha=0.5)
    ax.set_title(f"Simpson 3/8 | n = {min_steps_simpson38}\n Area = {area_simpson38:.9f}", fontsize=12)
    ax.set_xlabel("x", fontsize=10)
    ax.set_ylabel("f(x)", fontsize=10)
    add_area_to_legend(ax, area_simpson38, 'magenta', line3)
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout(rect=[0, 0, 1, 0.92])
    plt.show()
    