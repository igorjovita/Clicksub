import streamlit as st
import pandas as pd
from functions import select_planilha_acqua

st.subheader('Click Sub')

data_reserva = st.date_input('Data da panilha', format='DD/MM/YYYY')
if st.button('Pesquisar'):

    dados = select_planilha_acqua(data_reserva)

    df = pd.DataFrame(dados, columns=['Nome', 'Telefone', 'Comissario', 'Tipo', 'Fotos'])

    df.insert(0, 'Selecionar', [False] * len(df))

    st.data_editor(df, hide_index=True)
