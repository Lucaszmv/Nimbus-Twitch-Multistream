from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.box import SQUARE
from rich.align import Align
from datetime import datetime
from modules.art import bot_logo
import time
import os

console = Console()

class InterfaceManager:
    def __init__(self):
        self.channels_status = {}
        self.start_times = {}
        self.last_update = time.time()
        self.update_interval = 1
        self.start_time = datetime.now()

    def format_elapsed_time(self, start_time):
        if not start_time:
            return "0h 0m 0s"
        delta = datetime.now() - start_time
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        seconds = delta.seconds % 60
        return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"

    def display_header(self):
        bot_logo()

    def create_stats_table(self):
        runtime = self.format_elapsed_time(self.start_time)
        
        stats = Table(
            box=SQUARE,
            border_style="yellow",
            width=35,
            padding=(0, 2),
            show_header=True,
            header_style="white"
        )
        
        stats.add_column("CHANNELS", justify="center", style="white", width=15)
        stats.add_column("RUNTIME", justify="center", style="white", width=15)
        
        stats.add_row(
            str(len(self.channels_status)),
            runtime
        )
        
        return stats

    def create_status_table(self):
        table = Table(
            box=SQUARE,
            border_style="yellow",
            width=60,
            padding=(0, 2),
            show_lines=True,
            header_style="white"
        )
        
        table.add_column("CHANNEL", style="white", width=30, justify="center")
        table.add_column("STATUS", style="white", width=20, justify="center")
        table.add_column("RUNTIME", style="white", width=20, justify="center")
        
        status_colors = {
            "QUEUED": "yellow",
            "STREAMING": "green",
            "COMPLETED": "blue",
            "ERROR": "red"
        }
        
        for channel, data in self.channels_status.items():
            status = data['status'].upper()
            status_color = status_colors.get(status, "white")
            status_symbol = "●" if status != "ERROR" else "○"
            
            table.add_row(
                channel,
                f"[{status_color}]{status_symbol} {status}[/{status_color}]",
                self.format_elapsed_time(self.start_times.get(channel))
            )
        
        return table

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
            self.start_times[channel] = datetime.now()

    def set_error(self, channel):
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
                
        console.clear()
        self.display_header()
        
        stats_table = self.create_stats_table()
        status_table = self.create_status_table()
        
        console.print(Align.center(stats_table))
        console.print(Align.center(status_table))
        console.print("")
        
        self.last_update = current_time 