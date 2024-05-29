import streamlit as st
import Informacoes_cliente
import Lançamentos
import Vendas
from functions import Functions
from database import DataBaseMysql
from Caixa import Caixa

db = DataBaseMysql()
repo = Functions(db)
caixa = Caixa()
lista_nivel_1 = ['ricardo']

repo.authenticate()
if st.session_state["authentication_status"]:

    sidebar_opcoes = None
    if st.session_state["username"] in lista_nivel_1:
        sidebar_opcoes = ['Vendas', 'Lançamentos', 'Caixa', 'Financeiro', 'Informações Clientes']
        st.sidebar.write('---')
        st.sidebar.title('Menu')

    else:
        sidebar_opcoes = ['Vendas', 'Caixa', 'Informações Clientes']

    sidebar_menu = st.sidebar.radio('Selecione uma pagina', sidebar_opcoes)

    if sidebar_menu == 'Vendas':
        Vendas.layout_vendas()

    elif sidebar_menu == 'Lançamentos':
        Lançamentos.lancamentos()

    elif sidebar_menu == 'Informações Clientes':
        Informacoes_cliente.tela_info_clientes()

    elif sidebar_menu == 'Caixa':
        caixa.visualizar_caixa()
