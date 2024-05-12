import mysql.connector
import os
import streamlit as st
import yaml
from yaml.loader import SafeLoader
from PIL import Image
import streamlit_authenticator as stauth
import pandas as pd
from babel.numbers import format_currency


chars = "'),([]"


class Functions:

    def __init__(self, db):
        self.db = db

    def authenticate(self):
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

    def select_titular(self, data):

        query = "SELECT id_cliente, nome_cliente from reserva where data = %s and id_cliente = id_titular"
        params = (data,)

        return self.db.execute_query(query, params)

    def planilha_caixa_entrada_saida(self, data):
        select = self.obter_lancamentos_caixa(data)
        entrada = []
        saida = []
        colun1, colun2, colun3, colun4 = st.columns(4)
        col1, col2 = st.columns(2)
        if select:
            for item in select:
                if item[0] == 'ENTRADA':
                    entrada.append((item[1], item[2], item[3]))
                else:
                    saida.append((item[1], item[2], item[3]))

            if entrada:

                df_entrada = pd.DataFrame(entrada, columns=['Descriçao', 'Pagamento', 'Valor'])
                valor = df_entrada['Valor'].str.replace('R$ ', '')
                valor = valor.str.replace(',', '.').astype(float)

                total = valor.sum()
                total = format_currency(total, 'BRL', locale='pt_BR')
                df_entrada.loc[len(df_entrada.index)] = ['Total', '', total]
                with colun2:
                    st.subheader('Entrada')
                with col1:

                    st.markdown(df_entrada.style.hide(axis="index").to_html(), unsafe_allow_html=True)

            if saida:
                df_saida = pd.DataFrame(saida, columns=['Descriçao', 'Pagamento', 'Valor'])
                with colun3:
                    st.subheader('Saida')
                with col2:
                    st.markdown(df_saida.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    def obter_lancamentos_caixa(self, data):
        query = """
        SELECT 
            movimento,
            CASE WHEN descricao IS NULL THEN '' ELSE descricao END,
            CASE WHEN forma_pg IS NULL THEN '' ELSE forma_pg END,
            CASE WHEN valor IS NULL THEN '' ELSE CONCAT('R$ ', FORMAT(valor, 2, 'de_DE')) END
        FROM click_caixa WHERE data = %s"""
        params = (data,)

        return self.db.execute_query(query, params)

    def select_reserva(self, data, id_titular):

        query = """
        SELECT 
            c.nome, 
            c.telefone, 
            r.tipo, 
            r.id, 
            c.id 
        from reserva as r 
        INNER JOIN cliente as c ON r.id_cliente = c.id 
        WHERE r.data = %s and r.id_titular = %s"""

        params = (data, id_titular)

        return self.db.execute_query(query, params)

    def select_planilha_acqua(self, data):

        query = """
        SELECT 
            c.id, 
            r.id, 
            c.nome, 
            c.telefone, 
            v.nome, 
            r.tipo, 
            r.fotos 
        from reserva as r  
        JOIN cliente as c on r.id_cliente = c.id 
        JOIN vendedores as v ON r.id_vendedor = v.id 
        where r.data = %s """

        params = (data,)

        return self.db.execute_query(query, params)

    def select_id_staff(self, nome):
        query = "SELECT id FROM click_staffs WHERE nome = %s"
        params = (nome,)

        return self.db.execute_query(query, params)

    def select_operadoras(self):
        query = "SELECT id, nome from click_operadoras"

        return self.db.execute_query(query)

    def insert_click_pagamentos(self, data, id_reserva, pacote, forma_pg, valor):

        query = """
        INSERT INTO click_pagamentos 
        (data, id_reserva, pacote, forma_pg, valor, id_operadora) 
        VALUES (%s, %s, %s, %s, %s, %s)"""

        params = (data, id_reserva, pacote, forma_pg, valor, 1)

        return self.db.execute_query(query, params)

    def insert_click_caixa(self, data, movimento, descricao, forma_pg, valor):

        query = """
        INSERT INTO click_caixa 
        (data, movimento, descricao, forma_pg, valor) 
        VALUES (%s, %s, %s, %s, %s)"""

        params = (data, movimento, descricao, forma_pg, valor)

        return self.db.execute_query(query, params)

    def insert_click_lancamentos(self, data, id_staff, id_operadora, fotos, video, situacao):

        query = """
        INSERT INTO click_lancamentos 
        (data, id_staff, id_operadora, fotos, videos, situacao) 
        VALUES (%s, %s, %s, %s, %s, %s)"""

        params = (data, id_staff, id_operadora, fotos, video, situacao)

        return self.db.execute_query(query, params)

    def pressionar(self):
        st.session_state.botao = True
        # Atualize a lista de itens selecionados com os IDs correspondentes
        st.session_state.selected_items = st.session_state.df_state[
            st.session_state.df_state['Selecionar']].index.tolist()

    def update_telefone(self, telefone, id_cliente):
        query = "UPDATE reserva set telefone = %s where id_cliente = %s"

        params = (telefone, id_cliente)

        return self.db.execute_query(query, params)

    def update_foto_reserva(self, pacote, id_reserva):

        foto = ''
        if pacote == 'FOTO 5':
            foto = 'F5'
        elif pacote == 'FOTO 10':
            foto = 'F10'
        elif pacote == 'VIDEO':
            foto = 'Video'
        elif pacote == 'FOTO + VIDEO':
            foto = 'F/V'

        query = "UPDATE reserva set fotos = %s where id = %s"
        params = (foto, id_reserva)

        return self.db.execute_query(query, params)

    def create_clicksub(self):
        query = """
        CREATE TABLE IF NOT EXISTS pagamento_clicksub(
            id int not null auto_increment,
            id_reserva int,
            pacote varchar(40),
            forma_pg varchar(40),
            valor varchar(40),
            primary key (id),
            foreign key (id_reserva) references reserva(id));
        """
        self.db.execute_query(query)

    def create_click_staffs(self):
        query = """
            CREATE TABLE IF NOT EXISTS click_staffs(
                id int not null auto_increment,
                nome varchar(40),
                usuario varchar(40),
                foto5 int,
                foto10 int,
                foto_cred int,
                video int,
                primary key (id))
        """

        self.db.execute_query(query)

    def create_click_operadoras(self):
        query = """
            CREATE TABLE IF NOT EXISTS click_operadoras(
                id int not null auto_increment,
                nome varchar(40),
                foto5 int,
                foto10 int,
                foto_cred int,
                video int,
                primary key (id));
        """
        self.db.execute_query(query)

    def create_click_lancamentos(self):
        query = """
            CREATE TABLE IF NOT EXISTS click_lancamentos (
                id int not null auto_increment,
                data date,
                id_staff int,
                id_operadora int,
                fotos int,
                videos int,
                situacao varchar(40),
                primary key (id),
                foreign key (id_staffs) references click_staffs(id),
                foreign key (id_operadora) references click_operadoras(id));
            """

        self.db.execute_query(query)

    def create_click_caixa(self):
        query = """
        CREATE TABLE click_caixa(
            id int not null auto_increment,
            data date,
            movimento varchar(40),
            descricao varchar(50),
            forma_pg varchar(25),
            valor decimal(10,2),
        primary key (id));
        """
        self.db.execute_query(query)
