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
            if st.button('Abrir caixa'):

                repo.planilha_caixa_entrada_saida(data)

        if menu == 'Lançar':
            data = st.date_input('Data', format='DD/MM/YYYY')
            movimento = st.selectbox('Tipo de Movimentação', ['ENTRADA', 'SAIDA'], index=None)
            descricao = st.text_input('Descrição')
            forma_pg = st.selectbox('Forma Pagamento', ['Dinheiro', 'Pix', 'Saida'], index=None)
            valor = st.text_input('Valor')
            if st.button('Lançar no Caixa'):
                repo.insert_click_caixa(data, movimento, descricao, forma_pg, valor)
                st.success('Lançamento inserido no caixa')
