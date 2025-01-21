import os
import time
from colorama import Fore, Style
from datetime import timedelta
import shutil
from modules.art import bot_logo, colors

selected_color = Fore.RED

class MenuManager:
    # Constantes de Layout
    CHANNEL_MENU_LAYOUT = {
        'channel_width': 49,       # Channel Name
        'time_width': 10,          # Runtime
        'status_width': 10         # Status
    }
    
    STATS_MENU_LAYOUT = {
        'channels_width': 26,      # Largura da coluna "Channels Imported"
        'runtime_width': 26,       # Largura da coluna "Total Runtime"
        'total_width': 85         # Largura total do menu de estatísticas
    }

    # Novas constantes para alinhamento do menu
    MENU_PADDING = {
        'total_width': 85,           # Largura total do menu
        'stats_section': {
            'width': 85,             # Largura da seção de estatísticas
            'column_width': 35,      # Largura de cada coluna
            'padding': 2,            # Padding interno
            'separator': 3           # Espaço entre colunas
        },
        'channels_section': {
            'width': 85,             # Largura da seção de canais
            'channel_width': 35,     # Largura da coluna do canal
            'time_width': 20,        # Largura da coluna de tempo
            'status_width': 20       # Largura da coluna de status
        }
    }
    
    STATUS_COLORS = {
        'Queued': Fore.YELLOW,
        'Streaming': Fore.GREEN,
        'Completed': Fore.BLUE,
        'Error': Fore.RED
    }

    def __init__(self):
        self.channels_status = {}
        self.start_times = {}
        self.last_update = time.time()
        self.update_interval = 1  # Atualiza a cada 1 segundo
        
        self._init_symbols()
        self._init_stats()
        self._calculate_widths()

    def _init_symbols(self):
        """Inicializa os símbolos Unicode do menu"""
        self.symbols = {
            'top_left': f"{Style.NORMAL}{Fore.RED}┌{Fore.RESET}",
            'top_right': f"{Style.NORMAL}{Fore.RED}┐{Fore.RESET}",
            'bottom_left': f"{Style.NORMAL}{Fore.RED}└{Fore.RESET}",
            'bottom_right': f"{Style.NORMAL}{Fore.RED}┘{Fore.RESET}",
            'horizontal': f"{Style.NORMAL}{Fore.RED}─{Fore.RESET}",
            'vertical': f"{Style.NORMAL}{Fore.RED}│{Fore.RESET}",
            'left_t': f"{Style.NORMAL}{Fore.RED}├{Fore.RESET}",
            'right_t': f"{Style.NORMAL}{Fore.RED}┤{Fore.RESET}",
            'top_t': f"{Style.NORMAL}{Fore.RED}┬{Fore.RESET}",
            'bottom_t': f"{Style.NORMAL}{Fore.RED}┴{Fore.RESET}",
            'cross': f"{Style.NORMAL}{Fore.RED}┼{Fore.RESET}"
        }

    def _init_stats(self):
        """Inicializa as estatísticas"""
        self.stats = {
            'channels_imported': 0,
            'start_time': time.time()
        }

    def _calculate_widths(self):
        """Calcula as larguras totais dos menus"""
        self.layout = self.CHANNEL_MENU_LAYOUT
        self.stats_layout = self.STATS_MENU_LAYOUT
        
        # Ajustando as larguras totais para serem iguais
        self.total_width = sum(self.layout.values()) + 10  # largura do menu de canais
        self.stats_total_width = self.total_width  # fazendo a largura do menu de stats igual
        
        # Ajustando as larguras individuais do menu de stats para preencher o espaço
        self.stats_layout['channels_width'] = (self.total_width - 15) // 2  # -15 para compensar bordas e padding
        self.stats_layout['runtime_width'] = (self.total_width - 15) // 2

    def format_elapsed_time(self, seconds):
        if seconds is None:
            return "0h 0m 0s"
        td = timedelta(seconds=int(seconds))
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        secs = td.seconds % 60
        return f"{hours}h {minutes}m {secs}s"

    def initialize_channel(self, channel):
        """Inicializa um novo canal"""
        self.channels_status[channel] = {
            'status': 'Queued'
        }
        self.start_times[channel] = None

    def start_channel(self, channel):
        """Inicia o processamento de um canal"""
        if channel in self.channels_status:
            self.channels_status[channel]['status'] = 'Streaming'
            self.start_times[channel] = time.time()

    def set_error(self, channel, error_message="Erro desconhecido"):
        """Define um canal como erro"""
        if channel in self.channels_status:
            self.channels_status[channel]['status'] = 'Error'

    def set_channel_complete(self, channel):
        """Marca um canal como completo"""
        if channel in self.channels_status:
            self.channels_status[channel]['status'] = 'Completed'

    def draw_menu(self):
        """Desenha o menu atualizado"""
        current_time = time.time()
        if current_time - self.last_update < self.update_interval:
            return
                
        os.system('cls' if os.name == 'nt' else 'clear')
        terminal_width = shutil.get_terminal_size().columns
        
        bot_logo(selected_color)
        
        # Atualiza estatísticas
        self.stats['channels_imported'] = len(self.channels_status)
        
        # Calcula padding para centralização
        padding = " " * ((terminal_width - self.total_width) // 2)
        
        # Primeira linha - Topo com junção
        top_line = (
            f"{self.symbols['top_left']}"
            f"{self.symbols['horizontal'] * ((self.total_width - 3) // 2)}"
            f"{self.symbols['top_t']}"
            f"{self.symbols['horizontal'] * ((self.total_width - 3) // 2)}"
            f"{self.symbols['top_right']}"
        )
        print(f"{padding}{top_line}")
        
        # Títulos
        stats_header = (
            f"{self.symbols['vertical']} "
            f"{'Channels Imported':<{(self.total_width - 15) // 2}}     "
            f"{self.symbols['vertical']} "
            f"{'Total Runtime':<{(self.total_width - 15) // 2}}     "
            f"{self.symbols['vertical']}"
        )
        print(f"{padding}{stats_header}")
        
        # Linha separadora do meio
        separator = (
            f"{self.symbols['left_t']}"
            f"{self.symbols['horizontal'] * ((self.total_width - 3) // 2)}"
            f"{self.symbols['cross']}"
            f"{self.symbols['horizontal'] * ((self.total_width - 3) // 2)}"
            f"{self.symbols['right_t']}"
        )
        print(f"{padding}{separator}")
        
        # Valores
        stats_values = (
            f"{self.symbols['vertical']} "
            f"{str(self.stats['channels_imported']):<{(self.total_width - 15) // 2}}     "
            f"{self.symbols['vertical']} "
            f"{self.format_elapsed_time(time.time() - self.stats['start_time']):<{(self.total_width - 15) // 2}}     "
            f"{self.symbols['vertical']}"
        )
        print(f"{padding}{stats_values}")
        
        # Linha inferior com junção
        bottom_line = (
            f"{self.symbols['bottom_left']}"
            f"{self.symbols['horizontal'] * ((self.total_width - 3) // 2)}"
            f"{self.symbols['bottom_t']}"
            f"{self.symbols['horizontal'] * ((self.total_width - 3) // 2)}"
            f"{self.symbols['bottom_right']}"
        )
        print(f"{padding}{bottom_line}")
        
        # Segundo Menu - Lista de Canais
        print(f"{padding}{self.symbols['top_left']}{self.symbols['horizontal'] * (self.total_width - 2)}{self.symbols['top_right']}")
        print(f"{padding}{self.symbols['vertical']} {'Channel':<{self.layout['channel_width']}} {self.symbols['vertical']} "
              f"{'Runtime':<{self.layout['time_width']}} {self.symbols['vertical']} "
              f"{'Status':<{self.layout['status_width']}} {self.symbols['vertical']}")
        print(f"{padding}{self.symbols['left_t']}{self.symbols['horizontal'] * (self.total_width - 2)}{self.symbols['right_t']}")

        # Lista de canais
        for channel in self.channels_status:
            stats = self.channels_status[channel]
            elapsed = time.time() - (self.start_times[channel] or time.time())
            elapsed_str = self.format_elapsed_time(elapsed if self.start_times[channel] else 0)
            status_color = self.STATUS_COLORS.get(stats['status'], '')
            
            print(f"{padding}{self.symbols['vertical']} {channel:<{self.layout['channel_width']}} {self.symbols['vertical']} "
                  f"{elapsed_str:<{self.layout['time_width']}} {self.symbols['vertical']} "
                  f"{status_color}{stats['status']:<{self.layout['status_width']}}{Fore.RESET} {self.symbols['vertical']}")
        
        # Rodapé do segundo menu
        print(f"{padding}{self.symbols['bottom_left']}{self.symbols['horizontal'] * (self.total_width - 2)}{self.symbols['bottom_right']}")
        
        self.last_update = current_time
