import os
import sys
import time
from modules.utils import choose_files, distribute_videos, start_streaming, stop_streaming
from modules.art import bot_logo
import questionary
from colorama import Fore, Style as ColoramaStyle
from questionary import Style as QuestionaryStyle
from modules.interface_manager import InterfaceManager
import threading
import platform

# Configuração de Debug
DEBUG_MODE = False  # Altere para True para ativar o modo debug

# Função para limpar a tela de forma cross-platform
def clear_screen():
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")

clear_screen()
bot_logo()

# Atualiza o estilo do questionary para usar cores personalizadas
custom_style = QuestionaryStyle([
    ('qmark', 'fg:#ffff00'),  # Amarelo para o [BOT]
    ('question', 'fg:#ffffff nobold'),  # Branco sem negrito
    ('answer', 'fg:#ffffff nobold'),  # Branco sem negrito
    ('pointer', 'fg:#ffff00 nobold'),  # Amarelo sem negrito
    ('highlighted', 'fg:#ffff00 nobold'),  # Amarelo sem negrito
    ('selected', 'fg:#ffff00 nobold'),  # Amarelo sem negrito
    ('text', 'fg:#ffffff nobold'),  # Branco sem negrito
    ('instruction', 'fg:#ffffff nobold'),  # Branco sem negrito
    ('disabled', 'fg:#858585 nobold')  # Cinza sem negrito
])

ACCOUNTS_PATH = os.path.join(os.getcwd(), "channels_keys.txt")
ACCOUNTS = {}  # Mudado para dicionário
error_sleep_time = 10

# Carrega todas as chaves disponíveis
if os.path.exists(ACCOUNTS_PATH) and os.path.getsize(ACCOUNTS_PATH) > 0:
    with open(ACCOUNTS_PATH, "r") as file:
        for line in file:
            if ":" in line:
                channel_name, stream_key = line.strip().split(":", 1)
                ACCOUNTS[channel_name.strip()] = stream_key.strip()
    
    if ACCOUNTS:
        print(f"\n{Fore.YELLOW}[BOT]{Fore.WHITE} Canais disponíveis:")
        channel_names = list(ACCOUNTS.keys())
        for idx, channel in enumerate(channel_names, 1):
            print(f"{Fore.YELLOW}[{idx}]{Fore.WHITE} {channel}")
        
        while True:
            print(f"\n{Fore.YELLOW}[BOT]{Fore.WHITE} Digite os números dos canais que deseja usar (ex: 1,3,5) ou 'all' para usar todos:{Fore.RESET}")
            selection = questionary.text(
                "",
                style=custom_style
            ).ask()
            
            if selection.lower() == 'all':
                selected_channels = channel_names
                break
            
            try:
                selected_indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
                
                if any(idx < 0 or idx >= len(channel_names) for idx in selected_indices):
                    print(f"{Fore.LIGHTRED_EX}[BOT]{Fore.WHITE} Número inválido! Use números entre 1 e {len(channel_names)}{Fore.RESET}")
                    continue
                    
                selected_channels = [channel_names[idx] for idx in selected_indices]
                break
                
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}[BOT]{Fore.WHITE} Formato inválido! Use números separados por vírgula (ex: 1,3,5){Fore.RESET}")
                continue
        
        selected_accounts = {channel: ACCOUNTS[channel] for channel in selected_channels}
        ACCOUNTS = selected_accounts
                
        print(f"\n{Fore.YELLOW}[BOT]{Fore.WHITE} Canais selecionados:")
        for idx, channel in enumerate(ACCOUNTS.keys(), 1):
            print(f"{Fore.YELLOW}[{idx}]{Fore.WHITE} {channel}")
    else:
        print(f"{Fore.LIGHTRED_EX}[BOT]{Fore.WHITE} Formato inválido no arquivo! Use o formato 'nome_canal:chave_stream' em cada linha{Fore.RESET}")
        time.sleep(error_sleep_time)
        sys.exit(-1)
                
else:
    print(f"{Fore.LIGHTRED_EX}[BOT]{Fore.WHITE} Arquivo {ACCOUNTS_PATH} não encontrado ou vazio!{Fore.RESET}")
    print(f"{Fore.LIGHTRED_EX}[BOT]{Fore.WHITE} Crie o arquivo e adicione seus canais no formato 'nome_canal:chave_stream', um por linha.{Fore.RESET}")
    time.sleep(error_sleep_time)
    sys.exit(-1)

videos_to_stream = choose_files()
if not videos_to_stream:
    print(f"{Fore.LIGHTRED_EX}[BOT] Nenhum vídeo selecionado. O programa será encerrado em 5 segundos...{Fore.RESET}\n\n")
    time.sleep(5)
    sys.exit(-1)

# Mensagens do seletor de GPU e qualidade
gpu = questionary.select(
    message="Select your GPU",
    choices=[
        "None",
        "NVIDIA", 
        "AMD"
    ],
    qmark="[BOT]",  # Usa apenas [BOT] sem códigos de cor
    style=custom_style
).ask()

quality = questionary.select(
    message="Choose video quality",
    choices=[
        "160",
        "360", 
        "480",
        "720",
        "1080"
    ],
    qmark="[BOT]",  # Usa apenas [BOT] sem códigos de cor
    style=custom_style
).ask()

# Substitua a criação do MenuManager por:
interface = InterfaceManager()

# Adiciona os canais ao MenuManager
for channel_name in ACCOUNTS:
    interface.initialize_channel(channel_name)  # Usa o nome do canal para exibição

try:
    # Distribui os vídeos entre as contas
    video_distribution = distribute_videos(videos_to_stream, list(ACCOUNTS.keys()))
    
    # Inicia as streams em threads separadas para não bloquear o menu
    processes = []
    for channel_name, video in video_distribution.items():
        interface.start_channel(channel_name)
        process = threading.Thread(
            target=start_streaming,
            args=(video, [ACCOUNTS[channel_name]], quality, DEBUG_MODE, gpu)  # Usa a chave correspondente ao canal
        )
        process.daemon = True
        process.start()
        processes.append(process)
    
    # Loop principal para manter o menu atualizado
    start_time = time.time()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        interface.draw_menu()
        time.sleep(1)

except KeyboardInterrupt:
    stop_streaming()
    print(f"\n{Fore.LIGHTRED_EX}[BOT]{Fore.WHITE} Streaming interrompido pelo usuário{Fore.RESET}")
except Exception as e:
    print(f"\n{Fore.LIGHTRED_EX}[BOT]{Fore.WHITE} Erro: {str(e)}{Fore.RESET}")
    stop_streaming()
