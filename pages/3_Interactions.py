import streamlit as st
import pandas as pd
from datetime import date
from modules.models import Interaction
from modules.repo import init_db, add_interaction, list_interactions

init_db()
st.title('✉️ Interactions')

with st.form('add_interaction', clear_on_submit=True):
    c1,c2,c3 = st.columns(3)
    with c1:
        contact_id = st.number_input('ID Contact*', min_value=1, step=1)
        d = st.date_input('Date*', value=date.today())
        canal = st.selectbox('Canal', ['Appel','Email','WhatsApp','Zoom','Présentiel','Autre'])
    with c2:
        objet = st.text_input('Objet')
        resume = st.text_area('Résumé')
    with c3:
        resultat = st.selectbox('Résultat', ['Positif','Négatif','À suivre','Sans suite'])
        prochaine_action = st.text_input('Prochaine Action')
        relance = st.date_input('Relance', value=None)
        resp = st.text_input('Responsable')
    if st.form_submit_button('Insérer'):
        inter = Interaction(contact_id=int(contact_id), date=d, canal=canal, objet=objet or None, resume=resume or None, resultat=resultat or None, prochaine_action=prochaine_action or None, relance=relance, responsable=resp or None)
        add_interaction(inter)
        st.success('Interaction ajoutée.')

st.subheader('Historique')
rows = list_interactions()
st.dataframe(pd.DataFrame([r.dict() for r in rows]), use_container_width=True, hide_index=True)
