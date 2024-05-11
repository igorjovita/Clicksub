import streamlit as st

import Lançamentos
import Vendas
from functions import Functions
from database import DataBaseMysql

db = DataBaseMysql()
repo = Functions(db)

lista_nivel_1 = ['ricardo']

repo.authenticate()
if st.session_state["authentication_status"]:

    sidebar_opcoes = None
    if st.session_state["username"] in lista_nivel_1:
        sidebar_opcoes = ['Vendas', 'Lançamentos', 'Caixa', 'Financeiro']
        st.sidebar.write('---')
        st.sidebar.title('Menu')

    else:
        sidebar_opcoes = ['Vendas', 'Caixa']

    sidebar_menu = st.sidebar.radio('Selecione uma pagina', sidebar_opcoes)

    if sidebar_menu == 'Vendas':
        Vendas.layout_vendas()

    elif sidebar_menu == 'Lançamentos':
        Lançamentos.lancamentos()


    elif sidebar_menu == 'Caixa':
        Caixa.caixa()
