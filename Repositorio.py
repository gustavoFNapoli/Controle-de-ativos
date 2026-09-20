import mysql.connector

from model.Ativos import Ativo


class Repository:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = 'localhost:3306',
            user = 'gustavo',
            password = '123456',
            database = 'controle'
        )

    def insert(self, ativo:Ativo):
        mycursor = self.mydb.cursor()
        sql = 'INSERT INTO ativos (id, nome, categoria, responsavel, setor, localizacao, vulnerabilidades) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        val = (ativo.id, ativo.nome, ativo.categoria.name, ativo.responsavel, ativo.setor, ativo.localizacao, ativo.vulnerabilidades)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def find_all(self):
        mycursor = self.mydb.cursor()
        sql = 'SELECT * FROM ativos'
        mycursor.execute(sql)
        return mycursor.fetchall()

    def find_by_id(self, id):
        mycursor = self.mydb.cursor()
        sql = 'SELECT * FROM ativos WHERE id = %s'
        mycursor.execute(sql, id)
        return mycursor.fetchall()

    def find_by_nome(self, nome):
        mycursor = self.mydb.cursor()
        sql = 'SELECT * FROM ativos WHERE nome = %s'
        mycursor.execute(sql, nome)
        return mycursor.fetchall()

    def update(self, ativo:Ativo):
        mycursor = self.mydb.cursor()
        sql = 'UPDATE ativos SET categoria = %s, responsavel = %s, setor= %s, localizacao= %s, vulnerabilidades= %s WHERE id = %s'
        val = (ativo.categoria, ativo.responsavel, ativo.setor, ativo.localizacao, ativo.vulnerabilidades, ativo.id)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def update_vulnerabilidades(self, vulnerabilidades, id):
        mycursor = self.mydb.cursor()
        sql = 'UPDATE ativos SET vulnerabilidades= %s WHERE id = %s'
        val = (vulnerabilidades, id)
        mycursor.execute(sql, val)
        self.mydb.commit()