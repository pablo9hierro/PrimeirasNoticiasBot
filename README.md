# Primeiras Notícias Bot

**Automação de Postagens no Instagram para o Portal "Primeiras Notícias Oficial"**

## Descrição do Projeto

O **Primeiras Notícias Bot** automatiza a captura de parágrafos e a geração de imagens (snaps) a partir do portal de notícias *Primeiras Notícias Oficial*, e publica automaticamente os conteúdos no Instagram. Esse sistema foi desenvolvido para otimizar um processo repetitivo, garantindo agilidade e precisão, e servindo como uma poderosa ferramenta de automação para o setor de mídia digital.

## Funcionalidades

- **Fluxo 1 – Captura de Parágrafos:**
  - Inicia com a inserção manual do ID da notícia.
  - Automatiza a navegação: clica no título da notícia e captura o primeiro parágrafo.
  - Retorna para a página de listagem e repete o processo até capturar todos os parágrafos.
  - Ao final, gera um arquivo JSON com os parágrafos ordenados (para servir como descrição da publicação no instagram).

- **Fluxo 2 – Geração de Snaps:**
  - Inicia com a inserção manual do ID da notícia.
  - Navega até a página de Snap, clica no botão “Gerar Snap” e em seguida “Download”.
  - A imagem é automaticamente salva na pasta `snaps`.

- **Postagem Automática:**
  - Um bot em Python, usando a biblioteca **instagrapi**, varre a pasta `snaps` e associa cada imagem com o respectivo parágrafo (usando a ordem de chegada).
  - Publica as postagens no Instagram com legendas formatadas (iniciando com uma quebra de linha, o parágrafo e “Link na bio.”).
  - Inclui delays aleatórios entre postagens para reduzir o risco de bloqueio.

## Tecnologias Utilizadas

- **Front-end / Automação Web:** JavaScript (Userscript via Tampermonkey)
- **Back-end:** Python, instagrapi, Flask, Flask-CORS
- **Hospedagem:** GitHub Pages (para documentação visual) e Vercel/Netlify para o portfólio
- **Outras Ferramentas:** Git para versionamento

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

5. Iniciar o Bot de Postagem

python bot.py

Conclusão
O Primeiras Notícias Bot demonstra como automatizar processos repetitivos utilizando ferramentas modernas. Este projeto é um exemplo prático de como aplicar automação web, scraping e integração com redes sociais para otimizar fluxos de trabalho.

Licença
Este projeto está licenciado sob a Licença MIT.

Contato
LinkedIn: https://www.linkedin.com/in/pablo9hierro
E-mail: pablo9hierro@gmail.com
