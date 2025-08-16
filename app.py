import streamlit as st
import pandas as pd
from modules.repo import init_db, kpi_totaux, list_paiements, list_participations, list_evenements
from modules import charts

st.set_page_config(page_title='IIBA Cameroun CRM', layout='wide')
init_db()

st.title('📊 Dashboard IIBA Cameroun')

kpi = kpi_totaux()
c1,c2,c3,c4 = st.columns(4)
c1.metric('Contacts', kpi.get('total_contacts',0))
c2.metric('Membres IIBA', kpi.get('membres',0))
c3.metric('Prospects actifs', kpi.get('prospects_actifs',0))
c4.metric('Score moyen', kpi.get('score_moyen',0))

c5,c6,c7 = st.columns(3)
c5.metric('Événements', kpi.get('evenements',0))
c6.metric('Participations', kpi.get('participations',0))
c7.metric('CA réglé (FCFA)', int(kpi.get('ca_regle',0)))

st.divider()
evts = list_evenements()
parts = list_participations()
pays = list_paiements()

import pandas as pd
df_parts = pd.DataFrame([{'periode': (e.periode if e else ''),'type_evenement': (e.type if e else ''),'participants':1} for p in parts for e in evts if e.id==p.evenement_id])
fig1 = charts.chart_participants_par_periode_type(df_parts.groupby(['periode','type_evenement']).sum(numeric_only=True).reset_index())

df_pay = pd.DataFrame([{'nom_evenement': next((e.nom for e in evts if e.id==p.evenement_id), 'N/A'),'statut': p.statut or 'N/A','montant': p.montant or 0} for p in pays])
fig2 = charts.chart_ca_par_event_statut(df_pay.groupby(['nom_evenement','statut']).sum(numeric_only=True).reset_index())

df_imp = df_pay[df_pay['statut'].isin(['Non payé','Partiel'])].groupby('statut').sum(numeric_only=True).reset_index()
fig3 = charts.chart_impayes_pie(df_imp)

colA,colB,colC = st.columns(3)
colA.altair_chart(fig1, use_container_width=True)
colB.altair_chart(fig2, use_container_width=True)
colC.altair_chart(fig3, use_container_width=True)

st.caption("Commencez par créer des contacts, événements, participations et paiements pour animer le dashboard.")
