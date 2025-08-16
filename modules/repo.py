from typing import List, Optional
from contextlib import contextmanager
from sqlmodel import SQLModel, Session, create_engine, select, col
from .models import Contact, Interaction, Evenement, Participation, Paiement, Certification
from datetime import datetime
from .utils import format_period

DB_PATH='data/iiba.db'
engine=create_engine(f'sqlite:///{DB_PATH}', echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session

# Contacts
def add_contact(c: Contact)->Contact:
    with get_session() as s:
        s.add(c); s.commit(); s.refresh(c); return c

def update_contact(contact_id:int, data:dict)->Optional[Contact]:
    with get_session() as s:
        obj=s.get(Contact, contact_id)
        if not obj: return None
        for k,v in data.items():
            if hasattr(obj,k): setattr(obj,k,v)
        s.add(obj); s.commit(); s.refresh(obj); return obj

def delete_contact(contact_id:int)->bool:
    with get_session() as s:
        obj=s.get(Contact, contact_id)
        if not obj: return False
        s.delete(obj); s.commit(); return True

def list_contacts(q:Optional[str]=None, type_contact:Optional[str]=None, statut:Optional[str]=None, secteur:Optional[str]=None, ville:Optional[str]=None)->List[Contact]:
    with get_session() as s:
        st=select(Contact)
        if q:
            like=f"%{q}%"
            st=st.where((col(Contact.nom).like(like)) | (col(Contact.prenom).like(like)) | (col(Contact.email).like(like)) | (col(Contact.societe).like(like)))
        if type_contact: st=st.where(Contact.type_contact==type_contact)
        if statut: st=st.where(Contact.statut==statut)
        if secteur: st=st.where(Contact.secteur==secteur)
        if ville: st=st.where(Contact.ville==ville)
        st=st.order_by(Contact.prenom, Contact.nom)
        return list(s.exec(st))

def get_contact(contact_id:int)->Optional[Contact]:
    with get_session() as s:
        return s.get(Contact, contact_id)

# Interactions
def add_interaction(i: Interaction)->Interaction:
    with get_session() as s:
        s.add(i); s.commit(); s.refresh(i); return i

def list_interactions(contact_id:Optional[int]=None)->List[Interaction]:
    with get_session() as s:
        st=select(Interaction).order_by(Interaction.date.desc())
        if contact_id: st=st.where(Interaction.contact_id==contact_id)
        return list(s.exec(st))

# Evenements
def add_evenement(e: Evenement)->Evenement:
    with get_session() as s:
        if e.date and (not e.periode):
            e.periode = format_period(datetime.combine(e.date, datetime.min.time()), e.type or '')
        s.add(e); s.commit(); s.refresh(e); return e

def list_evenements()->List[Evenement]:
    with get_session() as s:
        st=select(Evenement).order_by(Evenement.date.desc().nullslast())
        return list(s.exec(st))

# Participations
def add_participation(p: Participation)->Participation:
    with get_session() as s:
        s.add(p); s.commit(); s.refresh(p); return p

def list_participations(contact_id:Optional[int]=None, evenement_id:Optional[int]=None)->List[Participation]:
    with get_session() as s:
        st=select(Participation).order_by(Participation.id.desc())
        if contact_id: st=st.where(Participation.contact_id==contact_id)
        if evenement_id: st=st.where(Participation.evenement_id==evenement_id)
        return list(s.exec(st))

# Paiements
def add_paiement(p: Paiement)->Paiement:
    with get_session() as s:
        s.add(p); s.commit(); s.refresh(p); return p

def list_paiements(evenement_id:Optional[int]=None)->List[Paiement]:
    with get_session() as s:
        st=select(Paiement).order_by(Paiement.date_paiement.desc().nullslast())
        if evenement_id: st=st.where(Paiement.evenement_id==evenement_id)
        return list(s.exec(st))

# Certifs
def add_certif(c: Certification)->Certification:
    with get_session() as s:
        s.add(c); s.commit(); s.refresh(c); return c

def list_certifs(contact_id:Optional[int]=None)->List[Certification]:
    with get_session() as s:
        st=select(Certification).order_by(Certification.date_examen.desc().nullslast())
        if contact_id: st=st.where(Certification.contact_id==contact_id)
        return list(s.exec(st))

# KPI
def kpi_totaux()->dict:
    with get_session() as s:
        tot_contacts = list(s.exec(select(Contact)))
        tot_events = list(s.exec(select(Evenement)))
        tot_parts = list(s.exec(select(Participation)))
        tot_paiements = list(s.exec(select(Paiement)))
        regle = sum([p.montant for p in tot_paiements if p.statut=='Réglé'])
        impayes = sum([p.montant for p in tot_paiements if p.statut!='Réglé'])
        membres = len([c for c in tot_contacts if c.type_contact=='Membre'])
        prospects_actifs = len([c for c in tot_contacts if (c.type_contact=='Prospect' and c.statut=='Actif')])
        score_moy= round(sum([c.score_iiba for c in tot_contacts])/len(tot_contacts),2) if tot_contacts else 0
        return {'total_contacts':len(tot_contacts),'membres':membres,'prospects_actifs':prospects_actifs,'evenements':len(tot_events),'participations':len(tot_parts),'ca_regle':regle,'impayes':impayes,'score_moyen':score_moy}

def recalc_score(contact_id:int)->int:
    with get_session() as s:
        c=s.get(Contact, contact_id)
        if not c: return 0
        nb_i=len(list(s.exec(select(Interaction).where(Interaction.contact_id==contact_id))))
        nb_p=len(list(s.exec(select(Participation).where(Participation.contact_id==contact_id))))
        nb_pay=len(list(s.exec(select(Paiement).where(Paiement.contact_id==contact_id))))
        c.score_iiba = nb_i + nb_p + 2*nb_pay
        s.add(c); s.commit(); s.refresh(c)
        return c.score_iiba
