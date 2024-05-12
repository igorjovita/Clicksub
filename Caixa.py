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
            st.subheader('Lançamentos Caixa')

            col1, col2 = st.columns(2)
            with col1:
                data = st.date_input('Data', format='DD/MM/YYYY')
                descricao = st.text_input('Descrição')
                valor = st.text_input('Valor')

            with col2:
                movimento = st.selectbox('Tipo de Movimentação', ['ENTRADA', 'SAIDA'], index=None)
                forma_pg = st.selectbox('Forma Pagamento', ['Dinheiro', 'Pix', 'Saida'], index=None)

            if st.button('Lançar no Caixa'):
                repo.insert_click_caixa(data, movimento, descricao, forma_pg, valor)
                st.success('Lançamento inserido no caixa')
