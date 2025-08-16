from typing import List, Dict
from datetime import datetime
import re
CHOICES={'genres':['Homme','Femme','Autre'],'secteurs':['Banque','Télécom','IT','Éducation','Santé','ONG','Industrie','Public','Autre'],'types_contact':['Membre','Prospect','Formateur','Partenaire'],'sources':['Afterwork','Formation','LinkedIn','Recommandation','Site Web','Salon','Autre'],'statuts':['Actif','Inactif','À relancer'],'canaux':['Appel','Email','WhatsApp','Zoom','Présentiel','Autre'],'villes':['Douala','Yaoundé','Limbe','Bafoussam','Garoua','Autres'],'pays':['Cameroun','Côte d\'Ivoire','Sénégal','France','Canada','Autres'],'types_evenement':['Formation','Groupe d\'étude','BA MEET UP','Webinaire','Conférence','Certification'],'lieux':['Présentiel','Zoom','Hybride'],'resultats':['Positif','Négatif','À suivre','Sans suite'],'statuts_paiement':['Réglé','Partiel','Non payé'],'moyens_paiement':['Mobile Money','Virement','CB','Cash'],'types_certif':['ECBA','CCBA','CBAP','PBA'],}

def is_valid_email(email:str)->bool:
    if not email: return True
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None

def clean_phone(phone:str)->str:
    if not phone: return ''
    import re
    return re.sub(r'[^0-9+]','',phone)

def format_period(dt:datetime, type_evt:str)->str:
    try: return dt.strftime('%B %Y')+' - '+(type_evt or '')
    except: return ''
