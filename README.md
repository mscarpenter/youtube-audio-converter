# Youtube Audio Converter

Uma ferramenta poderosa e intuitiva para baixar áudio do YouTube na melhor qualidade disponível, convertendo automaticamente para MP3 (320kbps) ou WAV (Lossless).

Possui uma interface gráfica moderna baseada em CustomTkinter e suporte para linha de comando.

---

## Funcionalidades
- **Alta Qualidade**: Baixa o melhor stream de áudio disponível.
- **Formatos Suportados**: MP3 (320kbps) ou WAV (sem perda de fidelidade).
- **Interface Moderna**: GUI responsiva e amigável.
- **Processamento em Segundo Plano**: Baixe áudios sem travar a interface.
- **Pasta Organizada**: Salva automaticamente em C:\Users\MySide - User\Music\Youtube Converter.

---

## Download (Para Não-Desenvolvedores)
Se você não é desenvolvedor e quer apenas usar o programa, não precisa instalar o Python:
1. Vá na aba [**Releases**](https://github.com/mscarpenter/youtube-audio-converter/releases) (no lado direito).
2. Baixe o arquivo `YT Audio.exe`.
3. Basta abrir e usar! (O FFmpeg já está embutido no executável).

---

## Pré-requisitos (Para Desenvolvedores)

### 1. Python e Dependências
Certifique-se de ter o Python 3.7+ instalado. Instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 2. FFmpeg
O FFmpeg é necessário para a conversão do áudio no modo de desenvolvimento.
- **Windows**:
  - Baixe em [ffmpeg.org](https://ffmpeg.org/download.html).
  - Ou instale via terminal: `winget install ffmpeg`.
  - **Dica**: Se você colocar o `ffmpeg.exe` na mesma pasta do script, ele será detectado automaticamente.

---

## Como Usar

### Interface Gráfica (GUI)
```bash
python app_gui.py
```

### Linha de Comando (CLI)
```bash
# Formato padrão (MP3)
python youtube_to_audio.py https://www.youtube.com/watch?v=VIDEO_ID

# Especificando WAV
python youtube_to_audio.py https://www.youtube.com/watch?v=VIDEO_ID wav
```

---

## Criando um Executável (.exe)
Se desejar gerar seu próprio executável:

1. Certifique-se de que o `ffmpeg.exe` está na pasta raiz.
2. Execute:
```bash
pyinstaller app_gui.spec
```

---

## Licença
Este projeto é para fins educacionais. Respeite os termos de serviço do YouTube.
