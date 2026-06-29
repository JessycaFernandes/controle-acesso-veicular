#Permite que o python interaja com o sitema opercional, tipo qual pasta, arquivos
import os
#Procura padrões dentro de textos
import re
#utiliza a IA para reconhecer textos em imagens
import easyocr
#organiza os pixels das img para matrizes e arrays
import numpy as np
#Importa a classe Image da biblioteca Pillow, serve para abrir e manipular img
from PIL import Image

leitor = easyocr.Reader(['en'], gpu=False)

#Cria a função ler placa e ercebe um parâmetro , que é o caminho da img
def ler_placa(caminho_imagem):
    # Essa linha na parte" image.open" abre a img, e converte ela para o formato rgb
    img = Image.open(caminho_imagem).convert('RGB')
    img_array = np.array(img)
    
    #dentro de resultados, tem as coordenadas, o texto e o nível de precisão ou confiança
    resultado = leitor.readtext(img_array)
    
    # aqui é armazenado todos os textos ness lista
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
        
        #padrão mercosul
        match = re.search(r'[A-Z]{3}[0-9][A-Z0-9][0-9]{2}', texto_corrigido)
        
        # se encontrou uma placa, retorna o etxto encontrado
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