import pandas as pd
import altair as alt

def chart_participants_par_periode_type(df: pd.DataFrame):
    if df.empty:
        return alt.Chart(pd.DataFrame({'info':['Aucune donnée']})).mark_text(size=16).encode(text='info')
    return alt.Chart(df).mark_bar().encode(
        x=alt.X('periode:N', sort='-y', title='Période'),
        y=alt.Y('participants:Q', title='Participants'),
        color=alt.Color('type_evenement:N', title="Type d'événement"),
        tooltip=['periode','type_evenement','participants']
    ).properties(height=300)

def chart_ca_par_event_statut(df: pd.DataFrame):
    if df.empty:
        return alt.Chart(pd.DataFrame({'info':['Aucune donnée']})).mark_text(size=16).encode(text='info')
    return alt.Chart(df).mark_bar().encode(
        x=alt.X('nom_evenement:N', sort='-y', title='Événement'),
        y=alt.Y('montant:Q', title='Montant (FCFA)'),
        color=alt.Color('statut:N'),
        tooltip=['nom_evenement','statut','montant']
    ).properties(height=300)

def chart_impayes_pie(df: pd.DataFrame):
    if df.empty:
        return alt.Chart(pd.DataFrame({'info':['Aucune donnée']})).mark_text(size=16).encode(text='info')
    return alt.Chart(df).mark_arc(innerRadius=60).encode(
        theta='montant:Q', color='statut:N', tooltip=['statut','montant']
    ).properties(height=300)
