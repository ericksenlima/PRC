#!/usr/bin/env python3

import cgi
#import psycopg2

#conexao = "dbname=historico user=postgres host=localhost"

form = cgi.FieldStorage()
cep = form.getvalue("cep")

#def insereNoticia():
#    conn = psycopg2.connect(conexao)
#    cur = conn.cursor()
#    cur.execute("INSERT INTO ceps (conteudo) VALUES (%s)", (str(cep),))
#    conn.commit()
#    conn.close()
#insereNoticia()

print ("Content-type: text/html\n\n" )
print ("<html><body>")
print ("<br/>")
print ("<a href={}>Vizualizar dados do CEP</a>".format("https://viacep.com.br/ws/{}/json/".format(cep)))
print ("</body></html>")