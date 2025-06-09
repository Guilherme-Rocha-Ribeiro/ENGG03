import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

# Dados experimentais
t = np.array([0, 2, 4, 6])  # minutos
P = np.array([0, 15, 23, 30])  # watts

# Obter o polinômio usando scipy
poly = lagrange(t, P)

# Função para avaliação
def P_t(t):
    return poly(t)

# Coeficientes do polinômio
coeffs = poly.coef[::-1]  # Inverte a ordem para formato convencional

# Exibir a função polinomial
print("Polinômio interpolador (scipy):")
print(f"P(t) = {coeffs[0]:.4f}", end="")
for i in range(1, len(coeffs)):
    print(f" + {coeffs[i]:.4f}t^{i}", end="")
print("\n")

# Verificação em t=4.5
P_45 = P_t(4.5)
print(f"P(4.5) = {P_45:.2f} W")

# Comparação com os pontos conhecidos
print("\nVerificação nos pontos experimentais:")
for ti, Pi in zip(t, P):
    print(f"P({ti}) = {P_t(ti):.1f} W (esperado: {Pi} W)")

# Plotagem
t_plot = np.linspace(0, 6, 100)
P_plot = P_t(t_plot)

plt.figure(figsize=(10, 6))
plt.scatter(t, P, color='red', label='Dados experimentais', zorder=5)
plt.plot(t_plot, P_plot, label='Polinômio interpolador (scipy)')
plt.scatter([4.5], [P_45], color='green', label=f'P(4.5) = {P_45:.2f} W', zorder=5)
plt.title('Interpolação de Lagrange com Scipy')
plt.xlabel('Tempo (min)')
plt.ylabel('Potência (W)')
plt.grid(True)
plt.legend()
plt.show()