from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    prenom: str
    genre: Optional[str] = None
    titre: Optional[str] = None
    societe: Optional[str] = None
    secteur: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    ville: Optional[str] = None
    pays: Optional[str] = None
    type_contact: Optional[str] = None
    source: Optional[str] = None
    statut: Optional[str] = None
    score_iiba: int = 0
    date_creation: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
    linkedin: Optional[str] = None
    attentes: Optional[str] = None

class Interaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: int = Field(foreign_key='contact.id')
    date: date
    canal: Optional[str] = None
    objet: Optional[str] = None
    resume: Optional[str] = None
    resultat: Optional[str] = None
    prochaine_action: Optional[str] = None
    relance: Optional[date] = None
    responsable: Optional[str] = None
    nom_contact: Optional[str] = None

class Evenement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    type: Optional[str] = None
    date: Optional[date] = None
    duree_h: Optional[float] = None
    lieu: Optional[str] = None
    formateurs: Optional[str] = None
    invites: Optional[str] = None
    objectif: Optional[str] = None
    periode: Optional[str] = None
    notes: Optional[str] = None

class Participation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: int = Field(foreign_key='contact.id')
    evenement_id: int = Field(foreign_key='evenement.id')
    role: Optional[str] = None
    inscription: Optional[datetime] = None
    arrivee: Optional[datetime] = None
    temps_present: Optional[str] = None
    feedback: Optional[str] = None
    note: Optional[float] = None
    commentaire: Optional[str] = None
    nom_participant: Optional[str] = None
    nom_evenement: Optional[str] = None

class Paiement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: int = Field(foreign_key='contact.id')
    evenement_id: Optional[int] = Field(default=None, foreign_key='evenement.id')
    date_paiement: Optional[date] = None
    montant: float = 0.0
    moyen: Optional[str] = None
    statut: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None
    relance: Optional[date] = None
    nom_contact: Optional[str] = None
    nom_evenement: Optional[str] = None

class Certification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contact_id: int = Field(foreign_key='contact.id')
    type_certif: Optional[str] = None
    date_examen: Optional[date] = None
    resultat: Optional[str] = None
    score: Optional[float] = None
    date_obtention: Optional[date] = None
    validite: Optional[str] = None
    renouvellement: Optional[date] = None
    notes: Optional[str] = None
    nom_contact: Optional[str] = None
