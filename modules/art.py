"""
Módulo responsável pela arte ASCII e elementos visuais do console.
Contém funções para exibição do logo e configurações de cores.
"""

from rich.console import Console
from rich.align import Align

console = Console()

def bot_logo():
    """
    Exibe o logo do bot no console usando Rich para formatação.
    """
    logo = """
[white bold]                       NIMBUS[/white bold]
[yellow] ────────────────────────────────────────────────[/yellow]
[white]       Made by: [bold yellow]Velbots[/bold yellow]  │  Version: [bold yellow]1.0.0[/bold yellow][/white]
[yellow] ────────────────────────────────────────────────[/yellow]"""

    console.print(Align.center(logo))