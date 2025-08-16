import streamlit as st
import pandas as pd
from modules.repo import init_db, list_interactions, list_participations, list_paiements, list_certifs, get_contact

init_db()
st.title('🔎 Vue 360° Contact')

cid = st.number_input('ID Contact', min_value=1, step=1)
if st.button('Charger la fiche'):
    c = get_contact(int(cid))
    if not c:
        st.error('Contact introuvable.')
    else:
        st.subheader(f"{c.prenom} {c.nom} — {c.titre or ''}")
        st.write(f"**Société**: {c.societe or '-'} | **Secteur**: {c.secteur or '-'} | **Ville**: {c.ville or '-'}")
        st.write(f"**Email**: {c.email or '-'} | **Tel**: {c.telephone or '-'} | **Type**: {c.type_contact or '-'} | **Statut**: {c.statut or '-'}")
        st.metric('Score IIBA', c.score_iiba)
        tabs = st.tabs(['Interactions','Participations','Paiements','Certifications'])
        with tabs[0]: st.dataframe(pd.DataFrame([i.dict() for i in list_interactions(int(cid))]), use_container_width=True, hide_index=True)
        with tabs[1]: st.dataframe(pd.DataFrame([p.dict() for p in list_participations(contact_id=int(cid))]), use_container_width=True, hide_index=True)
        with tabs[2]: st.dataframe(pd.DataFrame([p.dict() for p in list_paiements() if p.contact_id==int(cid)]), use_container_width=True, hide_index=True)
        with tabs[3]: st.dataframe(pd.DataFrame([x.dict() for x in list_certifs(contact_id=int(cid))]), use_container_width=True, hide_index=True)
