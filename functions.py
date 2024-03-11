import mysql.connector
import os


mydb = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    autocommit=True,
    ssl_verify_identity=False,
    ssl_ca=r"C:\users\acqua\downloads\cacert-2023-08-22.pem",
    charset="utf8")

cursor = mydb.cursor(buffered=True)


def select_planilha_acqua(data):
    mydb.connect()
    cursor.execute("SELECT c.nome, c.telefone, v.nome, r.tipo, r.fotos from reserva as r  JOIN cliente as c on r.id_cliente = c.id JOIN vendedores as v ON r.id_vendedor = v.id where r.data = %s ", (data,))
    dados = cursor.fetchall()
    mydb.close()

    return dados
