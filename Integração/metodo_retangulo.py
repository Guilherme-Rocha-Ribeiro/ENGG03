# Left Riemann Sums 
# So precisa alterar a func(x) para a funcao desejada 
import numpy as np
import matplotlib.pyplot as plt

def func(x):
    return 4*np.square(x) + 2*x - 1

def func_derivada(x):
    return 8 * x + 2


def leftRiemannSums(lower_bound ,upper_bound, steps = 1000):
    x = np.linspace(lower_bound, upper_bound, 1000)
    y = func(x) 

    plt.plot(x, y, color = 'black', linewidth=2, label='f(x) = 4x² + 2x - 1') 

    dx = (upper_bound - lower_bound)/steps # rectangle_length 
    current_x = lower_bound
    sum_area = 0

    for i in range(steps):
        # Draw each rectangle
        height = func(current_x)
        rect = plt.Rectangle(
            (current_x, 0), # (x, y) do canto inferior esquerdo
            dx, # largura 
            height, # altura 
            alpha=0.3,        # Transparency
            edgecolor= 'cyan',  # Border color
            facecolor='blue'   # Fill color
        )
        plt.gca().add_patch(rect)

        # Implementation of the sum
        sum_area += dx * height
        current_x += dx
    
    plt.title(f'Soma de Riemann à Esquerda (n={steps})\nÁrea aproximada: {sum_area:.4f}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)

    plt.show()
    return sum_area

    
def MiddleRiemannSums(lower_bound ,upper_bound, steps = 1000):







if __name__ == '__main__':
    # plot variables 
    area = leftRiemannSums(lower_bound = 2, upper_bound = 6, steps = 1000)
    print(f"Área aproximada: {area}")





