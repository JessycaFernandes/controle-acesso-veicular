from plyer import filechooser
#Usa essa biblioteca para escolher um arquivo do notebook
from kivy.animation import Animation
from kivy.uix.widget import Widget

import os
# Import Serve para trazer funcionalidade de outros módulos, os trabalha com pastas e arquivos
import sys
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
#Permite acessar informações do sistema e do interpretador do python
import cv2
# Essa biblioteca é responsável por abrir a câmera 
import threading
#Permite execuitar tarefas paralelas ao mesmo tempo


# importa o sistema de configuração inteiro do kivy
from kivy.config import Config
#Configura o tamanho da janela 
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '750')
#IMpedee o usuário de alterar o tamanho da janela
Config.set('graphics', 'resizable', False)



from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
#screen manager é o que controla a tela, screen representa um tela
from kivy.clock import Clock
#Representa o tempo
from kivy.graphics.texture import Texture
#Permite transformar uma imagem OPencv em uma imagem exibida no kivy



# Importa as funções do banco de dados e OCR
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from banco.banco import buscar_motoristas, registrar_acesso, criar_banco
# função para buscar motorista
from ocr.leitor_placa import ler_placa

PASTA = os.path.dirname(os.path.abspath(__file__))

class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.rodando = False

    def on_enter(self):
        # Quando entrar na tela, liga a câmera
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            self.ids.label_placa.text= 'X Câmera não encontrada!'
            return
        self.rodando = True
        Clock.schedule_interval(self.atualizar_camera, 1/30)  # 30fps

        
        
        
    def animar_scan(self):
        self.scan_direcao = 1
        self.scan_pos = 0.05
        Clock.schedule_interval(self.atualizar_scan, 1/30)

    def atualizar_scan(self, dt):
        velocidade = 0.012
        self.scan_pos += velocidade * self.scan_direcao

        if self.scan_pos >= 0.95:
            self.scan_pos = 0.95
            self.scan_direcao = -1
        elif self.scan_pos <= 0.05:
            self.scan_pos = 0.05
            self.scan_direcao = 1

        self.ids.linha_scan.pos_hint = {'center_x': 0.5, 'top': self.scan_pos + 0.05}
        
    def on_leave(self):
        # Quando sair da tela, desliga a câmera
        self.rodando = False
        Clock.unschedule(self.atualizar_camera)
        if self.camera:
            self.camera.release()

    def atualizar_camera(self, dt):
        # Captura frame e exibe na tela
        ret, frame = self.camera.read()
        if ret:
            # Converte pra formato que o Kivy entende
            frame = cv2.flip(frame, 0)
            buf = frame.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.ids.camera_view.texture = texture

    def capturar_placa(self):
        #Inicia a animação da linha do scan
        self.animar_scan()
        
        # Captura o frame atual e manda pro OCR
        ret, frame = self.camera.read()
        if not ret:
            self.ids.label_placa.text = 'Erro ao capturar imagem'
            return

        # Salva em pasta temporária do sistema, sem acentos no caminho
        import tempfile
        caminho_temp = os.path.join(tempfile.gettempdir(), 'frame_temp.jpg')
        sucesso = cv2.imwrite(caminho_temp, frame)

        if not sucesso:
            self.ids.label_placa.text = 'Erro ao salvar imagem'
            return

        # Roda o OCR em thread separada pra não travar a interface
        threading.Thread(target=self.processar_placa, args=(caminho_temp,)).start()

    def processar_placa(self, caminho_imagem):
        Clock.schedule_once(lambda dt: self.ids.label_placa.__setattr__('text', 'Lendo placa...'))
    
        placa = ler_placa(caminho_imagem)
    
        Clock.schedule_once(lambda dt: self.finalizar_leitura(placa))

    def finalizar_leitura(self, placa):
        #Para a animação de ascan
        Clock.unschedule(self.atualizar_scan)
        if placa is None:
            self.ids.label_placa.text = 'Placa não reconhecida'
            return

        self.ids.label_placa.text = f'Placa lida: {placa}'

        resultado = buscar_motoristas(placa)

        if resultado:
            matricula, nome, setor, ativa = resultado
            if ativa:
                registrar_acesso(placa, 'LIBERADO')
                tela = self.manager.get_screen('liberado')
                tela.ids.label_nome.text = f'Nome: {nome}'
                tela.ids.label_setor.text = f'Setor: {setor}'
                tela.ids.label_matricula.text = f'Matrícula: {matricula}'
                self.manager.current = 'liberado'
            else:
                registrar_acesso(placa, 'NEGADO', 'Matrícula inativa')
                tela = self.manager.get_screen('negado')
                tela.ids.label_placa_negado.text = f'Placa: {placa}'
                tela.ids.label_nome_negado.text = f'Nome: {nome}'
                tela.ids.label_matricula_negado.text = f'Matricula: {matricula}'
                tela.ids.label_motivo_negado.text = 'Matrícula inativa'
                self.manager.current = 'negado'
        else:
            registrar_acesso(placa, 'NEGADO', 'Placa não cadastrada')
            tela = self.manager.get_screen('negado')
            tela.ids.label_placa_negado.text = f'Placa: {placa}'
            tela.ids.label_nome_negado.text = ''
            tela.ids.label_matricula_negado.text = ''
            tela.ids.label_motivo_negado.text = 'Placa não cadastrada no sitema' 
            self.manager.current = 'negado'

    def testar_imagem(self):
        #abre o seletor de arquivos do sistema
        filechooser.open_file(
            on_selection=self.imagem_selecionada,
            filters=[("Imagens", "*.png", "*.jpg", "*.jpeg", "*.webp")]
        )
        
    def imagem_selecionada(self, selecao):
        if not selecao:
            return #usuário cancelou
        
        caminho_imagem = selecao[0]
        threading.Thread(target=self.processar_placa, args=(caminho_imagem,)).start()
# Tela que aparece quando o acesso é liberado
class TelaAcessoLiberado(Screen):
    pass

# Tela que aparece quando o acesso é negado
class TelaAcessoNegado(Screen):
    pass

# Gerenciador de telas
class GerenciadorTelas(ScreenManager):
    pass

# Classe principal do app
class ControleAcessoApp(App):
    def build(self):
        criar_banco()
        kv_path = os.path.join(PASTA, 'controle_acesso.kv')
        Builder.load_file(kv_path)
        sm = GerenciadorTelas()
        sm.add_widget(TelaPrincipal(name='principal'))
        sm.add_widget(TelaAcessoLiberado(name='liberado'))
        sm.add_widget(TelaAcessoNegado(name='negado'))
        sm.current = 'principal'
        return sm

if __name__ == '__main__':
    ControleAcessoApp().run()