import streamlit as st
import pandas as pd
from datetime import date
from modules.models import Certification
from modules.repo import init_db, add_certif, list_certifs

init_db()
st.title('🎓 Certifications')

with st.form('add_cert', clear_on_submit=True):
    c1,c2,c3 = st.columns(3)
    with c1:
        cid = st.number_input('ID Contact*', min_value=1, step=1)
        typec = st.selectbox('Type Certif', ['ECBA','CCBA','CBAP','PBA'])
        d_ex = st.date_input('Date Examen', value=date.today())
    with c2:
        resultat = st.selectbox('Résultat', ['Réussi','Échoué','En cours','Reporté'])
        score = st.number_input('Score', min_value=0.0, step=1.0)
        d_obt = st.date_input('Date Obtention', value=None)
    with c3:
        validite = st.text_input('Validité')
        renouvellement = st.date_input('Renouvellement', value=None)
        notes = st.text_area('Notes')
    if st.form_submit_button('Ajouter'):
        c = Certification(contact_id=int(cid), type_certif=typec, date_examen=d_ex, resultat=resultat, score=score or None, date_obtention=d_obt, validite=validite or None, renouvellement=renouvellement, notes=notes or None)
        add_certif(c)
        st.success('Certification ajoutée.')

rows = list_certifs()
st.dataframe(pd.DataFrame([r.dict() for r in rows]), use_container_width=True, hide_index=True)
