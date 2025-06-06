import numpy as np
import matplotlib.pyplot as plt

# Function
def func(x):
    return 150 + 30*np.sin((np.pi * x)/3)

# Initialize the plot once
plt.figure(figsize=(10, 6))
plt.title("Trapezoidal Rule Convergence")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)

# Plot the exact curve
x_exact = np.linspace(0, 3, 1000)
y_exact = func(x_exact)
plt.plot(x_exact, y_exact, 'k-', linewidth=2, label='f(x) = 150 + 30 sin(πx/3)')

def trapezoid_rule(lower_bound, upper_bound, steps):
    x = np.linspace(lower_bound, upper_bound, steps+1)
    y = func(x)
    
    # Clear previous trapezoids
    for artist in plt.gca().collections[1:]:  # Keep the original curve
        artist.remove()
    
    # Plot new trapezoids
    for i in range(steps):
        x_trap = [x[i], x[i], x[i+1], x[i+1]]
        y_trap = [0, y[i], y[i+1], 0]
        plt.fill_between(x_trap, y_trap, color='skyblue', alpha=0.5, edgecolor='blue')
    
    dx = (upper_bound - lower_bound) / steps
    trap_area = (dx/2) * (y[0] + (2*sum(y[1:steps])) + y[steps])
    
    plt.title(f"Trapezoidal Rule (Steps: {steps}, Area: {trap_area:.6f})")
    plt.draw()
    plt.pause(0.5)  # Pause to visualize
    
    return trap_area

def find_min_steps(lower_bound, upper_bound, tolerance=1e-2, max_steps=1000):
    steps = 1
    prev_area = trapezoid_rule(lower_bound, upper_bound, steps)
    
    while steps <= max_steps:
        steps *= 2
        current_area = trapezoid_rule(lower_bound, upper_bound, steps)
        
        if abs(current_area - prev_area) < tolerance:
            plt.title(f"Converged at {steps} steps (Area: {current_area:.6f})")
            plt.show()
            return steps
        
        prev_area = current_area
    
    plt.title(f"Max steps reached ({max_steps}) without convergence")
    plt.show()
    return None

if __name__ == '__main__':
    find_min_steps(0, 3)