import streamlit as st
import pandas as pd
from datetime import date
from modules.models import Paiement
from modules.repo import init_db, add_paiement, list_paiements

init_db()
st.title('💳 Paiements')

with st.form('add_pay', clear_on_submit=True):
    c1,c2,c3 = st.columns(3)
    with c1:
        cid = st.number_input('ID Contact*', min_value=1, step=1)
        eid = st.number_input('ID Événement', min_value=0, step=1, help='0 si non lié à un événement')
        d = st.date_input('Date Paiement', value=date.today())
    with c2:
        montant = st.number_input('Montant (FCFA)', min_value=0.0, step=1000.0)
        moyen = st.selectbox('Moyen', ['Mobile Money','Virement','CB','Cash'])
        statut = st.selectbox('Statut', ['Réglé','Partiel','Non payé'])
    with c3:
        reference = st.text_input('Référence')
        notes = st.text_area('Notes')
        relance = st.date_input('Relance', value=None)
    if st.form_submit_button('Enregistrer'):
        p = Paiement(contact_id=int(cid), evenement_id=int(eid) if eid>0 else None, date_paiement=d, montant=montant, moyen=moyen, statut=statut, reference=reference or None, notes=notes or None, relance=relance)
        add_paiement(p)
        st.success('Paiement enregistré.')

rows = list_paiements()
st.dataframe(pd.DataFrame([r.dict() for r in rows]), use_container_width=True, hide_index=True)
