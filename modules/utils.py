"""
Módulo de utilidades para streaming de vídeo.
Contém funções para seleção de arquivos, distribuição de vídeos e controle de streaming.
"""

import sys
import os
import subprocess
import time
import random
from tkinter import filedialog, Tk
from colorama import Fore, Style
from modules.art import bot_logo, colors
import platform

# Constantes de configuração
ALLOWED_TYPES = "*.mp4 *.png *.gif"
IS_LIVE_CURRENTLY = False
STOPPED_STREAMING = True

# Configurações de qualidade de vídeo (otimizadas para leveza)
CONFIGS = {
    "160": {
        "resolution": "284x160",
        "bitrate": "150k -maxrate 200k -bufsize 400k"  # Reduzido bitrate para 160p
    },
    "360": {
        "resolution": "640x360",
        "bitrate": "500k -maxrate 800k -bufsize 1600k"
    },
    "480": {
        "resolution": "854x480",
        "bitrate": "800k -maxrate 1200k -bufsize 2400k"
    },
    "720": {
        "resolution": "1280x720",
        "bitrate": "1500k -maxrate 2000k -bufsize 4000k"
    },
    "1080": {
        "resolution": "1920x1080",
        "bitrate": "2000k -maxrate 3000k -bufsize 6000k"
    }
}

# Configurações de codecs (otimizadas para performance)
CODECS = {
    "None": "-profile:v baseline -level 3.0 -c:v libx264 -preset ultrafast -tune zerolatency -threads 4 ",
    "NVIDIA": "-profile:v baseline -level 3.0 -c:v h264_nvenc -preset p7 -tune ll -rc cbr ",
    "AMD": "-profile:v baseline -usage ultralowlatency -c:v h264_amf -quality speed -rc cbr ",
}

def get_ffmpeg_path():
    system = platform.system().lower()
    if system == "windows":
        ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe")
        return ffmpeg_path
    else:
        return "ffmpeg"

FFMPEG_PATH = get_ffmpeg_path()

def resource_path(another_way: str) -> str:
    """
    Retorna o caminho absoluto para um recurso, funcionando tanto em desenvolvimento quanto em produção.

    Args:
        another_way (str): Caminho relativo do recurso

    Returns:
        str: Caminho absoluto do recurso
    """
    try:
        usual_way = sys._MEIPASS
    except Exception:
        usual_way = os.path.dirname(__file__)
    return os.path.join(usual_way, another_way)

def choose_files() -> list:
    """
    Abre um diálogo para seleção de múltiplos arquivos de vídeo.
    """
    print(f"\n{Fore.YELLOW}[BOT]{Fore.WHITE} Selecione os vídeos para stream (formatos suportados: mp4, png, gif)")
    print(f"{Fore.YELLOW}[BOT]{Fore.WHITE} Você pode selecionar múltiplos vídeos segurando CTRL e clicando nos arquivos")
    print(f"{Fore.YELLOW}[BOT]{Fore.WHITE} Se selecionar apenas 1 vídeo, ele será usado em todos os canais{Fore.RESET}")
    
    root = Tk()
    root.withdraw()
    
    files = filedialog.askopenfilenames(
        title="Selecione os vídeos para stream",
        filetypes=[
            ("Arquivos de Mídia", "*.mp4 *.png *.gif"),
            ("Todos os arquivos", "*.*")
        ]
    )
    
    selected_files = list(files)
    
    if selected_files:
        print(f"\n{Fore.YELLOW}[BOT]{Fore.WHITE} Vídeos selecionados:")
        for idx, file in enumerate(selected_files, 1):
            print(f"{Fore.YELLOW}[{idx}]{Fore.WHITE} {os.path.basename(file)}{Fore.RESET}")
    else:
        print(f"\n{Fore.LIGHTRED_EX}[BOT] Nenhum vídeo foi selecionado!{Fore.RESET}")
    
    return selected_files

def distribute_videos(videos: list, channels: list) -> dict:
    """
    Distribui vídeos entre os canais minimizando repetições.

    Args:
        videos (list): Lista de caminhos dos vídeos
        channels (list): Lista de nomes dos canais

    Returns:
        dict: Dicionário com a distribuição {canal: video}
    """
    if not videos:
        return {}
        
    distribution = {}
    available_videos = videos.copy()
    
    if len(videos) == 1:
        return {channel: videos[0] for channel in channels}
    
    for channel in channels:
        if not available_videos:
            used_videos = list(distribution.values())[-len(videos):]
            available_videos = [v for v in videos if v not in used_videos]
            
            if not available_videos:
                available_videos = videos.copy()
        
        video = random.choice(available_videos)
        distribution[channel] = video
        available_videos.remove(video)
    
    return distribution

def start_streaming(file: str, stream_keys: list, quality: str, debug_mode: bool, gpu: str) -> None:
    """
    Inicia o streaming de um arquivo para múltiplas chaves do Twitch.
    """
    global IS_LIVE_CURRENTLY, STOPPED_STREAMING
    STOPPED_STREAMING = False
    
    # Configurações de retry
    max_retries = 3
    retry_delay = 5
    retry_count = 0
    
    # Adiciona logger para cada key
    from modules.logger import Logger
    loggers = {}
    for key in stream_keys:
        loggers[key] = Logger(key)
        loggers[key].info(f"Iniciando configuração de streaming para a chave: {key[:20]}...")  # Log adicionado
    
    # Verifica FFmpeg antes de iniciar
    if not verify_ffmpeg():
        for key in stream_keys:
            loggers[key].error("FFmpeg não encontrado!")
        return
    
    while retry_count < max_retries and not STOPPED_STREAMING:   
        try:
            # Escapa caracteres especiais no caminho do arquivo
            file = file.replace("\\", "/")
            
            # Extrai largura e altura da resolução
            width, height = CONFIGS[quality]['resolution'].split('x')
            
            # Log das configurações
            for key in stream_keys:
                loggers[key].info(f"Configurações de streaming:")
                loggers[key].info(f"- Arquivo: {file}")
                loggers[key].info(f"- Qualidade: {quality} ({width}x{height})")
                loggers[key].info(f"- GPU: {gpu}")
                loggers[key].info(f"- Bitrate: {CONFIGS[quality]['bitrate']}")
            
            # Monta o comando como uma lista de argumentos
            command = [
                FFMPEG_PATH,
                "-hwaccel", "auto",
                "-stream_loop", "-1",
                "-i", file,
                "-map", "0:v",
                "-map", "0:a?",
                "-c:a", "aac",
                "-b:a", "96k",
                "-ar", "44100",
                "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,fps=30",
                "-pix_fmt", "yuv420p",
                "-g", "60",
                "-preset", "ultrafast",
                "-tune", "zerolatency",
                "-threads", "4",
                "-bufsize", "8000k",
                "-max_muxing_queue_size", "1024",
                "-fflags", "+genpts",
                "-flags", "+global_header"
            ]
            
            # Adiciona argumentos do codec baseado no GPU
            command.extend(CODECS[gpu].split())
            
            # Adiciona configurações de bitrate
            command.extend(f"-b:v {CONFIGS[quality]['bitrate']}".split())
            
            # Adiciona formato de saída
            command.extend(["-f", "flv"])
            
            # Para múltiplos outputs, usamos um rtmp para cada stream
            if len(stream_keys) == 1:
                rtmp_url = f"rtmp://live.twitch.tv/app/{stream_keys[0]}"
                command.append(rtmp_url)
                loggers[stream_keys[0]].info(f"Iniciando stream para: rtmp://live.twitch.tv/app/[CHAVE_OCULTA]")
            else:
                command.extend(["-f", "tee"])
                outputs = []
                for key in stream_keys:
                    outputs.append(f"[f=flv]rtmp://live.twitch.tv/app/{key}")
                    loggers[key].info(f"Iniciando stream múltipla para: rtmp://live.twitch.tv/app/[CHAVE_OCULTA]")
                command.append("|".join(outputs))
            
            # Log do comando completo (ocultando as chaves)
            cmd_log = " ".join(command).replace(stream_keys[0], "[CHAVE_OCULTA]")
            for key in stream_keys:
                loggers[key].debug(f"Comando FFmpeg: {cmd_log}")
            
            IS_LIVE_CURRENTLY = True
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                shell=False
            )
            
            # Monitora a saída do FFmpeg em tempo real
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    for key in stream_keys:
                        if "speed=" in output:  # Log de progresso do FFmpeg
                            loggers[key].debug(f"FFmpeg: {output.strip()}")
                        else:
                            loggers[key].info(f"FFmpeg: {output.strip()}")
            
            return_code = process.poll()
            if return_code != 0:
                for key in stream_keys:
                    loggers[key].error(f"FFmpeg encerrou com código de erro: {return_code}")
                retry_count += 1
                if retry_count < max_retries:
                    for key in stream_keys:
                        loggers[key].info(f"Tentando reconectar em {retry_delay} segundos... (Tentativa {retry_count + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    continue
            break
                
        except Exception as e:
            for key in stream_keys:
                loggers[key].error(f"Erro durante o streaming: {str(e)}")
                loggers[key].error(f"Detalhes do erro: {sys.exc_info()}")
            retry_count += 1
            if retry_count < max_retries:
                for key in stream_keys:
                    loggers[key].info(f"Tentando reconectar em {retry_delay} segundos... (Tentativa {retry_count + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                for key in stream_keys:
                    loggers[key].error("Número máximo de tentativas atingido. Encerrando streaming.")
                break

def stop_streaming() -> None:
    """
    Para todos os processos de streaming em execução.
    """
    try:
        global IS_LIVE_CURRENTLY, STOPPED_STREAMING
        IS_LIVE_CURRENTLY = False
        STOPPED_STREAMING = True
        
        system = platform.system().lower()
        if system == "windows":
            subprocess.run("taskkill /f /im ffmpeg.exe >nul 2>&1", shell=True)
        else:
            subprocess.run("pkill -f ffmpeg", shell=True)
    except Exception as e:
        pass

def verify_ffmpeg():
    """Verifica se o FFmpeg está disponível e retorna informações sobre a instalação"""
    from modules.logger import Logger
    logger = Logger("system")
    
    logger.info(f"Verificando FFmpeg em: {FFMPEG_PATH}")
    
    if os.path.exists(FFMPEG_PATH):
        logger.info("Arquivo FFmpeg encontrado")
        try:
            result = subprocess.run(
                [FFMPEG_PATH, "-version"],
                capture_output=True,
                text=True,
                shell=False
            )
            if result.returncode == 0:
                logger.info(f"FFmpeg versão: {result.stdout.split('version')[1].split()[0]}")
                return True
            else:
                logger.error(f"FFmpeg retornou erro: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Erro ao executar FFmpeg: {str(e)}")
            return False
    else:
        logger.error(f"FFmpeg não encontrado em: {FFMPEG_PATH}")
        logger.info("Por favor, coloque o ffmpeg.exe em ffmpeg/bin/ffmpeg.exe")
        return False

def check_twitch_connection(stream_key):
    """Verifica se a conexão com a Twitch está ativa"""
    try:
        import socket
        s = socket.create_connection(("live.twitch.tv", 1935), timeout=5)
        s.close()
        return True
    except:
        return False
