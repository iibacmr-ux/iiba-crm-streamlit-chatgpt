import streamlit as st
import pandas as pd
from datetime import date
from modules.models import Evenement
from modules.repo import init_db, add_evenement, list_evenements

init_db()
st.title('📅 Événements')

with st.form('add_evt', clear_on_submit=True):
    c1,c2,c3 = st.columns(3)
    with c1:
        nom = st.text_input('Nom Événement*','')
        type_evt = st.selectbox('Type', ['Formation','Groupe d\'étude','BA MEET UP','Webinaire','Conférence','Certification'])
        d = st.date_input('Date', value=date.today())
    with c2:
        duree = st.number_input('Durée (h)', value=2.0, step=0.5)
        lieu = st.selectbox('Lieu', ['Présentiel','Zoom','Hybride'])
        formateurs = st.text_input('Formateur(s)')
    with c3:
        invites = st.text_input('Invité(s)')
        objectif = st.text_area('Objectif')
        notes = st.text_area('Notes')
    if st.form_submit_button('Créer'):
        e = Evenement(nom=nom, type=type_evt, date=d, duree_h=duree, lieu=lieu, formateurs=formateurs or None, invites=invites or None, objectif=objectif or None, notes=notes or None)
        add_evenement(e)
        st.success('Événement créé.')

rows = list_evenements()
st.dataframe(pd.DataFrame([r.dict() for r in rows]), use_container_width=True, hide_index=True)
