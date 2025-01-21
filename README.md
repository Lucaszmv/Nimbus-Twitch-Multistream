# 🌩️ Nimbus Multistream

Ferramenta para transmitir múltiplos streams para Twitch simultaneamente.

## ✨ Características

- 📺 Suporte para múltiplos canais simultâneos
- 🖥️ Interface de console interativa
- 🎮 Suporte para diferentes qualidades de stream (160p até 1080p)
- 🚀 Suporte para aceleração de hardware (NVIDIA e AMD)
- 📝 Sistema de logs detalhado
- 📊 Monitoramento em tempo real dos streams

## 📋 Requisitos

- 🐍 Python 3.8 ou superior
- 🎬 FFmpeg
- 📦 Poetry (gerenciador de dependências)

## 🚀 Instalação

### 1. Clone o repositório:

```bash
git clone https://github.com/Lucaszmv/Nimbus-Multistream.git
cd Nimbus-Multistream
```

### 2. Instale o FFmpeg:

#### Windows:
Método Automático (PowerShell):
```powershell
# Cria diretório ffmpeg se não existir
New-Item -ItemType Directory -Force -Path "ffmpeg\bin"

# Download do FFmpeg
Invoke-WebRequest -Uri "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" -OutFile "ffmpeg-temp.zip"

# Extrai o arquivo
Expand-Archive "ffmpeg-temp.zip" -DestinationPath "ffmpeg-temp"

# Move o ffmpeg.exe para a pasta correta
Move-Item "ffmpeg-temp\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe" "ffmpeg\bin\ffmpeg.exe" -Force

# Limpa arquivos temporários
Remove-Item "ffmpeg-temp.zip"
Remove-Item "ffmpeg-temp" -Recurse
```

Método Manual:
1. Baixe o FFmpeg de [https://github.com/BtbN/FFmpeg-Builds/releases](https://github.com/BtbN/FFmpeg-Builds/releases)
2. Extraia o arquivo baixado
3. Crie uma pasta `ffmpeg/bin` no diretório do projeto
4. Copie o `ffmpeg.exe` para a pasta `ffmpeg/bin`

#### Linux:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

#### macOS:
```bash
# Usando Homebrew
brew install ffmpeg
```

### 3. Instale as dependências Python:

```bash
poetry install
```

### 4. Configure suas chaves de stream:

1. Crie um arquivo `channels_keys.txt`
2. Adicione seus canais e chaves no formato:
```
nome_canal:chave_stream
```
Exemplo:
```
canal1:live_123456789_abcdefghijklmnopqrst
canal2:live_987654321_uvwxyzabcdefghijklm
```

## 🎮 Uso

1. Execute o programa:

```bash
poetry run python main.py
```

2. 📂 Selecione os vídeos que deseja transmitir
3. 💻 Escolha sua GPU (None, NVIDIA ou AMD)
4. 📊 Selecione a qualidade do stream
5. 📺 Monitore seus streams através da interface

## 🔧 Configuração Avançada

- Suporte para múltiplas GPUs
- Configuração de bitrate personalizado
- Ajustes de qualidade de áudio
- Personalização de layouts de stream

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.