import mimetypes
from pathlib import Path

def gerar_imagem_gemini(caminho_imagem):
    caminho = Path(caminho_imagem)
    tipo_mime, _ = mimetypes.guess_type(caminho.name)

    arquivo_imagem = {
        "mime_type": tipo_mime or "image/jpeg",
        "data": caminho.read_bytes(),
    }

    print(f"Imagem preparada para envio: {caminho.name}")

    return arquivo_imagem
