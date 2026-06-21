# SmartGate — Sistema de Controle de Acesso Veicular

Sistema de controle de acesso para portarias, desenvolvido como projeto de workshop sobre Python e Kivy. O sistema reconhece a placa de um veículo através de uma câmera, consulta um banco de dados de motoristas cadastrados e libera ou nega o acesso automaticamente.

## Como funciona

1. O carro chega na entrada e o porteiro aponta a câmera para a placa.
2. O sistema captura a imagem e usa OCR para reconhecer os caracteres.
3. A placa lida é consultada no banco de dados.
4. Se a matrícula estiver ativa, o sistema exibe os dados do motorista (nome, setor, matrícula) e libera o acesso.
5. Se a matrícula estiver inativa ou a placa não for encontrada, o sistema exibe uma mensagem de acesso negado.
6. Toda tentativa de acesso (liberada ou negada) é registrada com data e hora.

## Tecnologias utilizadas

- **Python 3.11**
- **Kivy** — interface gráfica
- **EasyOCR** — reconhecimento óptico de caracteres (OCR)
- **OpenCV** — captura de vídeo da webcam
- **SQLite** — banco de dados de motoristas e log de acessos
- **Pandas / openpyxl** — importação de cadastro via planilha Excel

## Estrutura do projeto

```
controle de acesso/
├── main.py                      # interface e lógica principal
├── controle_acesso.kv           # layout visual das telas
├── banco/
│   └── banco.py                 # criação do banco, consultas e log
├── ocr/
│   └── leitor_placa.py          # leitura e correção da placa via OCR
└── assets/
    ├── Banco de dados.kivy.xlsx # planilha de motoristas cadastrados
    └── placa_teste.webp         # imagem de teste
```

## Como rodar o projeto

### 1. Instalar o Python 3.11

O Kivy ainda não possui suporte total às versões mais recentes do Python. Recomendado usar o Python 3.11.

### 2. Instalar as dependências

```bash
pip install kivy[full]
pip install easyocr
pip install opencv-python
pip install Pillow pandas openpyxl plyer
```

### 3. Rodar o sistema

```bash
cd "controle de acesso"
python main.py
```

Na primeira execução, o EasyOCR baixa automaticamente os modelos de reconhecimento (é necessário ter conexão com a internet nesse primeiro uso).

## Funcionalidades

- Captura de imagem em tempo real pela webcam
- Leitura e correção automática de caracteres ambíguos (ex.: `Z`→`7`, `O`→`0`)
- Interface estilizada como tela de smartphone, com animação de scanner
- Cadastro de motoristas via planilha Excel
- Histórico de tentativas de acesso (liberadas e negadas) no banco de dados
- Seletor de imagem para testes sem depender da câmera

## Autoria

Projeto desenvolvido por Jessyca Fernandes como parte de um workshop de Python.
