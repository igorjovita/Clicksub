import streamlit as st
from functions import select_planilha_acqua

st.subheader('Click Sub')

data_reserva = st.date_input('Data da panilha', format='DD/MM/YYYY')

dados = select_planilha_acqua(data_reserva)


st.table(dados)