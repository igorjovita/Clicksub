import streamlit as st
from database import DataBaseMysql
from functions import Functions
import pandas as pd
from babel.numbers import format_currency

db = DataBaseMysql()
repo = Functions(db)


def tela_info_clientes():
    st.subheader('Informações dos Clientes')

    data = st.date_input('Data da pesquisa', format='DD/MM/YYYY')

    if st.button('Pesquisar'):
        info = repo.select_info_clientes(data)

        df = pd.DataFrame(info, columns=['Nome', 'Telefone', 'Vendedor', 'Tipo', 'Pacote', 'Forma Pg', 'Valor'])
        df['Valor'] = format_currency(int(df['Valor']), 'BRL', locale='pt_BR')
        st.table(df)
