import os
import sys
import json
import time
import threading
import requests
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do Cloudinary com os dados da sua conta
cloudinary.config(
    cloud_name="dcigyfkwd",
    api_key="178348975469445",
    api_secret="x8gKGYkJJNH0uxkXDxvNuVjWHc0",
    secure=True
)

# Pasta de downloads (ajuste conforme necessário)
DOWNLOAD_FOLDER = r"C:\Users\Asus\Downloads"

# Lista onde as notícias processadas são armazenadas
dados_temporarios = []

@app.route('/exportar', methods=['POST'])
def exportar():
    global dados_temporarios
    dados = request.get_json()

    if not dados or 'noticias' not in dados:
        return jsonify({"status": "erro", "mensagem": "Nenhum dado de notícias recebido"}), 400

    noticias = dados["noticias"]
    # Filtra as notícias que possuam título e parágrafo não vazios
    noticias_filtradas = [n for n in noticias if n.get("title", "").strip() and n.get("paragraph", "").strip()]

    if not noticias_filtradas:
        return jsonify({"status": "erro", "mensagem": "Nenhuma notícia válida encontrada"}), 400

    dados_temporarios.extend(noticias_filtradas)

    return jsonify({
        "status": "sucesso",
        "mensagem": "Notícias recebidas e armazenadas!",
        "quantidade": len(noticias_filtradas)
    }), 200

@app.route('/dados', methods=['GET'])
def obter_dados():
    return jsonify({"noticias": dados_temporarios}), 200

@app.route('/imagens', methods=['GET'])
def listar_imagens():
    try:
        # Número de notícias processadas (ou parágrafos recebidos)
        quantidade_noticias = len(dados_temporarios)
        
        # Lista os arquivos que começam com "socialsnap_700pxx700px_"
        arquivos = [
            f for f in os.listdir(DOWNLOAD_FOLDER)
            if f.startswith("socialsnap_700pxx700px_") and os.path.isfile(os.path.join(DOWNLOAD_FOLDER, f))
        ]
        # Ordena os arquivos pela data de criação (mais antigo primeiro)
        arquivos.sort(key=lambda f: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, f)))
        
        # Seleciona somente os últimos arquivos, para que o número de imagens seja igual à quantidade de notícias
        if quantidade_noticias < len(arquivos):
            arquivos = arquivos[-quantidade_noticias:]
            arquivos.sort(key=lambda f: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, f)))
        
        image_urls = []
        for f in arquivos:
            file_path = os.path.join(DOWNLOAD_FOLDER, f)
            public_id = os.path.splitext(f)[0]
            try:
                upload_result = cloudinary.uploader.upload(file_path, public_id=public_id)
                secure_url = upload_result.get("secure_url")
                if secure_url:
                    image_urls.append(secure_url)
                else:
                    print(f"Falha no upload de {f}: Nenhuma secure_url retornada.")
            except Exception as e:
                print(f"Erro ao fazer upload de {f}: {e}")
        return jsonify({"imagens": image_urls}), 200
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

def obter_imagens_localmente():
    """
    Repete a lógica do endpoint /imagens para retornar a lista de URLs das imagens.
    """
    quantidade_noticias = len(dados_temporarios)
    arquivos = [
        f for f in os.listdir(DOWNLOAD_FOLDER)
        if f.startswith("socialsnap_700pxx700px_") and os.path.isfile(os.path.join(DOWNLOAD_FOLDER, f))
    ]
    arquivos.sort(key=lambda f: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, f)))
    if quantidade_noticias < len(arquivos):
        arquivos = arquivos[-quantidade_noticias:]
        arquivos.sort(key=lambda f: os.path.getctime(os.path.join(DOWNLOAD_FOLDER, f)))
    image_urls = []
    for f in arquivos:
        file_path = os.path.join(DOWNLOAD_FOLDER, f)
        public_id = os.path.splitext(f)[0]
        try:
            upload_result = cloudinary.uploader.upload(file_path, public_id=public_id)
            secure_url = upload_result.get("secure_url")
            if secure_url:
                image_urls.append(secure_url)
            else:
                print(f"Falha no upload de {f}: Nenhuma secure_url retornada.")
        except Exception as e:
            print(f"Erro ao fazer upload de {f}: {e}")
    return image_urls

def wait_for_images(timeout=60, poll_interval=5):
    """
    Aguarda até que pelo menos uma imagem seja encontrada ou até que o timeout seja atingido.
    """
    start_time = time.time()
    while True:
        imagens = obter_imagens_localmente()
        if imagens:
            return imagens
        if time.time() - start_time > timeout:
            return []
        print("Aguardando imagens para publicação...")
        time.sleep(poll_interval)

def publicar_instagram():
    """
    Seleciona a imagem e a notícia mais antigas, monta a legenda e efetua a publicação via API do Instagram.
    Cada etapa é verificada antes de prosseguir.
    """
    # Verifica se há notícias armazenadas
    if not dados_temporarios:
        print("Nenhuma notícia armazenada; não há o que publicar no Instagram.")
        return

    # Aguarda até que haja pelo menos uma imagem disponível
    imagens = wait_for_images(timeout=60, poll_interval=5)
    if not imagens:
        print("Timeout: Nenhuma imagem encontrada para publicação.")
        return

    # Seleciona a imagem e a notícia mais antigas (primeiro item de cada lista)
    imagem_url = imagens[0]
    noticia = dados_temporarios[0]
    titulo = noticia.get("title", "").strip()
    paragrafo = noticia.get("paragraph", "").strip()

    if paragrafo:
        legenda = f"{titulo}\n{paragrafo}\nLink na bio."
    else:
        legenda = f"{titulo}\nLink na bio."

    # Dados do Instagram Graph API - substitua "XXXXXX" pelos seus dados reais
    ig_user_id = "17841404760785911"
    access_token = "EAA325PSX9jUBOzb9h8fCNuQxzcZBjmQi4vjaOVq8B36kb2vvCZAZCEm5ZBlOzoDu3ZAsoIf7XALHI0GepH8xwDeYi971wp9qhj4NI1i18NAPwBYfhEd1khZBHZCezY0Bx58YPjcZBkldXfdooyMrsubGXqZBtTxsZBI1qqLRzwChei2tQqJX2ZCiY7cZBHFkqY57qwN3jnOMtd8F"

    # --- Passo 1: Criar o container de mídia ---
    create_media_url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media"
    create_params = {
        "image_url": imagem_url,
        "caption": legenda,
        "access_token": access_token
    }

    print("Criando container de mídia para Instagram...")
    create_response = requests.post(create_media_url, data=create_params)
    create_data = create_response.json()
    print("Resposta do container de mídia:", create_data)

    if "id" not in create_data:
        print("Erro ao criar container de mídia no Instagram. Processo abortado.")
        return

    creation_id = create_data["id"]

    # --- Passo 2: Publicar o container de mídia ---
    publish_media_url = f"https://graph.facebook.com/v17.0/{ig_user_id}/media_publish"
    publish_params = {
        "creation_id": creation_id,
        "access_token": access_token
    }

    print("Publicando a mídia no Instagram...")
    publish_response = requests.post(publish_media_url, data=publish_params)
    publish_data = publish_response.json()
    print("Resposta da publicação:", publish_data)

    # Remove a notícia publicada para evitar duplicidade
    dados_temporarios.pop(0)

def background_publisher():
    """
    Thread de fundo que verifica periodicamente se há notícias armazenadas
    e imagens disponíveis para publicar no Instagram.
    """
    while True:
        if dados_temporarios:
            print("Verificando condições para publicação no Instagram...")
            imagens = obter_imagens_localmente()
            if imagens:
                print("Condições atendidas, publicando no Instagram...")
                publicar_instagram()
            else:
                print("Nenhuma imagem disponível no momento.")
        else:
            print("Nenhuma notícia armazenada; aguardando...")
        time.sleep(30)  # Espera 30 segundos antes de verificar novamente

if __name__ == '__main__':
    # Inicia a thread de publicação em background
    publisher_thread = threading.Thread(target=background_publisher, daemon=True)
    publisher_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)
