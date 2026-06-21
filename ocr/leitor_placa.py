import os
import re
import easyocr
import numpy as np
from PIL import Image

leitor = easyocr.Reader(['en'], gpu=False)

def ler_placa(caminho_imagem):
    img = Image.open(caminho_imagem).convert('RGB')
    img_array = np.array(img)
    
    resultado = leitor.readtext(img_array)
    
    textos = []
    for item in resultado:
        texto = item[1]
        textos.append(texto)
    
    texto_completo = ''.join(textos).upper().replace(' ', '')
    print(f'Texto detectado: {texto_completo}')
    
    def corrigir_placa(texto):
        correcoes = {
            'Z': '7',
            'O': '0',
            'I': '1',
            'S': '5',
        }
        
        texto_corrigido = ''
        for char in texto:
            texto_corrigido += correcoes.get(char, char)
        
        print(f'Texto corrigido: {texto_corrigido}')
        
        match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_corrigido)
        
        if match:
            return match.group()
        return None
    
    placa = corrigir_placa(texto_completo)
    
    if placa is None:
        match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_completo)
        if match:
            return match.group()
    
    return placa

if __name__ == '__main__':
    PASTA = os.path.dirname(os.path.abspath(__file__))
    imagem = os.path.join(PASTA, '..', 'assets', 'placa_teste.webp')
    
    placa = ler_placa(imagem)
    print(f'Placa detectada: {placa}')