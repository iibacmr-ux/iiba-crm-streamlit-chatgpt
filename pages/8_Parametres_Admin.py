import streamlit as st
import pandas as pd
from modules.repo import init_db, list_contacts, recalc_score
from modules.utils import CHOICES

init_db()
st.title('⚙️ Paramètres & Admin')

st.subheader('Recalcul des scores IIBA')
contacts = list_contacts()
ids = [c.id for c in contacts]
if st.button('Recalculer tous les scores'):
    for cid in ids:
        recalc_score(cid)
    st.success('Recalcul effectué.')
    st.experimental_rerun()

st.divider()
st.subheader('Exporter les contacts (CSV)')
if st.button('Exporter .csv'):
    import io
    df = pd.DataFrame([c.dict() for c in contacts])
    st.download_button('Télécharger contacts.csv', data=df.to_csv(index=False).encode('utf-8'), file_name='contacts.csv', mime='text/csv')

st.divider()
st.subheader('Listes de valeurs (lecture seule)')
for k,v in CHOICES.items():
    with st.expander(k.capitalize()):
        st.write(v)
