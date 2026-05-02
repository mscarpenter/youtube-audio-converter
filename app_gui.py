import customtkinter as ctk
import yt_dlp
import os
import threading
import json
from tkinter import filedialog, messagebox
from PIL import Image

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
        self.geometry("900x600")

        # Configurações padrão
        self.settings_file = os.path.join(os.path.expanduser("~"), ".yt_audio_converter_settings.json")
        self.load_settings()

        # Define os caminhos dos recursos
        self.ffmpeg_path = self.resource_path("ffmpeg.exe")
        self.logo_path = self.resource_path("yt_icon_white_digital.png")
        
        if not os.path.exists(self.ffmpeg_path):
            self.ffmpeg_path = "ffmpeg"

        # Estado da Sidebar
        self.sidebar_expanded = False

        # Configuração do Grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---- MENU LATERAL (Sidebar) ----
        self.sidebar_frame = ctk.CTkFrame(self, width=60, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False) # Mantém a largura fixa
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Botão Hambúrguer (Toggle)
        self.btn_toggle = ctk.CTkButton(self.sidebar_frame, text="≡", width=40, height=40,
                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                       hover_color=("gray70", "gray30"), font=ctk.CTkFont(size=24),
                                       command=self.toggle_sidebar)
        self.btn_toggle.grid(row=0, column=0, padx=10, pady=20)

        # Botões de Navegação (começam sem texto)
        self.btn_nav_converter = ctk.CTkButton(self.sidebar_frame, text="", width=40,
                                              fg_color="transparent", text_color=("gray10", "gray90"), 
                                              hover_color=("gray70", "gray30"), anchor="w",
                                              command=self.show_converter)
        self.btn_nav_converter.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.btn_nav_settings = ctk.CTkButton(self.sidebar_frame, text="", width=40,
                                             fg_color="transparent", text_color=("gray10", "gray90"), 
                                             hover_color=("gray70", "gray30"), anchor="w",
                                             command=self.show_settings)
        self.btn_nav_settings.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.btn_nav_about = ctk.CTkButton(self.sidebar_frame, text="", width=40,
                                          fg_color="transparent", text_color=("gray10", "gray90"), 
                                          hover_color=("gray70", "gray30"), anchor="w",
                                          command=self.show_about)
        self.btn_nav_about.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # ---- ÁREA DE CONTEÚDO ----
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.frame_converter = self.create_converter_frame()
        self.frame_settings = self.create_settings_frame()
        self.frame_about = self.create_about_frame()

        self.show_converter()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            # Recolher
            self.sidebar_frame.configure(width=60)
            self.btn_nav_converter.configure(text="", anchor="center")
            self.btn_nav_settings.configure(text="", anchor="center")
            self.btn_nav_about.configure(text="", anchor="center")
            self.sidebar_expanded = False
        else:
            # Expandir
            self.sidebar_frame.configure(width=200)
            self.btn_nav_converter.configure(text="Conversor", anchor="w")
            self.btn_nav_settings.configure(text="Configurações", anchor="w")
            self.btn_nav_about.configure(text="Sobre & Ajuda", anchor="w")
            self.sidebar_expanded = True

    def load_settings(self):
        default_dir = os.path.join(os.path.expanduser("~"), "Music", "Youtube Audio")
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self.settings = json.load(f)
            except:
                self.settings = {"output_dir": default_dir}
        else:
            self.settings = {"output_dir": default_dir}
        
        if not os.path.exists(self.settings["output_dir"]):
            try: os.makedirs(self.settings["output_dir"])
            except: pass

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def show_converter(self):
        self.select_frame(self.frame_converter)
        self.btn_nav_converter.configure(fg_color=("gray75", "gray25"))
        self.btn_nav_settings.configure(fg_color="transparent")
        self.btn_nav_about.configure(fg_color="transparent")

    def show_settings(self):
        self.select_frame(self.frame_settings)
        self.btn_nav_converter.configure(fg_color="transparent")
        self.btn_nav_settings.configure(fg_color=("gray75", "gray25"))
        self.btn_nav_about.configure(fg_color="transparent")

    def show_about(self):
        self.select_frame(self.frame_about)
        self.btn_nav_converter.configure(fg_color="transparent")
        self.btn_nav_settings.configure(fg_color="transparent")
        self.btn_nav_about.configure(fg_color=("gray75", "gray25"))

    def select_frame(self, frame):
        self.frame_converter.grid_forget()
        self.frame_settings.grid_forget()
        self.frame_about.grid_forget()
        frame.grid(row=0, column=0, sticky="nsew")

    def create_converter_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)

        if os.path.exists(self.logo_path):
            logo_image = ctk.CTkImage(light_image=Image.open(self.logo_path),
                                     dark_image=Image.open(self.logo_path),
                                     size=(120, 85))
            ctk.CTkLabel(frame, image=logo_image, text="").grid(row=0, column=0, padx=20, pady=(40, 0))

        ctk.CTkLabel(frame, text="Youtube Audio Converter", font=ctk.CTkFont(size=28, weight="bold")).grid(row=1, column=0, padx=20, pady=(10, 30))

        self.entry_url = ctk.CTkEntry(frame, placeholder_text="Cole a URL do YouTube aqui...", width=550, height=40)
        self.entry_url.grid(row=2, column=0, padx=20, pady=10)

        self.frame_options = ctk.CTkFrame(frame, fg_color="transparent")
        self.frame_options.grid(row=3, column=0, padx=20, pady=10)

        self.format_var = ctk.StringVar(value="mp3")
        ctk.CTkRadioButton(self.frame_options, text="MP3 (320kbps)", variable=self.format_var, value="mp3").pack(side="left", padx=20)
        ctk.CTkRadioButton(self.frame_options, text="WAV (Lossless)", variable=self.format_var, value="wav").pack(side="left", padx=20)

        self.btn_download = ctk.CTkButton(frame, text="Converter e Baixar", width=200, height=45,
                                         command=self.start_download_thread, font=ctk.CTkFont(size=16, weight="bold"))
        self.btn_download.grid(row=4, column=0, padx=20, pady=30)

        self.textbox_log = ctk.CTkTextbox(frame, width=550, height=180)
        self.textbox_log.grid(row=5, column=0, padx=20, pady=(0, 20))
        self.textbox_log.insert("0.0", "Pronto para iniciar...\n")
        
        return frame

    def create_settings_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(frame, text="Configurações", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, padx=20, pady=40)

        path_frame = ctk.CTkFrame(frame)
        path_frame.grid(row=1, column=0, padx=40, pady=10, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(path_frame, text="Pasta de Destino Padrão:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.entry_path = ctk.CTkEntry(path_frame, width=400)
        self.entry_path.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.entry_path.insert(0, self.settings["output_dir"])
        self.entry_path.configure(state="readonly")

        ctk.CTkButton(path_frame, text="Alterar Pasta", command=self.browse_folder).grid(row=1, column=1, padx=20, pady=(0, 20))
        return frame

    def create_about_frame(self):
        frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(frame, text="Sobre & Ajuda", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, padx=20, pady=40)

        about_text = (
            "YT Audio Converter v1.1\n\n"
            "Desenvolvido por: mscarpenter\n"
            "Uma ferramenta eficiente para extrair áudio de vídeos do YouTube "
            "com a máxima qualidade disponível.\n\n"
            "Melhores Práticas:\n"
            "• Use apenas para conteúdos autorizados ou de domínio público.\n"
            "• Respeite os direitos dos criadores de conteúdo.\n"
            "• O formato WAV mantém a fidelidade total, enquanto o MP3 economiza espaço."
        )
        ctk.CTkLabel(frame, text=about_text, justify="left", wraplength=500, font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=40, pady=10)
        return frame

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.settings["output_dir"])
        if folder:
            self.settings["output_dir"] = folder
            self.entry_path.configure(state="normal")
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, folder)
            self.entry_path.configure(state="readonly")
            self.save_settings()
            self.log(f"Nova pasta de destino: {folder}")

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
        thread = threading.Thread(target=self.download_logic, args=(url, self.format_var.get()))
        thread.start()

    def download_logic(self, url, fmt):
        try:
            output_dir = self.settings["output_dir"]
            if not os.path.exists(output_dir): os.makedirs(output_dir)

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
            messagebox.showinfo("Sucesso", f"Concluído: {title}.{fmt}\nSalvo em: {output_dir}")
        except Exception as e:
            self.log(f"ERRO: {str(e)}")
            messagebox.showerror("Erro", f"Erro: {e}")
        finally:
            self.btn_download.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
