#manipula banco de dados
import sqlite3
#trabalha coma arquivos e pastas
import os

#Pega a pasta onde o banaco.py está
PASTA= os.path.dirname(os.path.abspath(__file__))
BANCO= os.path.join(PASTA, 'acesso.db')

def criar_banco():
    conn= sqlite3.connect(BANCO)
    cursor= conn.cursor()
    
    # Tabela de motoristas cadastrados; #texto únicoe não nulo, # integer é o valor inteiro, primary key é a identificação única de cada registro, autoincrement o banco cria o umero, #se vc n informar o valor ele bota 1
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motoristas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricula TEXT NOT NULL,
            placa TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            setor TEXT,
            ativa INTEGER DEFAULT 1 
        )     
    ''')
    
    # Tabela de log de acessos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS log_acessos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            data_hora TEXT NOT NULL,
            status TEXT NOT NULL,
            motivo TEXT
        )
    ''')
    
    #Confirma e salva alterações
    conn.commit()
    conn.close()
    print('Banco de dados criado com sucesso!')
    
def buscar_motoristas(placa):
    conn= sqlite3.connect(BANCO)
    cursor= conn.cursor()
    
    cursor.execute('''
        SELECT matricula, nome, setor, ativa
        FROM motoristas
        WHERE placa= ?
    ''', (placa,))
    
    resultado= cursor.fetchone()
    conn.close()
    return resultado

def registrar_acesso(placa, status, motivo=None):
    from datetime import datetime

    # Guarda a data e hora em uma variável
    data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    conn = sqlite3.connect(BANCO)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO log_acessos (placa, data_hora, status, motivo)
        VALUES (?, ?, ?, ?)
    ''', (
        placa,
        data_hora,
        status,
        motivo
    ))

    conn.commit()
    conn.close()

    # Retorna a data para quem chamou a função
    return data_hora
    
def inserir_motorista_teste():
    conn= sqlite3.connect(BANCO)
    cursor= conn.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO motoristas (matricula, placa, nome, setor, ativa)
        VALUES (?, ?, ?, ?, ?)
    ''', ('12345', 'QRM7E33', 'João Silva', 'Logística', 1))
    
    
    conn.commit()
    conn.close()
    print('Motorista de teste inserido!')


def importar_excel(caminho_arquivo):
    import pandas as pd
    
    df= pd.read_excel(caminho_arquivo)
    
    conn= sqlite3.connect(BANCO)
    cursor= conn.cursor()
    
    total_inseridos= 0
    
    
    for _, linha in df.iterrows():
        matricula = str(linha['MATRÍCULA'])
        placa = str(linha['PLACA']).upper().replace(' ', '')
        nome = str(linha['NOME'])
        setor = str(linha['SETOR'])
        ativa = 1 if str(linha['ATIVA']).upper() == 'SIM' else 0
        
        cursor.execute('''
            INSERT OR REPLACE INTO motoristas(matricula, placa, nome, setor, ativa)
            VALUES (?, ?, ?, ?, ?)
        ''',(matricula, placa, nome, setor, ativa))
        
        total_inseridos += 1
    
    conn.commit()
    conn.close()
    print(f'{total_inseridos} motoristas importados com sucesso!')
 

if __name__ == '__main__':
    criar_banco()
    importar_excel(os.path.join(PASTA, '..', 'assets', 'Banco de dados.kivy.xlsx'))