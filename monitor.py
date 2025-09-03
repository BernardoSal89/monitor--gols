import os
import time
import math
import requests
import sys

# ─── Configurações ────────────────────────────────────────────────────────────

API_KEY       = "live_4f980390b7fa2a4dd8246167b3a199"
ENDPOINT      = "https://api.api-futebol.com.br/v1/ao-vivo"

# Parâmetros configuráveis por variável de ambiente
MU            = float(os.getenv("MU", 2.5))
S             = float(os.getenv("S", 1.0))
INTERVALO_MIN = int(os.getenv("INTERVALO_MIN", 5))   # intervalo em minutos
DEBUG         = os.getenv("DEBUG", "False") == "True"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

# ─── Modelo: IEG e Probabilidade ───────────────────────────────────────────────

def calcular_ieg(ap, ca, fc, pc, esc, car):
    """
    Índice de Expectativa de Gol (IEG)
    ap: ataques perigosos
    ca: chutes ao gol
    fc: finalizações
    pc: posse de bola (%)
    esc: escanteios
    car: cartões
    """
    return 0.30*ap + 0.25*ca + 0.15*fc + 0.10*pc + 0.15*esc - 0.05*car

def probabilidade_gol(ieg, mu=MU, s=S):
    """
    Função logística que retorna P(gol).
    """
    return 1 / (1 + math.exp(-(ieg - mu) / s))

# ─── Auxiliar para extrair estatística ────────────────────────────────────────

def extrair_metrica(lista_estats, chave):
    """
    Procura em lista_estats um dicionário com 'tipo' == chave
    e retorna int(valor) ou 0 se não encontrar.
    """
    return next(
        (int(item["quantidade"]) for item in lista_estats if item["tipo"] == chave),
        0
    )

# ─── Loop Principal ────────────────────────────────────────────────────────────

def main():
    while True:
        if DEBUG:
            print(f"\n[DEBUG] Iniciando nova consulta às {time.strftime('%H:%M:%S')}")

        try:
            resp = requests.get(ENDPOINT, headers=HEADERS, timeout=10)
        except requests.RequestException as e:
            print("❌ Erro de conexão:", e)
            time.sleep(INTERVALO_MIN * 60)
            continue

        if resp.status_code != 200:
            print(f"❌ API retornou HTTP {resp.status_code}: {resp.text}")
            time.sleep(INTERVALO_MIN * 60)
            continue

        try:
            dados = resp.json()
        except ValueError:
            print("❌ Resposta não é JSON válido:", resp.text)
            time.sleep(INTERVALO_MIN * 60)
            continue

        # Valida presença de jogos ao vivo
        jogos = dados.get("jogos")
        if not jogos:
            print("⚠️ Nenhum jogo ao vivo encontrado ou chave inválida.")
            if DEBUG:
                print("[DEBUG] Payload completo:", dados)
            time.sleep(INTERVALO_MIN * 60)
            continue

        # Processa cada partida
        for jogo in jogos:
            mand = jogo["time_mandante"]
            vis  = jogo["time_visitante"]
            est_mand = jogo.get("estatisticas", {}).get("mandante", [])
            est_vis  = jogo.get("estatisticas", {}).get("visitante", [])

            # Extrai métricas do mandante (faça o mesmo para o visitante, se quiser)
            ap   = extrair_metrica(est_mand, "Ataques Perigosos")
            ca   = extrair_metrica(est_mand, "Chutes ao Gol")
            fc   = extrair_metrica(est_mand, "Finalizações")
            pc   = extrair_metrica(est_mand, "Posse de Bola")
            esc  = extrair_metrica(est_mand, "Escanteios")
            car  = extrair_metrica(est_mand, "Cartões")

            ieg  = calcular_ieg(ap, ca, fc, pc, esc, car)
            pg   = probabilidade_gol(ieg)

            print(f"{mand['nome_popular']} x {vis['nome_popular']}")
            print(f" → IEG do mandante: {ieg:.2f}")
            print(f" → Probabilidade de gol nos próximos {INTERVALO_MIN}': {pg:.2%}")
            print("-" * 40)

        # Aguarda próximo ciclo
        time.sleep(INTERVALO_MIN * 60)

if __name__ == "__main__":
    main()
