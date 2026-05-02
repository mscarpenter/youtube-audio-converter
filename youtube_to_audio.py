import yt_dlp
import sys
import os

def download_audio(url, format_type='mp3'):
    """
    Downloads audio from a YouTube URL and converts it to the specified format (mp3 or wav)
    at the best possible quality.
    """
    if format_type not in ['mp3', 'wav']:
        print("Erro: Formato inválido. Use 'mp3' ou 'wav'.")
        return

    # Tenta encontrar o ffmpeg no mesmo diretório do script ou no PATH
    ffmpeg_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ffmpeg.exe")
    
    if not os.path.exists(ffmpeg_exe):
        ffmpeg_exe = 'ffmpeg' # Fallback para o PATH do sistema

    # Configuration for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_exe,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_type,
            'preferredquality': '320' if format_type == 'mp3' else None, # 320kbps for MP3
        }],
        'outtmpl': '%(title)s.%(ext)s', # Save with video title
        'quiet': False,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"--- Iniciando download e conversão para {format_type.upper()} ---")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Adjust filename extension for the message
            base, _ = os.path.splitext(filename)
            final_filename = f"{base}.{format_type}"
            
            print(f"\n--- Sucesso! ---")
            print(f"Arquivo salvo como: {final_filename}")
            
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um problema: {e}")
        if "ffmpeg" in str(e).lower():
            print("\nAVISO CRÍTICO: O 'ffmpeg' não foi detectado.")
            print("Para realizar a conversão de áudio, você DEVE ter o ffmpeg instalado e configurado no PATH do seu sistema.")
            print("Baixe em: https://ffmpeg.org/download.html")

if __name__ == "__main__":
    # If arguments are provided via command line
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        fmt = sys.argv[2].lower() if len(sys.argv) > 2 else 'mp3'
        download_audio(video_url, fmt)
    else:
        # Interactive mode if no arguments
        print("--- Youtube Audio Converter (MP3/WAV) ---")
        url = input("Cole a URL do vídeo do YouTube: ").strip()
        if not url:
            print("URL inválida.")
            sys.exit(1)
            
        escolha = input("Escolha o formato (1 para MP3, 2 para WAV) [Padrão: 1]: ").strip()
        formato = 'wav' if escolha == '2' else 'mp3'
        
        download_audio(url, formato)
