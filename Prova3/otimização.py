# Importação das bibliotecas necessárias
import numpy as np # Para operações numéricas e criação de arrays (linspace)
import matplotlib.pyplot as plt # Para plotar gráficos

# ==============================================================================
#                              Variáveis de Entrada
# ==============================================================================

# Propriedades do Fluido (Biodiesel)
rho = 880           # kg/m³ (densidade do biodiesel)
mu = 3.52e-3        # Pa·s (viscosidade dinâmica)

# Parâmetros do Sistema de Bombeamento e Tubulação
Q = 0.00333         # m³/s (vazão volumétrica)
L = 50              # m (comprimento total da tubulação)
epsilon = 0.000045  # m (rugosidade absoluta do tubo)
g = 9.81            # m/s² (aceleração da gravidade)
eta = 0.7           # eficiência da bomba (adimensional)
H_estatica = 10     # m (altura estática que a bomba precisa vencer - diferença de nível, pressão)

# Parâmetros de Otimização e Custo
D_min = 0.03        # m (Diâmetro mínimo a ser considerado para otimização)
D_max = 0.1       # m (Diâmetro máximo a ser considerado para otimização)
num_pontos = 100  # Número de pontos discretos de diâmetro para avaliação
# Criação de um array com diâmetros uniformemente espaçados entre D_min e D_max
D_variavel = np.linspace(D_min, D_max, num_pontos)

# Função que define o custo do material da tubulação por metro em função do diâmetro
def custo_por_metro(D):
  # Exemplo: Custo por metro proporcional ao quadrado do diâmetro
  return 300 * D**2 # R$/m


energia_por_kWh = 0.70  # R$/kWh (Custo da energia elétrica por quilowatt-hora)

# ==============================================================================
#               Cálculos para cada Diâmetro e Armazenamento
# ==============================================================================

# Listas para armazenar os resultados de perda de carga, potência e custos para cada diâmetro avaliado
hf_list = []              # Lista para armazenar a perda de carga (m)
Potencia_list = []        # Lista para armazenar a potência hidráulica (W)
Custo_tubulacao_list = [] # Lista para armazenar o custo de aquisição da tubulação (R$)
Custo_energia_list = []   # Lista para armazenar o custo energético anual (R$)
Custo_total_list = []     # Lista para armazenar o custo total anual (R$)

# Loop que itera sobre cada diâmetro na faixa definida
for D in D_variavel:
  # 1. Área da seção transversal do tubo
  A = np.pi * D**2 / 4 # m²

  # 2. Velocidade média do fluido na tubulação
  v = Q / A # m/s

  # 3. Número de Reynolds para caracterizar o regime de escoamento
  Re = (rho * v * D) / mu # Adimensional

  # 4. Fator de atrito 'f' - determina a resistência ao escoamento
  # Utiliza a correlação de Swamee-Jain, válida para regime turbulento (Re > 4000)
  # Para simplificar, aplicamos a mesma fórmula, embora para Re <= 2100 (laminar),
  # f = 64/Re seria mais preciso. O range de diâmetros e vazão geralmente resulta em Re turbulento.
  # A condição 'if Re > 4000' original pode ser mantida se a intenção for rigorosa,
  # mas a Swamee-Jain é razoável para transição também. Mantendo a Swamee-Jain para todos Re > 0.
  # Evita divisão por zero caso D seja 0, embora D_variavel comece em D_min > 0.
  if Re > 0: # Garantir que Re é maior que zero para evitar log de zero ou negativo
      f = 0.25 / (np.log10(epsilon / (3.7 * D) + 5.74 / Re**0.9))**2
  else:
      # Caso Re seja zero (teórico, mas bom para robustez), o fator de atrito é indefinido
      # Neste contexto, como Q > 0 e D > 0, Re será sempre positivo.
      f = 0 # ou um valor apropriado para Re=0, embora não aplicável aqui.


  # 5. Perda de carga por atrito ao longo do comprimento da tubulação (Darcy-Weisbach)
  hf = f * L * v**2 / (D * 2 * g) # m
  hf_list.append(hf) # Armazena a perda de carga calculada

  # 6. Altura manométrica total que a bomba deve fornecer
  H = H_estatica + hf # m (Soma da altura estática e da perda de carga)

  # 7. Potência hidráulica necessária da bomba
  # Multiplicamos por rho, g, Q e H, e dividimos pela eficiência da bomba (eta)
  P = (rho * g * Q * H) / eta # W (Watts)
  Potencia_list.append(P) # Armazena a potência calculada

  # 8. Custo de aquisição da tubulação
  Custo_tubulacao = custo_por_metro(D) * L # R$ (Custo por metro vezes o comprimento total)
  Custo_tubulacao_list.append(Custo_tubulacao) # Armazena o custo da tubulação

  # 9. Custo energético anual da operação da bomba
  # Considera operação contínua (8760 horas por ano)
  # Divide a potência em W por 1000 para obter kW, multiplica pelas horas de operação e pelo custo por kWh
  E = (P / 1000) * 8760 * energia_por_kWh # R$/ano
  Custo_energia_list.append(E) # Armazena o custo energético

  # 10. Custo total anual
  # Soma do custo da tubulação (considerado como um investimento inicial anualizado implicitamente neste cálculo simplificado de "custo total anual")
  # e o custo energético anual.
  C_total = Custo_tubulacao + E # R$/ano
  Custo_total_list.append(C_total) # Armazena o custo total

# ==============================================================================
#                         Encontrar o Diâmetro Ótimo
# ==============================================================================

# Encontrar o índice do diâmetro que corresponde ao menor custo total na lista Custo_total_list
indice_otimo = np.argmin(Custo_total_list)

# Recuperar os valores correspondentes ao diâmetro ótimo usando o índice encontrado
D_otimo = D_variavel[indice_otimo]                       # Diâmetro ótimo
hf_otimo = hf_list[indice_otimo]                         # Perda de carga no diâmetro ótimo
Potencia_otima = Potencia_list[indice_otimo]             # Potência da bomba no diâmetro ótimo
Custo_tubulacao_otimo = Custo_tubulacao_list[indice_otimo] # Custo da tubulação no diâmetro ótimo
Custo_energia_otimo = Custo_energia_list[indice_otimo]     # Custo energético anual no diâmetro ótimo
Custo_total_otimo = Custo_total_list[indice_otimo]         # Custo total anual mínimo

# ==============================================================================
#                               Saídas e Resultados
# ==============================================================================

# Imprimir os resultados calculados para o diâmetro ótimo
print("===============================================")
print("            Resultados da Otimização")
print("===============================================")
print(f"Diâmetro ótimo: {D_otimo:.4f} m") # Formata para 4 casas decimais
print(f"Perda de carga correspondente: {hf_otimo:.4f} m") # Formata para 4 casas decimais
print(f"Potência da bomba: {Potencia_otima:.2f} W") # Formata para 2 casas decimais
print(f"Custo da tubulação: R$ {Custo_tubulacao_otimo:.2f}") # Formata para 2 casas decimais
print(f"Custo energético anual: R$ {Custo_energia_otimo:.2f}") # Formata para 2 casas decimais
print(f"Custo total anual mínimo: R$ {Custo_total_otimo:.2f}") # Formata para 2 casas decimais
print("===============================================")

# ==============================================================================
#                                    Gráfico
# ==============================================================================

# Plotar o gráfico do Custo Total Anual em função do Diâmetro da Tubulação
plt.figure(figsize=(10, 6)) # Define o tamanho da figura do gráfico
plt.plot(D_variavel, Custo_total_list, 'b-', label='Custo Total Anual') # Plota a curva de custo total vs diâmetro
plt.plot(D_variavel, Custo_energia_list, 'r:', label='Custo Energético Anual')
# Adiciona um ponto destacado no gráfico para indicar o diâmetro ótimo e o custo mínimo
plt.scatter(D_otimo, Custo_total_otimo, color='red', zorder=5, label=f'Ótimo (D={D_otimo:.4f} m, Custo={Custo_total_otimo:.2f} R$/ano)')
plt.xlabel("Diâmetro da Tubulação (m)") # Rótulo do eixo X
plt.ylabel("Custo Total Anual (R$/ano)") # Rótulo do eixo Y
plt.title("Custo Total Anual vs Diâmetro da Tubulação para Bombeamento de Biodiesel") # Título do gráfico
plt.grid(True) # Adiciona uma grade ao gráfico para facilitar a leitura
plt.legend() # Mostra a legenda do gráfico (incluindo o ponto ótimo)
plt.show() # Exibe o gráfico

# Plot 1: Head Loss vs Diameter
plt.figure(figsize=(10, 6))
plt.plot(D_variavel, hf_list, 'r--', label='Perda de Carga por Atrito')
plt.scatter(D_otimo, hf_otimo, color='blue', zorder=3, 
           label=f'hf_mínimo={hf_otimo:.2f} m')
plt.xlabel("Diâmetro da Tubulação (m)")
plt.ylabel("Perda de Carga (m)")
plt.title("Relação entre Diâmetro e Perda de Carga por Atrito")
plt.grid(True)
plt.legend()
plt.show()

# Plot 2: Pump Power vs Diameter
plt.figure(figsize=(10, 6))
plt.plot(D_variavel, Potencia_list, 'b-', linewidth=2, label='Potência hidráulica necessária da bomba')
plt.scatter(D_otimo, Potencia_otima, color='purple', zorder=5, label=f"P={Potencia_otima:.2f} W")
plt.xlabel("Diâmetro da Tubulação (m)")
plt.ylabel("Potência da Bomba (W)")
plt.title("Relação entre Diâmetro e Potência da Bomba")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.show()


