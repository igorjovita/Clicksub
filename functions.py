import mysql.connector
import os
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from PIL import Image
import streamlit_authenticator as stauth

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

chars = "'),([]"


def authenticate():
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    authenticator.login()

    if st.session_state["authentication_status"]:
        with st.sidebar:
            img = Image.open('logo_click.png')

            # Remover a margem ao redor da imagem
            img_cropped = img.crop(img.getbbox())
            st.image(img_cropped, use_column_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f'*{st.session_state["name"]}*')
            with col2:
                authenticator.logout()


    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


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

        cursor.execute("INSERT INTO click_pagamentos (id_reserva, pacote, forma_pg, valor, id_operadora) VALUES (%s, "
                       "%s, %s, %s)",
                       (id_reserva, pacote, forma_pg, valor, 1))

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


def select_titular(data):
    try:
        mydb.connect()

        cursor.execute("SELECT nome_cliente, id_titular from reserva where data = %s and id_cliente = id_titular",
                       (data,))
        dados = cursor.fetchall()
        lista = []
        lista_nome_id = []
        for dado in dados:
            nome_titular = (str(dado[0]).translate(str.maketrans('', '', chars)))
            lista.append(nome_titular)
            lista_nome_id.append(dado)
        return lista, lista_nome_id

    except mysql.connector.Error as err:
        st.error(f"Erro ao executar a consulta: {err}")
        return []  # Retorna uma lista vazia em caso de erro

    finally:
        data = None
        dados = None
        mydb.close()


def select_reserva_titular(data, id_titular):
    try:
        mydb.connect()
        cursor.execute(
            "SELECT c.nome, c.telefone, r.tipo, r.id, c.id from reserva as r INNER JOIN cliente as c ON r.id_cliente = c.id where r.data = %s and r.id_titular = %s",
            (data, id_titular))
        dados = cursor.fetchall()

        return dados

    except mysql.connector.Error as err:
        st.error(f"Erro ao executar a consulta: {err}")
        return []

    finally:
        mydb.close()
        dados = None


def create_click_staffs():
    mydb.connect()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS click_staffs(
            id int not null auto_increment,
            nome varchar(40),
            usuario varchar(40),
            foto5 int,
            foto10 int,
            foto_cred int,
            video int,
            primary key (id))
    """)


def create_click_operadoras():
    mydb.connect()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS click_operadoras(
            id int not null auto_increment,
            nome varchar(40),
            foto5 int,
            foto10 int,
            foto_cred int,
            video int,
            primary key (id));
    """)


def create_click_lancamentos():
    mydb.connect()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS click_lancamentos (
            id int not null auto_increment,
            data date,
            id_staffs int,
            id_operadora int,
            fotos int,
            videos int,
            situacao varchar(40),
            primary key (id),
            foreign key (id_staffs) references click_staffs(id),
            foreign key (id_operadora) references click_operadoras(id));
        """)


