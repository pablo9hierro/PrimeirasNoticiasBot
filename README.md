# Primeiras Notícias Bot

**Automação de Postagens no Instagram para o Portal "Primeiras Notícias Oficial"**

## Descrição do Projeto

O **Primeiras Notícias Bot** automatiza a captura de parágrafos e a geração de imagens (snaps) a partir do portal de notícias *Primeiras Notícias Oficial*, e publica automaticamente os conteúdos no Instagram. Esse sistema foi desenvolvido para otimizar um processo repetitivo, garantindo agilidade e precisão, e servindo como uma poderosa ferramenta de automação para o setor de mídia digital.

## Funcionalidades

- **Fluxo 1 – Captura de Parágrafos:**

  ![ativascriptparagrafo](https://github.com/user-attachments/assets/36ca852b-c20a-4fca-81e6-269df202d8f7)
  
  - Inicia com a inserção manual do ID da notícia.
  - 
    ![agurde](https://github.com/user-attachments/assets/4d4c07a4-6d30-4658-8ad0-e7a4b6ebb3af)

![processaoutroPraf](https://github.com/user-attachments/assets/4733ae3e-b328-4f6f-929f-19349f46faa0)


- **Fluxo 2 – Geração de Snaps:**
  - Inicia com a inserção manual do ID da notícia.
 ![paginaId](https://github.com/user-attachments/assets/123c3982-67a7-4a36-b0e8-d38556b03d38)

  - Navega até a página de Snap, clica no botão “Gerar Snap” e em seguida “Download”.
 
  - ![ekeqajq](https://github.com/user-attachments/assets/671b353e-f454-4068-83d8-ba9880c19d20)
  - 
![apertadown](https://github.com/user-attachments/assets/b7ebce44-bb5e-4360-aa03-2596b83c1566)

  - A imagem é automaticamente salva na pasta `snaps`.

- **Postagem Automática:**
  - Um bot em Python, usando a biblioteca **instagrapi**, varre a pasta `snaps` e associa cada imagem com o respectivo parágrafo (usando a ordem de chegada).
  - Publica as postagens no Instagram com legendas formatadas (iniciando com uma quebra de linha, o parágrafo e “Link na bio.”).
  - Inclui delays aleatórios entre postagens para reduzir o risco de bloqueio.

## Tecnologias Utilizadas

- **Front-end / Automação Web:** JavaScript (Userscript via Tampermonkey)
- **Back-end:** Python, instagrapi, Flask, Flask-CORS, Git
- **Hospedagem:** GitHub Pages


## Estrutura do Projeto

Como Configurar e Executar

git clone https://github.com/pablo9hierro/PrimeirasNoticiasBot.git
cd PrimeirasNoticiasBot

2. Configurar o Ambiente Python

python -m venv venv
venv\Scripts\activate  # No Windows

Instale as dependências:

pip install -r requirements.txt

3. Configurar as Credenciais e Caminhos

No arquivo bot.py, ajuste as variáveis:

USERNAME e PASSWORD 
CAMINHO_PARAGRAFOS (por exemplo, C:\Users\Asus\Documents\insta_post_bot\dados_paragrafos.json)
PASTA_IMAGENS (por exemplo, C:\Users\Asus\Documents\insta_post_bot\snaps)

4. Iniciar o Servidor

python server.py

![servidoriniciado](https://github.com/user-attachments/assets/601a6db9-ce62-44b8-b6d1-483d4b521217)

5. Iniciar o Bot de Postagem

python bot.py

![cmdd](https://github.com/user-attachments/assets/1199dd38-3954-4f6b-a07f-4c8f1d44084f)

Conclusão
O Primeiras Notícias Bot demonstra como automatizar processos repetitivos utilizando ferramentas modernas. Este projeto é um exemplo prático de como aplicar automação web, scraping e integração com redes sociais para otimizar fluxos de trabalho.

Licença
Este projeto está licenciado sob a Licença MIT.

Contato
LinkedIn: https://www.linkedin.com/in/pablo9hierro
E-mail: pablo9hierro@gmail.com
