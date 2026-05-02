# YouTube Audio Downloader Pro 🎵

Uma ferramenta poderosa e intuitiva para baixar áudio do YouTube na melhor qualidade disponível, convertendo automaticamente para **MP3 (320kbps)** ou **WAV (Lossless)**.

Possui uma interface gráfica moderna baseada em `CustomTkinter` e suporte para linha de comando.

---

## ✨ Funcionalidades
- **Alta Qualidade**: Baixa o melhor stream de áudio disponível.
- **Formatos Suportados**: MP3 (320kbps) ou WAV (sem perda de fidelidade).
- **Interface Moderna**: GUI responsiva e amigável.
- **Processamento em Segundo Plano**: Baixe áudios sem travar a interface.
- **Pasta Organizada**: Salva automaticamente em `C:\Users\MySide - User\Music\Youtube Converter`.

---

## 🛠️ Pré-requisitos

### 1. Python e Dependências
Certifique-se de ter o Python 3.7+ instalado. Instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 2. FFmpeg (Essencial)
O FFmpeg é necessário para a conversão do áudio.
- **Windows**:
  - Baixe em [ffmpeg.org](https://ffmpeg.org/download.html).
  - Ou instale via terminal: `winget install ffmpeg`.
  - **Dica**: Se você colocar o `ffmpeg.exe` na mesma pasta do script, ele será detectado automaticamente.

---

## 🚀 Como Usar

### Interface Gráfica (GUI)
Para uma experiência visual:
```bash
python app_gui.py
```

### Linha de Comando (CLI)
Para uso rápido via terminal:
```bash
# Formato padrão (MP3)
python youtube_to_audio.py https://www.youtube.com/watch?v=VIDEO_ID

# Especificando WAV
python youtube_to_audio.py https://www.youtube.com/watch?v=VIDEO_ID wav
```

---

## 📦 Criando um Executável (.exe)
Se desejar transformar o projeto em um executável para Windows:

1. Certifique-se de que o `ffmpeg.exe` está na pasta raiz.
2. Execute o PyInstaller usando o arquivo `.spec` já configurado:
```bash
pyinstaller app_gui.spec
```
O executável será gerado na pasta `dist/`.

---

## 📝 Licença
Este projeto é para fins educacionais. Respeite os termos de serviço do YouTube.
