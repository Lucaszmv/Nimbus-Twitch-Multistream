import os
import logging
from datetime import datetime
from colorama import Fore

class Logger:
    def __init__(self, stream_key):
        # Cria o diretório de logs se não existir
        self.logs_dir = "logs"
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
            
        # Configura o logger
        self.logger = logging.getLogger(stream_key)
        self.logger.setLevel(logging.DEBUG)
        
        # Nome do arquivo de log baseado na stream key
        nome_arquivo = f"{stream_key}.log"
        caminho_arquivo = os.path.join(self.logs_dir, nome_arquivo)
        
        # Limpa handlers existentes
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Configura o handler de arquivo
        file_handler = logging.FileHandler(caminho_arquivo, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Adiciona o handler ao logger
        self.logger.addHandler(file_handler)
    
    def debug(self, mensagem, print_terminal=False):
        """Registra uma mensagem de debug"""
        self.logger.debug(mensagem)
        if print_terminal:
            print(f"{Fore.CYAN}[DEBUG] {mensagem}{Fore.RESET}")
    
    def info(self, mensagem, print_terminal=False):
        """Registra uma mensagem de informação"""
        self.logger.info(mensagem)
        if print_terminal and not mensagem.startswith("FFmpeg:"):
            print(f"{Fore.WHITE}[LOG] {mensagem}{Fore.RESET}")
    
    def error(self, mensagem, print_terminal=False):
        """Registra uma mensagem de erro"""
        self.logger.error(mensagem)
        if print_terminal:
            print(f"{Fore.RED}[ERROR] {mensagem}{Fore.RESET}")
    
    def warning(self, mensagem, print_terminal=False):
        """Registra uma mensagem de aviso"""
        self.logger.warning(mensagem)
        if print_terminal:
            print(f"{Fore.YELLOW}[WARNING] {mensagem}{Fore.RESET}") 