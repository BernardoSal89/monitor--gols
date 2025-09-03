import math

def calcular_ieg(ap, ca, fc, pc, esc, car):
    return 0.30*ap + 0.25*ca + 0.15*fc + 0.10*pc + 0.15*esc - 0.05*car

def probabilidade_gol(ieg, mu=2.5, s=1):
    return 1 / (1 + math.exp(-(ieg - mu) / s))

# Exemplo de uso
if __name__ == "__main__":
    ap, ca, fc, pc, esc, car = 4, 2, 3, 62, 1, 0
    ieg = calcular_ieg(ap, ca, fc, pc, esc, car)
    p_gol = probabilidade_gol(ieg)
    print(f"Probabilidade de gol nos próximos 10': {p_gol:.2%}") 
