import streamlit as st
import pandas as pd
from datetime import datetime
from modules.models import Participation
from modules.repo import init_db, add_participation, list_participations

init_db()
st.title('📝 Participations')

with st.form('add_part', clear_on_submit=True):
    c1,c2,c3 = st.columns(3)
    with c1:
        cid = st.number_input('ID Contact*', min_value=1, step=1)
        eid = st.number_input('ID Événement*', min_value=1, step=1)
        role = st.selectbox('Rôle', ['Participant','Animateur','Invité'])
    with c2:
        insc = st.text_input('Inscription (YYYY-MM-DD HH:MM)','')
        arr = st.text_input('Arrivée (YYYY-MM-DD HH:MM)','')
        tmp = st.text_input('Temps Présent (ex: 1h20)','')
    with c3:
        fb = st.selectbox('Feedback', ['Très satisfait','Satisfait','Moyen','Insatisfait'], index=1)
        note = st.number_input('Note', min_value=0.0, max_value=5.0, step=0.5)
        com = st.text_area('Commentaire')
    if st.form_submit_button('Ajouter'):
        def parse_dt(s):
            try: return datetime.fromisoformat(s) if s else None
            except: return None
        p = Participation(contact_id=int(cid), evenement_id=int(eid), role=role, inscription=parse_dt(insc), arrivee=parse_dt(arr), temps_present=tmp or None, feedback=fb or None, note=note or None, commentaire=com or None)
        add_participation(p)
        st.success('Participation ajoutée.')

rows = list_participations()
st.dataframe(pd.DataFrame([r.dict() for r in rows]), use_container_width=True, hide_index=True)
