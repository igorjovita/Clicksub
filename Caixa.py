from streamlit_option_menu import option_menu
from functions import Functions
from database import DataBaseMysql
import streamlit as st

db = DataBaseMysql()
repo = Functions(db)


class Caixa:

    def visualizar_caixa(self):
        menu = option_menu('Caixa ClickSub', ['Visualizar', 'Lançar'], orientation='horizontal')

        if menu == 'Visualizar':
            data = st.date_input('Data do caixa', format='DD/MM/YYYY')
            repo.planilha_caixa_entrada_saida(data)
