import math

def calcular_ieg(ap, ca, fc, pc, esc, car):
    return 0.30*ap + 0.25*ca + 0.15*fc + 0.10*pc + 0.15*esc - 0.05*car

def probabilidade_gol(ieg, mu=2.5, s=1):
    return 1 / (1 + math.exp(-(ieg - mu) / s))


if __name__ == "__main__":
    ap, ca, fc, pc, esc, car = 4, 2, 3, 62, 1, 0
    ieg = calcular_ieg(ap, ca, fc, pc, esc, car)
    p_gol = probabilidade_gol(ieg)
    print(f"Probabilidade de gol nos próximos 10': {p_gol:.2%}") 
import os

mu = float(os.getenv("MU", 2.5))
s = float(os.getenv("S", 1))
intervalo = int(os.getenv("INTERVALO_MIN", 10))
debug = os.getenv("DEBUG", "False") == "True"
import requests

url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"
querystring = {"fixture": "4f980390b7fa2a4dd8246167b3a199"}  # substitua pelo ID correto

headers = {
    "X-RapidAPI-Key": "SUA_CHAVE_AQUI",
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
dados = response.json()
print("Conteúdo da resposta da API:")
print(dados)
for time in dados['response']:
    nome_time = time['team']['name']
    estatisticas = {estat['type']: estat['value'] for estat in time['statistics']}
    print(f"{nome_time}: {estatisticas}")
import requests

url = "URL_DA_API_AQUI"
resposta = requests.get(url)

try:
    dados = resposta.json()
    if 'resposta' in dados:
        for time in dados['resposta']:
            # processa os dados do time
            print(time)
    else:
        print("⚠️ Chave 'resposta' não encontrada na resposta da API.")
        print("Conteúdo recebido:", dados)
except Exception as e:
    print("❌ Erro ao processar resposta da API:", e)
import time

while True:
    # 1. Buscar dados da API
    # 2. Calcular IEG e P(gol)
    # 3. Salvar ou exibir os resultados
    print("Atualizando probabilidade de gol...")
    time.sleep(300)  # espera 5 minutos
import requests
import math

# Funções do modelo
def calcular_ieg(ap, ca, fc, pc, esc, car):
    return 0.30*ap + 0.25*ca + 0.15*fc + 0.10*pc + 0.15*esc - 0.05*car

def probabilidade_gol(ieg, mu=2.5, s=1):
    return 1 / (1 + math.exp(-(ieg - mu) / s))

# Endpoint da API-Futebol
url = "https://api.api-futebol.com.br/v1/ao-vivo"
headers = {
    "Authorization": "Bearer live_4f980390b7fa2a4dd8246167b3a199"
}

# Consulta à API
resposta = requests.get(url, headers=headers)
dados = resposta.json()

# Verifica se há jogos ao vivo
if 'jogos' in dados:
    for jogo in dados['jogos']:
        mandante = jogo['time_mandante']['nome_popular']
        visitante = jogo['time_visitante']['nome_popular']
        estat_mandante = jogo.get('estatisticas', {}).get('mandante', [])
        estat_visitante = jogo.get('estatisticas', {}).get('visitante', [])

        def extrair_metrica(estats, chave):
            return next((int(item['quantidade']) for item in estats if item['tipo'] == chave), 0)

        # Métricas do mandante
        ap = extrair_metrica(estat_mandante, "Ataques Perigosos")
        ca = extrair_metrica(estat_mandante, "Chutes ao Gol")
        fc = extrair_metrica(estat_mandante, "Finalizações")
        pc = extrair_metrica(estat_mandante, "Posse de Bola")
        esc = extrair_metrica(estat_mandante, "Escanteios")
        car = extrair_metrica(estat_mandante, "Cartões")

        ieg = calcular_ieg(ap, ca, fc, pc, esc, car)
        p_gol = probabilidade_gol(ieg)

        print(f"{mandante} vs {visitante}")
        print(f"→ IEG: {ieg:.2f}")
        print(f"→ Probabilidade de gol nos próximos 10': {p_gol:.2%}")
        print("-" * 40)
else:
    print("⚠️ Nenhum jogo ao vivo encontrado ou chave inválida.")
    print("Resposta da API:", dados)
