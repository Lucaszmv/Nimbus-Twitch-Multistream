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

1. Clone o repositório:

```bash
git clone https://github.com/Lucaszmv/Nimbus-Multistream.git
cd Nimbus-Multistream
```

2. Instale as dependências:

```bash
poetry install
```

3. Configure suas chaves de stream:

- 📄 Crie um arquivo `channels_keys.txt`
- 🔑 Adicione suas chaves de stream da Twitch, uma por linha

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