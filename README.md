# Coletor de Dados do YouTube com MongoDB

Este projeto coleta automaticamente **comentários**, **transcrições**, **livechats** e **superchats** de vídeos de um canal do YouTube, utilizando a biblioteca [`youtool`](https://github.com/PythonicCafe/youtool), e armazena os dados em um banco de dados **MongoDB**.

---

## ✅ Objetivo

Trabalho prático da disciplina de **NoSQL**, com foco em:

- Consumo da API do YouTube
- Armazenamento em banco de dados NoSQL (MongoDB)
- Manipulação de dados não estruturados (comentários, chats, etc.)
- Boas práticas com variáveis de ambiente (`dotenv`)

---

## 🔍 Canal analisado

[**Flow Podcast**](https://www.youtube.com/@FlowPodcast)\
A coleta é aplicada sobre os **10 vídeos mais recentes** do canal.

---

## 🛠️ Tecnologias utilizadas

- Python 3.12+
- MongoDB (local)
- [youtool](https://github.com/PythonicCafe/youtool)
- pymongo
- chat-downloader
- dotenv (`python-dotenv`)
- yt-dlp (para transcrições)

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/abnerdouglas/youtool.git
cd youtool
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🔐 Configuração com `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
API_KEY=sua_chave_youtube_aqui
MONGO_URI=mongodb://localhost:27017/
```

---

## 🚀 Execução

```bash
python index.py
```

Durante a execução, os seguintes dados são coletados e armazenados no MongoDB:

- `playlists`: playlists do canal
- `videos_playlist`: vídeos de cada playlist
- `flow_videos`: metadados completos dos vídeos oficiais
- `videos_infos`: detalhes do último vídeo
- `transcricoes`: caminhos e status dos arquivos `.vtt`
- `livechat`: chat ao vivo de uma live conhecida
- `canais`: dados do canal principal

---

## 📂 Estrutura esperada no MongoDB

Banco: `youtube_data`

| Coleção           | Conteúdo                          |
| ----------------- | --------------------------------- |
| `playlists`       | Playlists do canal                |
| `videos_playlist` | Vídeos contidos em playlists      |
| `flow_videos`     | 10 vídeos oficiais mais recentes  |
| `videos_infos`    | Dados completos do último vídeo   |
| `transcricoes`    | Caminho e status das transcrições |
| `livechat`        | Chat ao vivo e superchats         |
| `canais`          | Informações detalhadas do canal   |

---

## 🎥 Demonstração

- **GIF/Vídeo de demonstração aqui (1 min e 35 s):**

![GIF](./youtool-gif.gif)

---

## 👨‍💼 Autores

- Abner Machado
- Pedro Kajiya
- Bruno Silvério

---

## 📚 Fontes de apoio

- [youtool – GitHub](https://github.com/PythonicCafe/youtool)
- [Palestra Python Brasil 2024 – YouTube](https://youtu.be/1jBGuR3dw8s?t=6193)
- [Slides da apresentação – Turicas](http://turicas.info/slides/youtool/#/)

