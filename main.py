import streamlit as st
import Vendas

lista_nivel_1 = ['ricardo']
if st.session_state["authentication_status"]:
    st.sidebar.write('---')
    st.sidebar.title('Menu')

    if st.session_state["username"] in lista_nivel_1:
        sidebar_opcoes = ['Vendas', 'Lançamentos', 'Financeiro']
    else:
        sidebar_opcoes = None

    if sidebar_opcoes is None:
        sidebar_menu = 'Vendas'

    else:
        sidebar_menu = st.sidebar.radio('Selecione uma pagina', sidebar_opcoes)

    if sidebar_menu == 'Vendas':
        Vendas.layout_vendas()

