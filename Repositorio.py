import mysql.connector

from model.Ativos import Ativo


class Repository:

    mydb = mysql.connector.connect(
        host = '',
        user = '',
        password = ''
    )

    def insert(ativo:Ativo):
        mycursor = mydb.cursor()
        sql = ('INSERT INTO ativos (id, nome, categoria, responsavel, setor, localizacao, vulnerabilidades) VALUES ({}, {}, {}, {}, {}, {}, {})'
               .format(ativo.id, ativo.nome, ativo.categoria.name, ativo.responsavel, ativo.setor, ativo.localizacao, ativo.vulnerabilidades))
        mycursor.execute(sql)
        mycursor.commit()

    def find_all():
        mycursor = mydb.cursor()
        sql = ('SELECT * FROM ativos')
        mycursor.execute(sql)
        return mycursor.fetchall()

    def find_by_id(id):
        mycursor = mydb.cursor()
        sql = ('SELECT * FROM ativos WHERE id = {}').format(id)
        mycursor.execute(sql)
        return mycursor.fetchall()

    def find_by_nome(nome):
        mycursor = mydb.cursor()
        sql = ('SELECT * FROM ativos WHERE nome = {}').format(nome)
        mycursor.execute(sql)
        return mycursor.fetchall()