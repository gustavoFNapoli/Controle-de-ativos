import mysql.connector
import json

from model.Ativos import Ativo


class Repository:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host='localhost',
            port=3306,
            user = 'gustavo',
            password = '123456',
            database = 'controle'
        )

    def insert(self, ativo:Ativo):
        mycursor = self.mydb.cursor()
        sql = 'INSERT INTO ativos (nome, categoria, responsavel, setor, localizacao, vulnerabilidades) VALUES (%s, %s, %s, %s, %s, %s)'
        val = (ativo.nome,
               ativo.categoria.value,
               ativo.responsavel,
               ativo.setor,
               ativo.localizacao,
               json.dumps(ativo.vulnerabilidades, default=lambda obj: obj.value))
        mycursor.execute(sql, val)
        self.mydb.commit()

    def find_all(self):
        mycursor = self.mydb.cursor()
        sql = 'SELECT * FROM ativos'
        mycursor.execute(sql)
        return [Ativo(*item) for item in mycursor.fetchall()]

    def find_by_id(self, id):
        mycursor = self.mydb.cursor()
        sql = 'SELECT * FROM ativos WHERE id = %s'
        val = (id,)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()
        if resultado is None:
            return None
        return Ativo(*resultado)

    def find_by_nome(self, nome):
        mycursor = self.mydb.cursor()
        sql = 'SELECT * FROM ativos WHERE nome = %s'
        val = (nome,)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchall()
        if not resultado:
            return None
        return [Ativo(*item) for item in mycursor.fetchall()]

    def update(self, ativo:Ativo):
        mycursor = self.mydb.cursor()
        sql = 'UPDATE ativos SET nome = %s, categoria = %s, responsavel = %s, setor= %s, localizacao= %s, vulnerabilidades= %s WHERE id = %s'
        val = (ativo.nome,
               ativo.categoria.value,
               ativo.responsavel,
               ativo.setor,
               ativo.localizacao,
               json.dumps(ativo.vulnerabilidades, default=lambda obj: obj.value),
               ativo.id)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def update_vulnerabilidades(self, vulnerabilidades, id):
        mycursor = self.mydb.cursor()
        sql = 'UPDATE ativos SET vulnerabilidades= %s WHERE id = %s'
        val = (vulnerabilidades, id)
        mycursor.execute(sql, val)
        self.mydb.commit()

    def delete_ativo(self, id):
        mycursor = self.mydb.cursor()
        sql = 'DELETE FROM ativos WHERE id = %s'
        val = (id,)
        mycursor.execute(sql, val)
        self.mydb.commit()