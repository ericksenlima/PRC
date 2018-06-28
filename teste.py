#!/usr/bin/env python3

import cgi
import cgitb
import psycopg2
import json
import requests

cgitb.enable("/tmp/log.html")


# Dados para acessar os dados no KCEP

token = "OxJHdQosVeaxFPK2rvvsY3I7zy2W7FfX2BB2I3p8"
autenticacao = {"x-api-key": "{}".format(token)}


# Recuperando os dados do formulario HTML

def recupera_form_html():
    form = cgi.FieldStorage()
    consulta = {'cepOrigem': form.getvalue('cepOrigem'), 'cepDestino': form.getvalue('cepDestino'),
                'comprimento': form.getvalue('comprimento'), 'largura': form.getvalue('largura'),
                'altura': form.getvalue('altura'), 'peso': form.getvalue('peso'), 'servico': form.getvalue('servico')}
    return consulta


# Realiza a consulta diretamente no site recebendo dicionário e retorna dicionário Python

def consultar_site(dados):
    url_api = "https://api.kcep.run/{0}/{1}/{2}/{3}/{4}/{5}".format(
        dados["cepOrigem"], dados["cepDestino"],
        dados["comprimento"], dados["largura"], dados["altura"], dados["peso"])

    consulta = requests.get(url_api, headers=autenticacao)
    if consulta.status_code == 200:
        resposta = consulta.content.decode('utf-8')
        return json.loads(resposta)
    return None


'''
AREA DE TESTES

a = {'cepOrigem': "85801-001", 'cepDestino': "01505-010",
     'comprimento': "16", 'largura': "11", 'altura': "2", 'peso': "1"}

print(consultar_site(a))
'''

# Dados para acesso ao banco de dados

conexao = "dbname=historico user=postgres host=localhost"


# Testa se a tabela já existe no banco

def table_exists(table_str):
    exists = False
    try:
        con = psycopg2.connect(conexao)
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cur.fetchone()[0]
        cur.close()
    except psycopg2.Error as e:
        print(e)
    return exists


# Conectando e criando o banco

def criarbanco():
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    conn = psycopg2.connect("dbname=postgres user=postgres host=localhost")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute('CREATE DATABASE historico')
    conn = psycopg2.connect(conexao)
    cur = conn.cursor()

    # Criando tabela e colunas

    cur.execute('\
        CREATE TABLE public.consultaFretes\
            (id serial PRIMARY KEY,\
            cepOrigem text NOT NULL,\
            cepDestino text NOT NULL,\
            comprimento text NOT NULL,\
            largura text NOT NULL,\
            altura text NOT NULL,\
            peso text NOT NULL,\
            servico text NOT NULL,\
            data timestamp without time zone\
            );'
                )
    conn.commit()

    # Gravando os dados e encerra conexão
    cur.close()
    conn.close()


# Inserir uma consulta no banco, recebendo dicionário da consulta via API

def inserir_consulta():
    pass


# Realizar consulta já existente no banco, recebendo o código da consulta e retornando dicionário

def consulta_banco():
    pass
    # con = psycopg2.connect(conexao)
    # cur = con.cursor()
    # cur.execute("SELECT )
    # cur.close()
    # return registro


'''
def if __name__ == '__main__':

    recupera_form_html()
    
    if table_exists("consultaFretes"):
        print("Banco de consulta de fretes ja existe")
    else:
        print("Criando banco de consulta de fretes")
        criarbanco()
'''
