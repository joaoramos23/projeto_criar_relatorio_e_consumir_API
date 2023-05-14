
"""
Banco de dados utilizado: SQL Server.
Para saber qual driver usar, basta pesquisar o driver do respectivo banco de dados.
É necessário criar um DATABASE chamado 'produtos_fakestore' no seu banco de dados. 'CREATE DATABASE produtos_fakestore;'
Estou disponibilizando este código com a inserção no banco de dados. No entanto, abaixo há uma função chamada 'order_items()'. Ela consome a API e imprime na tela todos os itens de forma organizada.
Basta comentar a linha do código que chama a 'main_function()' e chamar a função 'order_items()' para visualizar a impressão.

Link API utilizada:'https://fakestoreapi.com/products'.
"""


import requests # pip install requests
import json
import pyodbc # pip install pyodbc
import re # problema com aspas, impossibilitando de inserir no banco de dados


DRIVER = "{ODBC Driver 17 for SQL Server}"
SERVER = "NOME SERVIDOR"
USER = "USUARIO"
PASSWORD = "SENHA"


def request():
    resposta = requests.get('https://fakestoreapi.com/products')
    resposta = resposta.json()
    return resposta

def connection_data():
    conexao_dados = (
        f"Driver={DRIVER};" # Driver do banco de dados
        f"Server={SERVER};" # Nome do servidor
        "Database=master;" # Nome banco de dados
        f"UID={USER};" # Usuario
        f"PWD={PASSWORD}" # Senha
        )
    return conexao_dados

def connect():
    conexao_dados = connection_data()
    conexao_data = pyodbc.connect(conexao_dados,autocommit = True)
    print("Conexão Bem Sucedida")
    return conexao_data

def create_cursor(conexao):
    criando_cursor = conexao.cursor()
    return criando_cursor

def create_table(cursor):
    cursor.execute(""" USE produtos_fakestore; 
        DROP TABLE PRODUTOS;    
        CREATE TABLE PRODUTOS (
        ID VARCHAR(15) PRIMARY KEY,
        TITLE VARCHAR(250),
        PRICE DECIMAL(5,2),
        DESCRIPTION TEXT,
        CATEGORY VARCHAR(250),
        IMAGE VARCHAR(250),
        RATE DECIMAL(5,2),
        COUNT INT
        );""") 

def insert_items(cursor):
    resposta = request()
    for itens in resposta:
        cod_item = itens['id']
        titulo = re.sub("\'","",itens['title'])
        preco = itens['price']
        descricao = re.sub("\'","",itens['description'])
        categoria = re.sub("\'","",itens['category'])
        imagem_url = itens['image']
        avaliacao = itens['rating']['rate']
        importancia = itens['rating']['count']
        cursor.execute("""
        USE produtos_fakestore;
        INSERT INTO PRODUTOS (ID, TITLE, PRICE, DESCRIPTION, CATEGORY, IMAGE, RATE, COUNT)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """,
        cod_item, titulo, preco, descricao, categoria, imagem_url, avaliacao, importancia)
            
def main_function():
    conexao = connect()
    cursor = create_cursor(conexao)
    create_table(cursor)
    insert_items(cursor)

#main_function()

# Função para visualizar os itens consumidos da API no console:

def order_items():  
    resposta = request()
    for itens in resposta:
        print("ID ITEM: ",itens['id'])
        print("TITULO: ",itens['title'])
        print("PREÇO: ",itens['price'])
        print("DESCRIÇÃO: ",itens['description'])
        print("CATEGORIA: ",itens['category'])
        print("IMAGEM URL: ",itens['image'])
        print("AVALIAÇÃO: ",itens['rating']['rate'])
        print("IMPORTANCIA: ",itens['rating']['count'],end="\n\n\n")

order_items()