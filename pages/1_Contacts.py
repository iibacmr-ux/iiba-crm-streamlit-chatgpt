import streamlit as st
import pandas as pd
from modules.models import Contact
from modules.repo import init_db, add_contact, list_contacts, update_contact
from modules.utils import CHOICES, is_valid_email, clean_phone

init_db()
st.title('👥 Contacts')

with st.expander('➕ Ajouter un contact', expanded=False):
    with st.form('add_contact_form', clear_on_submit=True):
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            nom = st.text_input('Nom*','')
            prenom = st.text_input('Prénom*','')
            genre = st.selectbox('Genre*', CHOICES['genres'])
            email = st.text_input('Email','')
        with col2:
            titre = st.text_input('Titre/Fonction','')
            societe = st.text_input('Société','')
            secteur = st.selectbox('Secteur', CHOICES['secteurs'])
            telephone = st.text_input('Téléphone*','')
        with col3:
            ville = st.selectbox('Ville', CHOICES['villes'])
            pays = st.selectbox('Pays', CHOICES['pays'])
            type_contact = st.selectbox('Type', CHOICES['types_contact'], index=1)
            source = st.selectbox('Source', CHOICES['sources'])
            statut = st.selectbox('Statut', CHOICES['statuts'])
        notes = st.text_area('Notes')
        linkedin = st.text_input('LinkedIn')
        attentes = st.text_input('Attentes (texte libre)')
        if st.form_submit_button('Insérer'):
            if not nom or not prenom or not genre or not telephone:
                st.error('Champs requis manquants.')
            elif not is_valid_email(email):
                st.error("Email invalide.")
            else:
                c = Contact(nom=nom.strip(), prenom=prenom.strip(), genre=genre, titre=titre or None, societe=societe or None, secteur=secteur or None, email=email or None, telephone=clean_phone(telephone), ville=ville or None, pays=pays or None, type_contact=type_contact, source=source or None, statut=statut or None, notes=notes or None, linkedin=linkedin or None, attentes=attentes or None)
                c=add_contact(c)
                st.success(f"Contact #{c.id} inséré : {c.prenom} {c.nom}")

q = st.text_input('Recherche (nom, prénom, email, société)')
fc1,fc2,fc3,fc4 = st.columns(4)
with fc1: f_type = st.selectbox('Type', ['']+CHOICES['types_contact'])
with fc2: f_statut = st.selectbox('Statut', ['']+CHOICES['statuts'])
with fc3: f_secteur = st.selectbox('Secteur', ['']+CHOICES['secteurs'])
with fc4: f_ville = st.selectbox('Ville', ['']+CHOICES['villes'])
rows = list_contacts(q or None, f_type or None, f_statut or None, f_secteur or None, f_ville or None)
df = pd.DataFrame([r.dict() for r in rows])
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader('✏️ Modifier un contact')
colx1,colx2 = st.columns([1,1])
with colx1: edit_id = st.number_input('ID Contact', min_value=0, step=1)
with colx2: new_statut = st.selectbox('Nouveau Statut', CHOICES['statuts'])
if st.button('Mettre à jour statut', type='primary'):
    if edit_id:
        ok = update_contact(int(edit_id), {'statut': new_statut})
        if ok: st.success('Statut mis à jour.'); st.experimental_rerun()
        else: st.error('ID introuvable.')
