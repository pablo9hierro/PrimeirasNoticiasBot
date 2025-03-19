import os
import json
import time
import random
from instagrapi import Client

# Parâmetros fixos

CAMINHO_PARAGRAFOS = r"C:\Users\Asus\Downloads\paragrafos_instagram_ordenado.json"
PASTA_IMAGENS = r"C:\Users\Asus\Documents\insta_post_bot\snaps"
LEGENDA_ADICIONAL = "Link na bio."
DELAY_MIN = 3
DELAY_MAX = 6

def carregar_paragrafos(caminho_json):
    with open(caminho_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Retorna a lista de parágrafos em ordem de chegada
    return data.get("paragrafos", [])

def login_instagram(usuario, senha):
    cl = Client()
    cl.login(usuario, senha)
    print("✅ Login realizado com sucesso!")
    return cl

def esperar_imagens(pasta, expected_count):
    print(f"⏳ Aguardando que a pasta '{pasta}' contenha ao menos {expected_count} imagens...")
    while True:
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(".jpg")]
        if len(arquivos) >= expected_count:
            return arquivos
        time.sleep(10)

def postar_imagens(cl, pasta_imagens, paragrafos, legenda_adicional, delay_min, delay_max):
    total_paragrafos = len(paragrafos)
    # Espera que a pasta tenha ao menos o número esperado de imagens
    arquivos = esperar_imagens(pasta_imagens, total_paragrafos)
    
    # Ordena os arquivos pela data de modificação (mais antigos primeiro, mais recentes depois)
    arquivos_ordenados = sorted(arquivos, key=lambda x: os.path.getmtime(os.path.join(pasta_imagens, x)))
    
    if len(arquivos_ordenados) != total_paragrafos:
        print(f"⚠️ Número de imagens ({len(arquivos_ordenados)}) e de parágrafos ({total_paragrafos}) não coincidem.")
        return

    print("Iniciando postagem: associando imagens com parágrafos na ordem natural.")
    for i in range(total_paragrafos):
        imagem_selecionada = arquivos_ordenados[i]
        caminho_imagem = os.path.join(pasta_imagens, imagem_selecionada)
        texto_paragrafo = paragrafos[i].get("texto", f"Notícia {i+1}")
        # Legenda com quebra de linha antes do parágrafo e antes do Link na bio
        legenda = f"\n\n{texto_paragrafo}\n\n{legenda_adicional}"
        
        print(f"\n[{i+1}/{total_paragrafos}] Publicando imagem '{imagem_selecionada}' para o parágrafo {i+1}...")
        try:
            cl.photo_upload(caminho_imagem, legenda)
            print(f"✅ Postagem {i+1} concluída!")
        except Exception as e:
            print(f"❌ Erro ao postar imagem '{imagem_selecionada}': {e}")
        
        delay = random.randint(delay_min, delay_max)
        print(f"⏳ Aguardando {delay} segundos antes da próxima postagem...")
        time.sleep(delay)
        
        try:
            os.remove(caminho_imagem)
            print(f"🗑️ Imagem '{imagem_selecionada}' removida.")
        except Exception as e:
            print(f"Erro ao remover a imagem '{imagem_selecionada}': {e}")

if __name__ == "__main__":
    print("Iniciando bot de postagem automático no Instagram...")
    paragrafos = carregar_paragrafos(CAMINHO_PARAGRAFOS)
    if not paragrafos:
        print("Nenhum parágrafo encontrado no JSON. Verifique o arquivo.")
        exit(1)
    cl = login_instagram(USERNAME, PASSWORD)
    postar_imagens(cl, PASTA_IMAGENS, paragrafos, LEGENDA_ADICIONAL, DELAY_MIN, DELAY_MAX)
    print("🎉 Todas as postagens foram concluídas!")
