from pprint import pprint
from pathlib import Path
from pymongo import MongoClient
from youtool import YouTube
from decimal import Decimal
from dotenv import load_dotenv
import os

load_dotenv()

# Função auxiliar: converte Decimals para float em dados aninhados
def fix_decimal_fields(doc):
    if isinstance(doc, list):
        return [fix_decimal_fields(item) for item in doc]
    elif isinstance(doc, dict):
        return {
            k: fix_decimal_fields(v) if isinstance(v, (dict, list)) else (float(v) if isinstance(v, Decimal) else v)
            for k, v in doc.items()
        }
    return doc

# Configuração MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["youtube_data"]

# Inicialização YouTool com API Key
api_keys = [os.getenv("API_KEY")]
yt = YouTube(api_keys, disable_ipv6=True)

# Coletar ID do canal Flow Podcast
channel_url = "https://www.youtube.com/@FlowPodcast"
channel_id = yt.channel_id_from_url(channel_url)
assert channel_id.startswith("UC")
print(f"🎯 Canal selecionado: Flow Podcast ({channel_id})")

# Diretório para transcrições
download_path = Path("transcricoes")
download_path.mkdir(parents=True, exist_ok=True)

# 1. Coletar playlists do canal
print("▶️ Playlists do canal:")
for playlist in yt.channel_playlists(channel_id):
    print(f"Playlist: {playlist['title']}")
    db["playlists"].insert_one(playlist)
    for video in yt.playlist_videos(playlist["id"]):
        print(f"  📹 Vídeo: {video['title']}")
        db["videos_playlist"].insert_one(video)
    print("-" * 80)

# 2. Coletar vídeos do canal Flow Podcast com metadados completos
print("🎥 Coletando vídeos oficiais do canal Flow Podcast:")
uploads_playlist = "UU" + channel_id[2:]
videos_from_channel = list(yt.playlist_videos(uploads_playlist))[:10]  # limite para 10 vídeos recentes

# Buscar metadados completos
video_ids = [video["id"] for video in videos_from_channel]
complete_infos = list(yt.videos_infos(video_ids))

# Inserir no MongoDB
db["flow_videos"].insert_many(fix_decimal_fields(complete_infos))

# Usar o vídeo mais recente como base
last_video = complete_infos[0]
video_id = last_video["id"]

print(f"✅ Total de vídeos coletados: {len(complete_infos)}")
print("-" * 80)

# 3. Obter detalhes do último vídeo coletado
print("ℹ️ Detalhes do último vídeo oficial:")
pprint(last_video)
db["videos_infos"].insert_one(fix_decimal_fields(last_video))
print("-" * 80)

# 4. Informações do canal Flow Podcast
print("📡 Informações do canal:")
for canal_info in yt.channels_infos([channel_id]):
    pprint(canal_info)
    db["canais"].insert_one(canal_info)
print("-" * 80)


# 5. Livechat de um vídeo conhecido com live
live_video_id = "yyzIPQsa98A"
print(f"💬 Livechat do vídeo {live_video_id}:")
try:
    livechat = list(yt.video_livechat(live_video_id))
    for message in livechat:
        print(message)
    if livechat:
        db["livechat"].insert_many(fix_decimal_fields(livechat))
except Exception as e:
    print(f"⚠️ Livechat indisponível: {e}")
print("-" * 80)

# 6. Transcrição de dois vídeos
print(f"📝 Transcrição de {video_id} e {live_video_id}:")
try:
    for downloaded in yt.download_transcriptions([video_id, live_video_id], language_code="pt", path=download_path):
        info = {
            "video_id": downloaded["video_id"],
            "status": downloaded["status"],
            "file_path": str(downloaded["filename"]),
            "size_kb": downloaded["filename"].stat().st_size / 1024 if downloaded["status"] == "done" else None
        }
        print(info)
        db["transcricoes"].insert_one(info)
except Exception as e:
    print(f"⚠️ Falha ao baixar transcrição: {e}")
print("-" * 80)

# 7. Consumo de cota da API
print("📊 Cota utilizada nesta sessão:")
total_used = 0
for method, units_used in yt.used_quota.items():
    print(f"{method:25}: {units_used:03d} unit(s)")
    total_used += units_used
print(f"TOTAL                     : {total_used:03d} unit(s)")
