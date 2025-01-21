"""
Módulo responsável pela arte ASCII e elementos visuais do console.
Contém funções para exibição do logo e configurações de cores.
"""

from colorama import Fore, Style
import os

# Adicionando a variável colors que está sendo importada
# Cor padrão utilizada em todo o aplicativo
colors = Fore.LIGHTRED_EX

def bot_logo(logo_color=None):
    """
    Exibe o logo do bot no console com cores e formatação personalizadas.

    Args:
        logo_color (colorama.Fore, optional): Cor a ser utilizada no logo. 
            Se None, utiliza a cor padrão definida em colors.
    """
    # Se nenhuma cor for especificada, usa a cor padrão
    if logo_color is None:
        logo_color = colors
        
    # Exibe o logo do bot no console.
    largura_console = os.get_terminal_size().columns
    print(f"{Style.NORMAL}{logo_color}\n\n")
    print(f"{Style.NORMAL}╦  ╦ ╦╔╦╗╦╔╗╔╔═╗".center(largura_console))
    print(f"{Style.NORMAL}║  ║ ║║║║║║║║╠═╣".center(largura_console))
    print(f"{Style.NORMAL}╩═╝╚═╝╩ ╩╩╝╚╝╩ ╩".center(largura_console))

    print(f"{Style.NORMAL}{Fore.LIGHTWHITE_EX}            TWITCH MULTI STREAM{Fore.RESET}".center(largura_console))
    print(f"{Style.NORMAL}{Fore.LIGHTWHITE_EX}          ───────────────────────────────────────{Fore.RESET}".center(largura_console))
    print(f"{Style.NORMAL}{Fore.LIGHTWHITE_EX}                                 Made by: {logo_color}Velbots{Fore.RESET}{Fore.LIGHTWHITE_EX}  |  Version: {logo_color}1.0.0{Fore.RESET}".center(largura_console))
    print(f"{Style.NORMAL}{Fore.LIGHTWHITE_EX}          ───────────────────────────────────────{Fore.RESET}".center(largura_console))
