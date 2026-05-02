import customtkinter as ctk
import yt_dlp
import os
import threading
from tkinter import filedialog, messagebox

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def resource_path(self, relative_path):
        """ Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller """
        try:
            import sys
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)

    def __init__(self):
        super().__init__()

        self.title("Youtube Audio Converter")
        self.geometry("600x450")

        # Define o caminho do FFmpeg (embutido ou local)
        self.ffmpeg_path = self.resource_path("ffmpeg.exe")
        
        if not os.path.exists(self.ffmpeg_path):
            # Fallback para o caminho do sistema caso não esteja embutido ou local
            self.ffmpeg_path = "ffmpeg"

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Título
        self.label_title = ctk.CTkLabel(self, text="Youtube Audio Converter", font=ctk.CTkFont(size=24, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input URL
        self.entry_url = ctk.CTkEntry(self, placeholder_text="Cole a URL do YouTube aqui...", width=500)
        self.entry_url.grid(row=1, column=0, padx=20, pady=10)

        # Opções de Formato
        self.frame_options = ctk.CTkFrame(self)
        self.frame_options.grid(row=2, column=0, padx=20, pady=10)

        self.format_var = ctk.StringVar(value="mp3")
        self.radio_mp3 = ctk.CTkRadioButton(self.frame_options, text="MP3 (320kbps)", variable=self.format_var, value="mp3")
        self.radio_mp3.pack(side="left", padx=20, pady=10)
        
        self.radio_wav = ctk.CTkRadioButton(self.frame_options, text="WAV (Lossless)", variable=self.format_var, value="wav")
        self.radio_wav.pack(side="left", padx=20, pady=10)

        # Botão Download
        self.btn_download = ctk.CTkButton(self, text="Baixar e Converter", command=self.start_download_thread, font=ctk.CTkFont(weight="bold"))
        self.btn_download.grid(row=3, column=0, padx=20, pady=20)

        # Log de Status
        self.textbox_log = ctk.CTkTextbox(self, width=500, height=150)
        self.textbox_log.grid(row=4, column=0, padx=20, pady=(0, 20))
        self.textbox_log.insert("0.0", "Pronto para iniciar...\n")

    def log(self, message):
        self.textbox_log.insert("end", f"> {message}\n")
        self.textbox_log.see("end")

    def start_download_thread(self):
        url = self.entry_url.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL válida.")
            return
        
        self.btn_download.configure(state="disabled")
        self.log(f"Iniciando processo para: {url}")
        
        # Rodar em uma thread separada para não travar a interface
        thread = threading.Thread(target=self.download_logic, args=(url, self.format_var.get()))
        thread.start()

    def download_logic(self, url, fmt):
        try:
            # Pasta de destino
            output_dir = r'C:\Users\MySide - User\Music\Youtube Converter'
            
            # Cria a pasta se não existir
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            ydl_opts = {
                'format': 'bestaudio/best',
                'ffmpeg_location': self.ffmpeg_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': fmt,
                    'preferredquality': '320' if fmt == 'mp3' else None,
                }],
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.log(f"Baixando áudio...")
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Audio')
                self.log(f"Sucesso: {title}.{fmt}")
                
            messagebox.showinfo("Sucesso", f"Download concluído:\n{title}.{fmt}")
        
        except Exception as e:
            self.log(f"ERRO: {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        
        finally:
            self.btn_download.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
