from PIL import Image
import os

img_path = r'c:\Users\MySide - User\Documents\chrome-audio-converter-main\YoutubeAudioConverter\yt_icon_white_digital.png'
icon_path = r'c:\Users\MySide - User\Documents\chrome-audio-converter-main\YoutubeAudioConverter\icon.ico'

if os.path.exists(img_path):
    img = Image.open(img_path)
    # Save as ICO with multiple sizes for better compatibility
    img.save(icon_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Ícone criado com sucesso em: {icon_path}")
else:
    print("Imagem não encontrada.")
