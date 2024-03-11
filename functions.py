import mysql.connector
import os
import streamlit as st

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


def create_clicksub():
    mydb.connect()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagamento_clicksub(
        id int not null auto_increment,
        id_reserva int,
        pacote varchar(40),
        forma_pg varchar(40),
        valor varchar(40),
        primary key (id),
        foreign key (id_reserva) references reserva(id));
    """)

    mydb.close()


def insert_clicksub(id_reserva, pacote, forma_pg, valor):
    try:
        mydb.connect()

        cursor.execute("INSERT INTO pagamento_clicksub (id_reserva, pacote, forma_pg, valor) VALUES (%s, %s, %s, %s)", (id_reserva, pacote, forma_pg, valor))

    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar a reserva: {err}")
    finally:

        mydb.close()

def select_planilha_acqua(data):
    mydb.connect()
    cursor.execute(
        "SELECT c.id, r.id, c.nome, c.telefone, v.nome, r.tipo, r.fotos from reserva as r  JOIN cliente as c on r.id_cliente = c.id JOIN vendedores as v ON r.id_vendedor = v.id where r.data = %s ",
        (data,))
    dados = cursor.fetchall()
    mydb.close()

    return dados


def pressionar():
    st.session_state.botao = True
    # Atualize a lista de itens selecionados com os IDs correspondentes
    st.session_state.selected_items = st.session_state.df_state[st.session_state.df_state['Selecionar']].index.tolist()


def update_telefone(id_cliente, telefone):
    mydb.connect()
    cursor.execute("UPDATE reserva set telefone = %s where id_cliente = %s", (telefone, id_cliente))
    mydb.close()


def update_foto_reserva(id_reserva, pacote):

    try:
        mydb.connect()
        cursor = mydb.cursor()
        foto = ''
        if pacote == 'FOTO 5':
            foto = 'F5'
        elif pacote == 'FOTO 10':
            foto = 'F10'
        elif pacote == 'VIDEO':
            foto = 'Video'
        elif pacote == 'FOTO + VIDEO':
            foto = 'F/V'

        cursor.execute("UPDATE reserva set fotos = %s where id = %s", (foto, id_reserva))
        mydb.commit()
    except mysql.connector.Error as err:
        st.error(f"Erro ao atualizar a reserva: {err}")

    finally:

        mydb.close()



