import numpy as np
import matplotlib.pyplot as plt

# Valores iniciais
a = 0.6 
b = 0.2 
h1_0 = 2.0
h2_0 = 1.0
t_total = 20
dt = 0.5
steps = int(t_total / dt)

# Sistema de equações
def eq_system(h1, h2):
    dh1dt = -a * np.sqrt(h1) + b * (h2 - h1)
    dh2dt = a * np.sqrt(h1) - b * (h2 - h1)
    return dh1dt, dh2dt

# Euler
def euler_system(func, h1_0, h2_0, dt, steps):
    h1 = np.zeros(steps + 1)
    h2 = np.zeros(steps + 1)
    h1[0], h2[0] = h1_0, h2_0
    
    for i in range(steps):
        dh1, dh2 = func(h1[i], h2[i])
        h1[i+1] = h1[i] + dt * dh1
        h2[i+1] = h2[i] + dt * dh2
    
    return h1, h2

# Runge-kutta4 
def rk4_system(func, h1_0, h2_0, dt, steps):
    h1 = np.zeros(steps + 1)
    h2 = np.zeros(steps + 1)
    h1[0], h2[0] = h1_0, h2_0

    for i in range(steps):
        k1_h1, k1_h2 = func(h1[i], h2[i])
        k2_h1, k2_h2 = func(h1[i] + dt/2 * k1_h1, h2[i] + dt/2 * k1_h2)
        k3_h1, k3_h2 = func(h1[i] + dt/2 * k2_h1, h2[i] + dt/2 * k2_h2)
        k4_h1, k4_h2 = func(h1[i] + dt * k3_h1, h2[i] + dt * k3_h2)

        h1[i+1] = h1[i] + dt/6 * (k1_h1 + 2*k2_h1 + 2*k3_h1 + k4_h1)
        h2[i+1] = h2[i] + dt/6 * (k1_h2 + 2*k2_h2 + 2*k3_h2 + k4_h2)

    return h1, h2

# Função CORRIGIDA para encontrar o ponto de estabilização
def find_stabilization(time, h1, h2, eq_system, tolerance=1e-6, consecutive_steps=3):
    """
    Encontra o ponto de estabilização baseado nas derivadas dh/dt ≈ 0
    
    Args:
        time: array de tempos
        h1, h2: arrays de alturas
        eq_system: função que calcula as derivadas
        tolerance: tolerância para considerar derivada zero
        consecutive_steps: número de passos consecutivos estáveis requeridos
    
    Returns:
        Tupla (tempo, h1, h2) no ponto de estabilização
    """
    stable_steps = 0
    for i in range(len(time)):
        # Calcula as derivadas reais do sistema
        dh1dt, dh2dt = eq_system(h1[i], h2[i])
        
        if abs(dh1dt) < tolerance and abs(dh2dt) < tolerance:
            stable_steps += 1
            if stable_steps >= consecutive_steps:
                return time[i-consecutive_steps+1], h1[i-consecutive_steps+1], h2[i-consecutive_steps+1]
        else:
            stable_steps = 0
    
    return time[-1], h1[-1], h2[-1]  # Retorna o final se não encontrar estabilização

if __name__ == "__main__":
    h1_euler, h2_euler = euler_system(eq_system, h1_0, h2_0, dt, steps)
    h1_rk4, h2_rk4 = rk4_system(eq_system, h1_0, h2_0, dt, steps)

    time = np.linspace(0, t_total, steps + 1)
    
    # Encontrar pontos de estabilização CORRETAMENTE (passando eq_system)
    stab_time_euler, stab_h1_euler, stab_h2_euler = find_stabilization(time, h1_euler, h2_euler, eq_system)
    stab_time_rk4, stab_h1_rk4, stab_h2_rk4 = find_stabilization(time, h1_rk4, h2_rk4, eq_system)
    
    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(time, h1_euler, label="h1 (Euler)", linestyle='solid', color='cyan')
    plt.plot(time, h2_euler, label="h2 (Euler)", linestyle='solid', color='magenta')
    plt.plot(time, h1_rk4, label="h1 (RK4)", linestyle='--', color='black')
    plt.plot(time, h2_rk4, label="h2 (RK4)", linestyle='--', color='purple')

    # Marcar pontos de estabilização
    plt.scatter(stab_time_euler, stab_h1_euler, color='cyan', marker='o', s=100, 
               label=f'Estab. Euler (t={stab_time_euler:.1f}s)')
    plt.scatter(stab_time_euler, stab_h2_euler, color='magenta', marker='o', s=100)
    plt.scatter(stab_time_rk4, stab_h1_rk4, color='black', marker='x', s=100, 
               label=f'Estab. RK4 (t={stab_time_rk4:.1f}s)')
    plt.scatter(stab_time_rk4, stab_h2_rk4, color='purple', marker='x', s=100)

    plt.xlabel("Tempo (s)")
    plt.ylabel("Altura (m)")
    plt.title("Variação da altura X Tempo com pontos de estabilização (critério dh/dt ≈ 0)")
    plt.legend()
    plt.grid()
    plt.show()


    
    # Print final values

    print(f"Altura final por Euler tank1: {h1_euler[-1]:.8f} m")
    print(f"Altura final por Euler tank2: {h2_euler[-1]:.8f} m")

    print(f"Altura final por rk4 tank1: {h1_rk4[-1]:.8f} m")
    print(f"Altura final por rk4 tank2: {h2_rk4[-1]:.8f} m")

    # print(h1_euler[0:-1:4])
    # print(h2_euler[0:-1:4])

    # print(h1_rk4[0:-1:4])
    # print(h2_rk4[0:-1:4])