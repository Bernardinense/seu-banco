import base64

def imagem_para_base64(caminho_imagem: str) -> str:
    """Converte uma imagem para uma string base64."""
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
    
    